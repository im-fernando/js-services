#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handler de Comandos Quality
Processa e executa comandos para os clientes Quality
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.helpers import sort_services_by_priority

class QualityCommandHandler:
    """Handler de comandos para serviços Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.quality_services = config.get('quality_services', {})
        
        # Modo Quality
        self.quality_mode = False
        
        # Histórico de comandos
        self.command_history = []
        self.history_limit = 1000
        
        self.logger.info("⚡ Command Handler inicializado")
    
    def set_quality_mode(self, enabled: bool) -> None:
        """
        Ativa/desativa modo Quality
        
        Args:
            enabled: Se deve ativar o modo Quality
        """
        self.quality_mode = enabled
        
        if enabled:
            self.logger.info("🎯 Modo Quality ativado - Comandos específicos habilitados")
        else:
            self.logger.info("🎯 Modo Quality desativado")
    
    def execute_command(self, client_id: str, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executa um comando para um cliente
        
        Args:
            client_id: ID do cliente
            action: Ação a executar
            parameters: Parâmetros do comando
            
        Returns:
            Resultado da execução
        """
        try:
            parameters = parameters or {}
            
            # Registrar comando no histórico
            self._add_to_history(client_id, action, parameters)
            
            # Validar comando
            validation_result = self._validate_command(action, parameters)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['error'],
                    'action': action
                }
            
            # Executar comando baseado na ação
            if action == 'get_quality_services_status':
                return self._handle_get_services_status(client_id, parameters)
                
            elif action == 'start_service':
                return self._handle_start_service(client_id, parameters)
                
            elif action == 'stop_service':
                return self._handle_stop_service(client_id, parameters)
                
            elif action == 'restart_service':
                return self._handle_restart_service(client_id, parameters)
                
            elif action == 'restart_all_services':
                return self._handle_restart_all_services(client_id, parameters)
                
            elif action == 'get_processes':
                return self._handle_get_processes(client_id, parameters)
                
            elif action == 'kill_process':
                return self._handle_kill_process(client_id, parameters)
                
            elif action == 'get_logs':
                return self._handle_get_logs(client_id, parameters)
                
            elif action == 'start_log_monitoring':
                return self._handle_start_log_monitoring(client_id, parameters)
                
            elif action == 'stop_log_monitoring':
                return self._handle_stop_log_monitoring(client_id, parameters)
                
            elif action == 'get_system_info':
                return self._handle_get_system_info(client_id, parameters)
                
            else:
                return {
                    'success': False,
                    'error': f'Ação não reconhecida: {action}',
                    'action': action
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao executar comando {action} para {client_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'action': action
            }
    
    def _validate_command(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida um comando antes da execução
        
        Args:
            action: Ação a validar
            parameters: Parâmetros do comando
            
        Returns:
            Resultado da validação
        """
        try:
            # Comandos que requerem service_name
            service_commands = ['start_service', 'stop_service', 'restart_service', 'get_logs', 'start_log_monitoring', 'stop_log_monitoring']
            
            if action in service_commands:
                service_name = parameters.get('service_name')
                if not service_name:
                    return {'valid': False, 'error': 'Parâmetro service_name é obrigatório'}
                
                if service_name not in self.quality_services:
                    return {'valid': False, 'error': f'Serviço {service_name} não é um serviço Quality válido'}
            
            # Comandos que requerem pid
            if action == 'kill_process':
                pid = parameters.get('pid')
                if not pid:
                    return {'valid': False, 'error': 'Parâmetro pid é obrigatório'}
                
                try:
                    int(pid)
                except ValueError:
                    return {'valid': False, 'error': 'Parâmetro pid deve ser um número inteiro'}
            
            # Comandos que requerem lines
            if action == 'get_logs':
                lines = parameters.get('lines', 100)
                try:
                    lines = int(lines)
                    if lines <= 0 or lines > 10000:
                        return {'valid': False, 'error': 'Parâmetro lines deve estar entre 1 e 10000'}
                except ValueError:
                    return {'valid': False, 'error': 'Parâmetro lines deve ser um número inteiro'}
            
            return {'valid': True}
            
        except Exception as e:
            return {'valid': False, 'error': f'Erro na validação: {e}'}
    
    def _handle_get_services_status(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para obter status dos serviços"""
        return {
            'success': True,
            'action': 'get_quality_services_status',
            'message': 'Comando para obter status dos serviços enviado',
            'parameters': parameters
        }
    
    def _handle_start_service(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para iniciar serviço"""
        service_name = parameters.get('service_name')
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'start_service',
            'message': f'Comando para iniciar serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_stop_service(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para parar serviço"""
        service_name = parameters.get('service_name')
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'stop_service',
            'message': f'Comando para parar serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_restart_service(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para reiniciar serviço"""
        service_name = parameters.get('service_name')
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'restart_service',
            'message': f'Comando para reiniciar serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_restart_all_services(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para reiniciar todos os serviços"""
        return {
            'success': True,
            'action': 'restart_all_services',
            'message': 'Comando para reiniciar todos os serviços Quality enviado',
            'parameters': parameters
        }
    
    def _handle_get_processes(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para obter processos"""
        return {
            'success': True,
            'action': 'get_processes',
            'message': 'Comando para obter processos Quality enviado',
            'parameters': parameters
        }
    
    def _handle_kill_process(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para finalizar processo"""
        pid = parameters.get('pid')
        
        return {
            'success': True,
            'action': 'kill_process',
            'message': f'Comando para finalizar processo {pid} enviado',
            'parameters': parameters
        }
    
    def _handle_get_logs(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para obter logs"""
        service_name = parameters.get('service_name')
        lines = parameters.get('lines', 100)
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'get_logs',
            'message': f'Comando para obter {lines} linhas de log do serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_start_log_monitoring(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para iniciar monitoramento de logs"""
        service_name = parameters.get('service_name')
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'start_log_monitoring',
            'message': f'Comando para iniciar monitoramento de logs do serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_stop_log_monitoring(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para parar monitoramento de logs"""
        service_name = parameters.get('service_name')
        service_info = self.quality_services.get(service_name, {})
        
        return {
            'success': True,
            'action': 'stop_log_monitoring',
            'message': f'Comando para parar monitoramento de logs do serviço {service_info.get("name", service_name)} enviado',
            'parameters': parameters
        }
    
    def _handle_get_system_info(self, client_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle para obter informações do sistema"""
        return {
            'success': True,
            'action': 'get_system_info',
            'message': 'Comando para obter informações do sistema enviado',
            'parameters': parameters
        }
    
    def _add_to_history(self, client_id: str, action: str, parameters: Dict[str, Any]) -> None:
        """
        Adiciona comando ao histórico
        
        Args:
            client_id: ID do cliente
            action: Ação executada
            parameters: Parâmetros do comando
        """
        try:
            command_entry = {
                'timestamp': datetime.now().isoformat(),
                'client_id': client_id,
                'action': action,
                'parameters': parameters
            }
            
            self.command_history.append(command_entry)
            
            # Limitar histórico
            if len(self.command_history) > self.history_limit:
                self.command_history = self.command_history[-self.history_limit:]
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar comando ao histórico: {e}")
    
    def get_command_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retorna histórico de comandos
        
        Args:
            limit: Limite de comandos a retornar
            
        Returns:
            Lista de comandos do histórico
        """
        try:
            return self.command_history[-limit:] if limit > 0 else self.command_history
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter histórico de comandos: {e}")
            return []
    
    def get_quality_services_info(self) -> Dict[str, Any]:
        """
        Retorna informações dos serviços Quality
        
        Returns:
            Informações dos serviços
        """
        try:
            services_list = []
            
            # Ordenar serviços por prioridade
            service_names = sort_services_by_priority(list(self.quality_services.keys()), self.quality_services)
            
            for service_name in service_names:
                service_info = self.quality_services[service_name]
                services_list.append({
                    'name': service_name,
                    'display_name': service_info.get('name', service_name),
                    'description': service_info.get('description', ''),
                    'icon': service_info.get('icon', '⚙️'),
                    'critical': service_info.get('critical', False),
                    'dependencies': service_info.get('dependencies', [])
                })
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_services': len(services_list),
                'services': services_list
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter informações dos serviços Quality: {e}")
            return {'error': str(e)}
    
    def get_available_commands(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de comandos disponíveis
        
        Returns:
            Lista de comandos
        """
        try:
            commands = [
                {
                    'action': 'get_quality_services_status',
                    'description': 'Obter status de todos os serviços Quality',
                    'parameters': [],
                    'category': 'services'
                },
                {
                    'action': 'start_service',
                    'description': 'Iniciar um serviço específico',
                    'parameters': ['service_name'],
                    'category': 'services'
                },
                {
                    'action': 'stop_service',
                    'description': 'Parar um serviço específico',
                    'parameters': ['service_name'],
                    'category': 'services'
                },
                {
                    'action': 'restart_service',
                    'description': 'Reiniciar um serviço específico',
                    'parameters': ['service_name'],
                    'category': 'services'
                },
                {
                    'action': 'restart_all_services',
                    'description': 'Reiniciar todos os serviços Quality',
                    'parameters': [],
                    'category': 'services'
                },
                {
                    'action': 'get_processes',
                    'description': 'Obter lista de processos Quality',
                    'parameters': [],
                    'category': 'processes'
                },
                {
                    'action': 'kill_process',
                    'description': 'Finalizar um processo por PID',
                    'parameters': ['pid'],
                    'category': 'processes'
                },
                {
                    'action': 'get_logs',
                    'description': 'Obter logs de um serviço',
                    'parameters': ['service_name', 'lines'],
                    'category': 'logs'
                },
                {
                    'action': 'start_log_monitoring',
                    'description': 'Iniciar monitoramento de logs em tempo real',
                    'parameters': ['service_name'],
                    'category': 'logs'
                },
                {
                    'action': 'stop_log_monitoring',
                    'description': 'Parar monitoramento de logs',
                    'parameters': ['service_name'],
                    'category': 'logs'
                },
                {
                    'action': 'get_system_info',
                    'description': 'Obter informações do sistema',
                    'parameters': [],
                    'category': 'system'
                }
            ]
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_commands': len(commands),
                'commands': commands
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter comandos disponíveis: {e}")
            return {'error': str(e)}
