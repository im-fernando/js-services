#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente de Rede Quality
Gerencia comunicação WebSocket com o servidor de controle
"""

import json
import time
import threading
import websocket
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from utils.helpers import safe_json_serialize

class QualityNetworkClient:
    """Cliente de rede para comunicação com o servidor Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.server_config = config.get('server', {})
        self.client_config = config.get('client', {})
        
        # Configurações de conexão
        self.host = self.server_config.get('host', 'localhost')
        self.port = self.server_config.get('port', 8765)
        self.reconnect_interval = self.server_config.get('reconnect_interval', 5)
        self.heartbeat_interval = self.server_config.get('heartbeat_interval', 30)
        
        # Estado da conexão
        self.ws = None
        self.connected = False
        self.connecting = False
        self.reconnect_thread = None
        self.heartbeat_thread = None
        
        # Filas de mensagens
        self.pending_commands = []
        self.command_lock = threading.Lock()
        
        # Callbacks
        self.message_callbacks = []
        
        # Identificação do cliente
        self.client_id = self.client_config.get('id', 'UNKNOWN_CLIENT')
        self.client_name = self.client_config.get('name', 'Unknown Client')
        
        self.logger.info(f"🌐 Network Client inicializado - {self.client_name} ({self.client_id})")
    
    def connect(self) -> bool:
        """
        Conecta ao servidor
        
        Returns:
            True se conectou com sucesso
        """
        try:
            if self.connected or self.connecting:
                return self.connected
            
            self.connecting = True
            self.logger.info(f"🔌 Conectando ao servidor: {self.host}:{self.port}")
            
            # URL do WebSocket
            ws_url = f"ws://{self.host}:{self.port}"
            
            # Configurar WebSocket
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Iniciar conexão em thread separada
            ws_thread = threading.Thread(
                target=self.ws.run_forever,
                name="WebSocketClient",
                daemon=True
            )
            ws_thread.start()
            
            # Aguardar conexão
            timeout = 10
            start_time = time.time()
            
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if self.connected:
                self.logger.success(f"✅ Conectado ao servidor: {self.host}:{self.port}")
                self._start_heartbeat()
                return True
            else:
                self.logger.error(f"❌ Timeout ao conectar ao servidor")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao conectar: {e}")
            self.connecting = False
            return False
    
    def disconnect(self) -> None:
        """Desconecta do servidor"""
        try:
            self.logger.info("🔌 Desconectando do servidor...")
            
            self.connected = False
            self.connecting = False
            
            # Parar heartbeat
            if self.heartbeat_thread and self.heartbeat_thread.is_alive():
                self.heartbeat_thread.join(timeout=2)
            
            # Fechar WebSocket
            if self.ws:
                self.ws.close()
                self.ws = None
            
            self.logger.info("✅ Desconectado do servidor")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao desconectar: {e}")
    
    def send_message(self, message: Dict[str, Any]) -> bool:
        """
        Envia mensagem para o servidor
        
        Args:
            message: Mensagem para enviar
            
        Returns:
            True se enviou com sucesso
        """
        try:
            if not self.connected or not self.ws:
                self.logger.warning("⚠️  Não conectado ao servidor")
                return False
            
            # Adicionar informações do cliente
            message['client_id'] = self.client_id
            message['timestamp'] = datetime.now().isoformat()
            
            # Serializar mensagem
            json_message = json.dumps(message, default=safe_json_serialize, ensure_ascii=False)
            
            # Enviar
            self.ws.send(json_message)
            
            self.logger.debug(f"📤 Mensagem enviada: {message.get('type', 'unknown')}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def send_heartbeat(self) -> bool:
        """
        Envia heartbeat para o servidor
        
        Returns:
            True se enviou com sucesso
        """
        try:
            heartbeat_message = {
                'type': 'heartbeat',
                'data': {
                    'client_id': self.client_id,
                    'client_name': self.client_name,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'alive'
                }
            }
            
            return self.send_message(heartbeat_message)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar heartbeat: {e}")
            return False
    
    def get_pending_commands(self) -> List[Dict[str, Any]]:
        """
        Retorna comandos pendentes
        
        Returns:
            Lista de comandos pendentes
        """
        with self.command_lock:
            commands = self.pending_commands.copy()
            self.pending_commands.clear()
            return commands
    
    def add_message_callback(self, callback: Callable) -> None:
        """
        Adiciona callback para mensagens recebidas
        
        Args:
            callback: Função callback
        """
        self.message_callbacks.append(callback)
    
    def is_connected(self) -> bool:
        """
        Verifica se está conectado
        
        Returns:
            True se conectado
        """
        return self.connected
    
    def _on_open(self, ws) -> None:
        """Callback de abertura da conexão"""
        try:
            self.connected = True
            self.connecting = False
            self.logger.info("🔌 Conexão WebSocket aberta")
            
            # Enviar identificação inicial
            self._send_client_identification()
            
        except Exception as e:
            self.logger.error(f"❌ Erro no callback de abertura: {e}")
    
    def _on_message(self, ws, message: str) -> None:
        """Callback de mensagem recebida"""
        try:
            # Parsear mensagem JSON
            data = json.loads(message)
            
            self.logger.debug(f"📨 Mensagem recebida: {data.get('type', 'unknown')}")
            
            # Processar comando se for do tipo correto
            if data.get('type') == 'command':
                with self.command_lock:
                    self.pending_commands.append(data)
            
            # Chamar callbacks
            for callback in self.message_callbacks:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"❌ Erro no callback de mensagem: {e}")
                    
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Erro ao decodificar mensagem JSON: {e}")
        except Exception as e:
            self.logger.error(f"❌ Erro no callback de mensagem: {e}")
    
    def _on_error(self, ws, error) -> None:
        """Callback de erro"""
        self.logger.error(f"❌ Erro WebSocket: {error}")
        self.connected = False
        self.connecting = False
    
    def _on_close(self, ws, close_status_code, close_msg) -> None:
        """Callback de fechamento"""
        self.logger.warning(f"🔌 Conexão WebSocket fechada: {close_status_code} - {close_msg}")
        self.connected = False
        self.connecting = False
        
        # Iniciar reconexão automática
        self._start_reconnect()
    
    def _send_client_identification(self) -> None:
        """Envia identificação do cliente"""
        try:
            identification = {
                'type': 'client_identification',
                'data': {
                    'client_id': self.client_id,
                    'client_name': self.client_name,
                    'location': self.client_config.get('location', 'Unknown'),
                    'version': '1.0.0',
                    'capabilities': [
                        'service_management',
                        'process_monitoring',
                        'log_monitoring',
                        'real_time_status'
                    ]
                }
            }
            
            self.send_message(identification)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar identificação: {e}")
    
    def _start_heartbeat(self) -> None:
        """Inicia thread de heartbeat"""
        try:
            self.heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop,
                name="Heartbeat",
                daemon=True
            )
            self.heartbeat_thread.start()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar heartbeat: {e}")
    
    def _heartbeat_loop(self) -> None:
        """Loop de heartbeat"""
        try:
            while self.connected:
                time.sleep(self.heartbeat_interval)
                
                if self.connected:
                    self.send_heartbeat()
                    
        except Exception as e:
            self.logger.error(f"❌ Erro no loop de heartbeat: {e}")
    
    def _start_reconnect(self) -> None:
        """Inicia thread de reconexão"""
        try:
            if self.reconnect_thread and self.reconnect_thread.is_alive():
                return  # Já existe thread de reconexão
            
            self.reconnect_thread = threading.Thread(
                target=self._reconnect_loop,
                name="Reconnect",
                daemon=True
            )
            self.reconnect_thread.start()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar reconexão: {e}")
    
    def _reconnect_loop(self) -> None:
        """Loop de reconexão automática"""
        try:
            self.logger.info("🔄 Iniciando reconexão automática...")
            
            while not self.connected:
                time.sleep(self.reconnect_interval)
                
                if not self.connected:
                    self.logger.info("🔄 Tentando reconectar...")
                    if self.connect():
                        self.logger.success("✅ Reconexão bem-sucedida")
                        break
                    else:
                        self.logger.warning("⚠️  Falha na reconexão, tentando novamente...")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no loop de reconexão: {e}")
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Retorna informações da conexão
        
        Returns:
            Informações da conexão
        """
        return {
            'connected': self.connected,
            'connecting': self.connecting,
            'host': self.host,
            'port': self.port,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'pending_commands': len(self.pending_commands),
            'callbacks_count': len(self.message_callbacks)
        }
