#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe principal do Quality Agent
Gerencia serviços, processos e comunicação com o servidor
"""

import time
import threading
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from .service_manager import QualityServiceManager
from .process_manager import QualityProcessManager
from .log_monitor import QualityLogMonitor
from .network_client import QualityNetworkClient
from utils.helpers import get_system_info, safe_json_serialize

class QualityAgent:
    """Agente principal para monitoramento e controle dos serviços Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.running = False
        
        # Componentes principais
        self.service_manager = QualityServiceManager(config, logger)
        self.process_manager = QualityProcessManager(config, logger)
        self.log_monitor = QualityLogMonitor(config, logger)
        self.network_client = QualityNetworkClient(config, logger)
        
        # Threads de monitoramento
        self.monitor_thread = None
        self.heartbeat_thread = None
        
        # Cache de status
        self.last_status = {}
        self.status_lock = threading.Lock()
        
        self.logger.info("🤖 Quality Agent inicializado")
    
    def start(self) -> None:
        """Inicia o agente e todos os componentes"""
        try:
            self.logger.info("🚀 Iniciando Quality Agent...")
            self.running = True
            
            # Conectar ao servidor
            if not self.network_client.connect():
                self.logger.error("❌ Falha ao conectar ao servidor")
                return
            
            # Iniciar threads de monitoramento
            self._start_monitoring_threads()
            
            # Enviar informações iniciais
            self._send_initial_info()
            
            self.logger.success("✅ Quality Agent iniciado com sucesso")
            
            # Loop principal
            self._main_loop()
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar agente: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Para o agente e todos os componentes"""
        self.logger.info("🛑 Parando Quality Agent...")
        self.running = False
        
        # Parar threads
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=5)
        
        # Desconectar do servidor
        self.network_client.disconnect()
        
        self.logger.info("✅ Quality Agent parado")
    
    def _start_monitoring_threads(self) -> None:
        """Inicia threads de monitoramento"""
        # Thread de monitoramento de status
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            name="StatusMonitor",
            daemon=True
        )
        self.monitor_thread.start()
        
        # Thread de heartbeat
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            name="Heartbeat",
            daemon=True
        )
        self.heartbeat_thread.start()
    
    def _monitoring_loop(self) -> None:
        """Loop de monitoramento contínuo"""
        while self.running:
            try:
                # Coletar status dos serviços
                services_status = self.service_manager.get_all_services_status()
                
                # Coletar status dos processos
                processes_status = self.process_manager.get_quality_processes()
                
                # Atualizar cache de status
                with self.status_lock:
                    self.last_status = {
                        'timestamp': datetime.now().isoformat(),
                        'services': services_status,
                        'processes': processes_status,
                        'system': get_system_info()
                    }
                
                # Enviar status para o servidor
                self._send_status_update()
                
                # Aguardar próximo ciclo
                time.sleep(5)  # Atualizar a cada 5 segundos
                
            except Exception as e:
                self.logger.error(f"❌ Erro no loop de monitoramento: {e}")
                time.sleep(10)  # Aguardar mais tempo em caso de erro
    
    def _heartbeat_loop(self) -> None:
        """Loop de heartbeat para manter conexão ativa"""
        heartbeat_interval = self.config.get('server', {}).get('heartbeat_interval', 30)
        
        while self.running:
            try:
                time.sleep(heartbeat_interval)
                
                if self.running:
                    self.network_client.send_heartbeat()
                    
            except Exception as e:
                self.logger.error(f"❌ Erro no heartbeat: {e}")
    
    def _main_loop(self) -> None:
        """Loop principal do agente"""
        try:
            while self.running:
                # Processar comandos recebidos
                self._process_commands()
                
                # Aguardar um pouco antes da próxima iteração
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("👋 Interrupção recebida pelo usuário")
        except Exception as e:
            self.logger.error(f"❌ Erro no loop principal: {e}")
    
    def _process_commands(self) -> None:
        """Processa comandos recebidos do servidor"""
        try:
            commands = self.network_client.get_pending_commands()
            
            for command in commands:
                self._execute_command(command)
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar comandos: {e}")
    
    def _execute_command(self, command: Dict[str, Any]) -> None:
        """Executa um comando recebido"""
        try:
            action = command.get('data', {}).get('action')
            parameters = command.get('data', {}).get('parameters', {})
            
            self.logger.info(f"📨 Executando comando: {action}")
            
            result = None
            
            if action == 'get_quality_services_status':
                result = self.service_manager.get_all_services_status()
                
            elif action == 'start_service':
                service_name = parameters.get('service_name')
                result = self.service_manager.start_service(service_name)
                
            elif action == 'stop_service':
                service_name = parameters.get('service_name')
                result = self.service_manager.stop_service(service_name)
                
            elif action == 'restart_service':
                service_name = parameters.get('service_name')
                result = self.service_manager.restart_service(service_name)
                
            elif action == 'restart_all_services':
                result = self.service_manager.restart_all_services()
                
            elif action == 'get_processes':
                result = self.process_manager.get_quality_processes()
                
            elif action == 'kill_process':
                pid = parameters.get('pid')
                result = self.process_manager.kill_process(pid)
                
            elif action == 'get_logs':
                service_name = parameters.get('service_name')
                lines = parameters.get('lines', 100)
                result = self.log_monitor.get_recent_logs(service_name, lines)
                
            elif action == 'start_log_monitoring':
                service_name = parameters.get('service_name')
                result = self.log_monitor.start_monitoring(service_name)
                
            elif action == 'stop_log_monitoring':
                service_name = parameters.get('service_name')
                result = self.log_monitor.stop_monitoring(service_name)
                
            else:
                result = {'error': f'Ação não reconhecida: {action}'}
            
            # Enviar resposta
            self._send_command_response(command, result)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao executar comando: {e}")
            self._send_command_response(command, {'error': str(e)})
    
    def _send_initial_info(self) -> None:
        """Envia informações iniciais para o servidor"""
        try:
            initial_info = {
                'type': 'client_info',
                'client_id': self.config['client']['id'],
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'name': self.config['client']['name'],
                    'location': self.config['client']['location'],
                    'system_info': get_system_info(),
                    'installed_services': self.service_manager.get_installed_services(),
                    'agent_version': '1.0.0'
                }
            }
            
            self.network_client.send_message(initial_info)
            self.logger.info("📤 Informações iniciais enviadas")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar informações iniciais: {e}")
    
    def _send_status_update(self) -> None:
        """Envia atualização de status para o servidor"""
        try:
            with self.status_lock:
                status_data = self.last_status.copy()
            
            message = {
                'type': 'status_update',
                'client_id': self.config['client']['id'],
                'timestamp': datetime.now().isoformat(),
                'data': status_data
            }
            
            self.network_client.send_message(message)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar status: {e}")
    
    def _send_command_response(self, original_command: Dict[str, Any], result: Any) -> None:
        """Envia resposta de comando para o servidor"""
        try:
            response = {
                'type': 'command_response',
                'client_id': self.config['client']['id'],
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'original_action': original_command.get('data', {}).get('action'),
                    'result': result,
                    'success': 'error' not in str(result).lower()
                }
            }
            
            self.network_client.send_message(response)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar resposta: {e}")
    
    def install_as_service(self) -> None:
        """Instala o agente como serviço Windows"""
        try:
            self.logger.info("📦 Instalando como serviço Windows...")
            
            # Aqui seria implementada a instalação como serviço Windows
            # Por enquanto, apenas log
            self.logger.info("⚠️  Instalação como serviço não implementada ainda")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao instalar serviço: {e}")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        with self.status_lock:
            return self.last_status.copy()
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao servidor"""
        return self.network_client.is_connected()
