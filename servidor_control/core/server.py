#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Principal Quality Control Panel
Gerencia conexões WebSocket e coordena operações
"""

import json
import time
import threading
import websocket
from typing import Dict, Any, List, Optional
from datetime import datetime

from .client_manager import QualityClientManager
from .command_handler import QualityCommandHandler
from .session_manager import SessionManager
from .attendant_manager import AttendantManager
from database.activity_log import ActivityLogger
from utils.helpers import safe_json_serialize, validate_client_id

class QualityControlServer:
    """Servidor principal do Quality Control Panel"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.server_config = config.get('server', {})
        
        # Configurações do servidor
        self.host = self.server_config.get('host', '0.0.0.0')
        self.port = self.server_config.get('port', 8765)
        self.max_clients = self.server_config.get('max_clients', 50)
        self.heartbeat_timeout = self.server_config.get('heartbeat_timeout', 60)
        
        # Componentes principais
        self.client_manager = QualityClientManager(config, logger)
        self.command_handler = QualityCommandHandler(config, logger)
        self.session_manager = SessionManager(logger)
        self.attendant_manager = AttendantManager(config, logger)
        self.activity_logger = ActivityLogger(logger)
        
        # Estado do servidor
        self.running = False
        self.server_thread = None
        self.cleanup_thread = None
        
        # WebSocket server
        self.ws_server = None
        
        # Modo Quality
        self.quality_mode = False
        self.multi_attendant_mode = True
        
        self.logger.info("🌐 Quality Control Server inicializado")
    
    def start(self) -> None:
        """Inicia o servidor"""
        try:
            self.logger.info(f"🚀 Iniciando servidor em {self.host}:{self.port}")
            self.running = True
            
            # Iniciar thread de limpeza
            self._start_cleanup_thread()
            
            # Iniciar servidor WebSocket
            self._start_websocket_server()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar servidor: {e}")
            raise
    
    def stop(self) -> None:
        """Para o servidor"""
        try:
            self.logger.info("🛑 Parando servidor...")
            self.running = False
            
            # Parar threads
            if self.cleanup_thread and self.cleanup_thread.is_alive():
                self.cleanup_thread.join(timeout=5)
            
            # Fechar servidor WebSocket
            if self.ws_server:
                self.ws_server.shutdown()
            
            # Desconectar todos os clientes
            self.client_manager.disconnect_all_clients()
            
            self.logger.info("✅ Servidor parado")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar servidor: {e}")
    
    def set_quality_mode(self, enabled: bool) -> None:
        """
        Ativa/desativa modo Quality
        
        Args:
            enabled: Se deve ativar o modo Quality
        """
        self.quality_mode = enabled
        self.command_handler.set_quality_mode(enabled)
        
        if enabled:
            self.logger.info("🎯 Modo Quality ativado")
        else:
            self.logger.info("🎯 Modo Quality desativado")
    
    def _start_websocket_server(self) -> None:
        """Inicia servidor WebSocket"""
        try:
            import websocket_server
            
            # Configurar servidor WebSocket
            self.ws_server = websocket_server.WebsocketServer(
                self.port,
                host=self.host,
                loglevel=websocket_server.logging.INFO
            )
            
            # Configurar callbacks
            self.ws_server.set_fn_new_client(self._on_client_connect)
            self.ws_server.set_fn_client_left(self._on_client_disconnect)
            self.ws_server.set_fn_message_received(self._on_message_received)
            
            self.logger.success(f"✅ Servidor WebSocket iniciado em {self.host}:{self.port}")
            
            # Executar servidor em thread separada
            self.server_thread = threading.Thread(
                target=self.ws_server.run_forever,
                name="WebSocketServer",
                daemon=True
            )
            self.server_thread.start()
            
        except ImportError:
            self.logger.error("❌ websocket-server não instalado. Execute: pip install websocket-server")
            raise
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar servidor WebSocket: {e}")
            raise
    
    def _start_cleanup_thread(self) -> None:
        """Inicia thread de limpeza"""
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_loop,
            name="CleanupThread",
            daemon=True
        )
        self.cleanup_thread.start()
    
    def _cleanup_loop(self) -> None:
        """Loop de limpeza de clientes inativos"""
        while self.running:
            try:
                time.sleep(30)  # Executar a cada 30 segundos
                
                if self.running:
                    self.client_manager.cleanup_inactive_clients(self.heartbeat_timeout)
                    
            except Exception as e:
                self.logger.error(f"❌ Erro no loop de limpeza: {e}")
    
    def _on_client_connect(self, client, server) -> None:
        """Callback de conexão de cliente"""
        try:
            client_id = f"CLIENT_{client['id']}"
            self.logger.info(f"🔌 Cliente conectado: {client_id}")
            
            # Registrar cliente
            self.client_manager.add_client(client, client_id)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar conexão de cliente: {e}")
    
    def _on_client_disconnect(self, client, server) -> None:
        """Callback de desconexão de cliente"""
        try:
            client_id = f"CLIENT_{client['id']}"
            client_info = self.client_manager.get_client_info(client_id)
            
            if client_info:
                client_name = client_info.get('name', 'Unknown')
                self.logger.client_disconnected(client_id, client_name)
            
            # Remover cliente
            self.client_manager.remove_client(client_id)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar desconexão de cliente: {e}")
    
    def _on_message_received(self, client, server, message: str) -> None:
        """Callback de mensagem recebida"""
        try:
            # Parsear mensagem JSON
            data = json.loads(message)
            
            client_id = f"CLIENT_{client['id']}"
            
            self.logger.debug(f"📨 Mensagem recebida de {client_id}: {data.get('type', 'unknown')}")
            
            # Processar mensagem
            self._process_message(client, client_id, data)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Erro ao decodificar mensagem JSON: {e}")
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar mensagem: {e}")
    
    def _process_message(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """
        Processa mensagem recebida
        
        Args:
            client: Cliente WebSocket
            client_id: ID do cliente
            data: Dados da mensagem
        """
        try:
            message_type = data.get('type')
            
            if message_type == 'client_identification':
                self._handle_client_identification(client, client_id, data)
                
            elif message_type == 'client_info':
                self._handle_client_info(client, client_id, data)
                
            elif message_type == 'status_update':
                self._handle_status_update(client, client_id, data)
                
            elif message_type == 'heartbeat':
                self._handle_heartbeat(client, client_id, data)
                
            elif message_type == 'command_response':
                self._handle_command_response(client, client_id, data)
                
            else:
                self.logger.warning(f"⚠️  Tipo de mensagem desconhecido: {message_type}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar mensagem de {client_id}: {e}")
    
    def _handle_client_identification(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """Processa identificação de cliente"""
        try:
            client_data = data.get('data', {})
            real_client_id = client_data.get('client_id', client_id)
            
            # Validar ID do cliente
            if not validate_client_id(real_client_id):
                self.logger.warning(f"⚠️  ID de cliente inválido: {real_client_id}")
                return
            
            # Atualizar informações do cliente
            self.client_manager.update_client_info(client_id, {
                'real_client_id': real_client_id,
                'name': client_data.get('client_name', 'Unknown Client'),
                'location': client_data.get('location', 'Unknown'),
                'version': client_data.get('version', '1.0.0'),
                'capabilities': client_data.get('capabilities', []),
                'last_activity': datetime.now().isoformat()
            })
            
            client_name = client_data.get('client_name', 'Unknown')
            self.logger.client_connected(real_client_id, client_name)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar identificação: {e}")
    
    def _handle_client_info(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """Processa informações do cliente"""
        try:
            client_data = data.get('data', {})
            
            # Atualizar informações do cliente
            self.client_manager.update_client_info(client_id, {
                'system_info': client_data.get('system_info', {}),
                'installed_services': client_data.get('installed_services', []),
                'agent_version': client_data.get('agent_version', '1.0.0'),
                'last_activity': datetime.now().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar informações do cliente: {e}")
    
    def _handle_status_update(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """Processa atualização de status"""
        try:
            status_data = data.get('data', {})
            
            # Atualizar status do cliente
            self.client_manager.update_client_status(client_id, status_data)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar atualização de status: {e}")
    
    def _handle_heartbeat(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """Processa heartbeat"""
        try:
            # Atualizar última atividade
            self.client_manager.update_client_activity(client_id)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar heartbeat: {e}")
    
    def _handle_command_response(self, client, client_id: str, data: Dict[str, Any]) -> None:
        """Processa resposta de comando"""
        try:
            response_data = data.get('data', {})
            action = response_data.get('original_action', 'unknown')
            success = response_data.get('success', False)
            
            self.logger.command_executed(client_id, action, success)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar resposta de comando: {e}")
    
    def send_command_to_client(self, client_id: str, action: str, parameters: Dict[str, Any] = None) -> bool:
        """
        Envia comando para um cliente específico
        
        Args:
            client_id: ID do cliente
            action: Ação a executar
            parameters: Parâmetros do comando
            
        Returns:
            True se enviou com sucesso
        """
        try:
            client = self.client_manager.get_client(client_id)
            if not client:
                self.logger.warning(f"⚠️  Cliente {client_id} não encontrado")
                return False
            
            command = {
                'type': 'command',
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'action': action,
                    'parameters': parameters or {}
                }
            }
            
            # Enviar comando
            message = json.dumps(command, default=safe_json_serialize, ensure_ascii=False)
            client['handler'].send_message(message)
            
            self.logger.info(f"📤 Comando enviado para {client_id}: {action}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar comando para {client_id}: {e}")
            return False
    
    def broadcast_command(self, action: str, parameters: Dict[str, Any] = None) -> int:
        """
        Envia comando para todos os clientes conectados
        
        Args:
            action: Ação a executar
            parameters: Parâmetros do comando
            
        Returns:
            Número de clientes que receberam o comando
        """
        try:
            clients = self.client_manager.get_all_clients()
            sent_count = 0
            
            for client_id in clients:
                if self.send_command_to_client(client_id, action, parameters):
                    sent_count += 1
            
            self.logger.info(f"📢 Comando broadcast enviado para {sent_count} clientes: {action}")
            return sent_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar comando broadcast: {e}")
            return 0
    
    def get_server_status(self) -> Dict[str, Any]:
        """
        Retorna status do servidor
        
        Returns:
            Status do servidor
        """
        try:
            clients = self.client_manager.get_all_clients()
            client_count = len(clients)
            
            return {
                'running': self.running,
                'host': self.host,
                'port': self.port,
                'connected_clients': client_count,
                'max_clients': self.max_clients,
                'quality_mode': self.quality_mode,
                'uptime': time.time() - getattr(self, '_start_time', time.time()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter status do servidor: {e}")
            return {'error': str(e)}
    
    def get_clients_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo dos clientes conectados
        
        Returns:
            Resumo dos clientes
        """
        return self.client_manager.get_clients_summary()
