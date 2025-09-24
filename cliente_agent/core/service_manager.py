#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Serviços Quality
Controla os 5 serviços específicos do sistema Quality
"""

import os
import subprocess
import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.helpers import get_process_by_name, kill_process_by_pid, validate_path, format_uptime, format_bytes

class QualityServiceManager:
    """Gerenciador específico para serviços Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.services = config.get('services', [])
        self.dependencies = config.get('service_dependencies', {})
        self.startup_order = config.get('startup_order', [])
        
        # Cache de status
        self.status_cache = {}
        self.cache_lock = threading.Lock()
        
        self.logger.info(f"🔧 Service Manager inicializado com {len(self.services)} serviços")
    
    def get_installed_services(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de serviços que estão realmente instalados
        
        Returns:
            Lista de serviços instalados
        """
        installed = []
        
        for service in self.services:
            if not service.get('enabled', True):
                continue
                
            executable_path = service.get('executable_path', '')
            
            if validate_path(executable_path):
                installed.append({
                    'name': service['name'],
                    'display_name': service['display_name'],
                    'executable_path': executable_path,
                    'description': service.get('description', ''),
                    'log_base_path': service.get('log_base_path', '')
                })
            else:
                self.logger.warning(f"⚠️  Serviço {service['display_name']} não encontrado: {executable_path}")
        
        return installed
    
    def get_all_services_status(self) -> Dict[str, Any]:
        """
        Retorna status de todos os serviços
        
        Returns:
            Dicionário com status de cada serviço
        """
        with self.cache_lock:
            status = {}
            
            for service in self.services:
                if not service.get('enabled', True):
                    continue
                    
                service_name = service['name']
                service_status = self._get_service_status(service)
                status[service_name] = service_status
            
            self.status_cache = status
            return status.copy()
    
    def _get_service_status(self, service: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtém status detalhado de um serviço
        
        Args:
            service: Configuração do serviço
            
        Returns:
            Status detalhado do serviço
        """
        service_name = service['name']
        display_name = service['display_name']
        executable_path = service.get('executable_path', '')
        
        # Buscar processos do serviço
        processes = get_process_by_name(service_name)
        
        if not processes:
            # Tentar buscar pelo nome do executável
            exe_name = os.path.basename(executable_path)
            processes = get_process_by_name(exe_name)
        
        if processes:
            # Serviço está rodando
            main_process = processes[0]  # Pegar o primeiro processo
            
            return {
                'status': 'running',
                'display_name': display_name,
                'pid': main_process['pid'],
                'name': main_process['name'],
                'exe': main_process['exe'],
                'create_time': main_process['create_time'],
                'uptime': format_uptime(time.time() - main_process['create_time']),
                'memory_usage': format_bytes(main_process['memory_usage']),
                'memory_bytes': main_process['memory_usage'],
                'cpu_percent': main_process['cpu_percent'],
                'process_count': len(processes),
                'last_check': datetime.now().isoformat()
            }
        else:
            # Serviço não está rodando
            return {
                'status': 'stopped',
                'display_name': display_name,
                'pid': None,
                'name': None,
                'exe': executable_path,
                'uptime': None,
                'memory_usage': '0 B',
                'memory_bytes': 0,
                'cpu_percent': 0.0,
                'process_count': 0,
                'last_check': datetime.now().isoformat(),
                'error': 'Processo não encontrado'
            }
    
    def start_service(self, service_name: str) -> Dict[str, Any]:
        """
        Inicia um serviço específico
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Resultado da operação
        """
        try:
            service = self._find_service_by_name(service_name)
            if not service:
                return {'success': False, 'error': f'Serviço {service_name} não encontrado'}
            
            executable_path = service.get('executable_path', '')
            if not validate_path(executable_path):
                return {'success': False, 'error': f'Executável não encontrado: {executable_path}'}
            
            # Verificar se já está rodando
            current_status = self._get_service_status(service)
            if current_status['status'] == 'running':
                return {'success': True, 'message': f'Serviço {service_name} já está rodando'}
            
            # Iniciar o serviço
            self.logger.info(f"🚀 Iniciando serviço: {service['display_name']}")
            
            # Executar o serviço
            process = subprocess.Popen(
                [executable_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(executable_path)
            )
            
            # Aguardar um pouco para verificar se iniciou
            time.sleep(2)
            
            # Verificar se iniciou com sucesso
            new_status = self._get_service_status(service)
            if new_status['status'] == 'running':
                self.logger.success(f"✅ Serviço {service['display_name']} iniciado com sucesso")
                return {
                    'success': True,
                    'message': f'Serviço {service_name} iniciado com sucesso',
                    'pid': new_status['pid']
                }
            else:
                return {
                    'success': False,
                    'error': f'Falha ao iniciar serviço {service_name}'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar serviço {service_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def stop_service(self, service_name: str) -> Dict[str, Any]:
        """
        Para um serviço específico
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Resultado da operação
        """
        try:
            service = self._find_service_by_name(service_name)
            if not service:
                return {'success': False, 'error': f'Serviço {service_name} não encontrado'}
            
            # Verificar se está rodando
            current_status = self._get_service_status(service)
            if current_status['status'] != 'running':
                return {'success': True, 'message': f'Serviço {service_name} já está parado'}
            
            pid = current_status['pid']
            if not pid:
                return {'success': False, 'error': 'PID do processo não encontrado'}
            
            self.logger.info(f"🛑 Parando serviço: {service['display_name']} (PID: {pid})")
            
            # Finalizar o processo
            success = kill_process_by_pid(pid)
            
            if success:
                self.logger.success(f"✅ Serviço {service['display_name']} parado com sucesso")
                return {
                    'success': True,
                    'message': f'Serviço {service_name} parado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'error': f'Falha ao parar serviço {service_name}'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar serviço {service_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def restart_service(self, service_name: str) -> Dict[str, Any]:
        """
        Reinicia um serviço específico
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Resultado da operação
        """
        try:
            self.logger.info(f"🔄 Reiniciando serviço: {service_name}")
            
            # Parar o serviço
            stop_result = self.stop_service(service_name)
            if not stop_result['success']:
                return stop_result
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Iniciar o serviço
            start_result = self.start_service(service_name)
            if not start_result['success']:
                return start_result
            
            self.logger.success(f"✅ Serviço {service_name} reiniciado com sucesso")
            return {
                'success': True,
                'message': f'Serviço {service_name} reiniciado com sucesso'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao reiniciar serviço {service_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def restart_all_services(self) -> Dict[str, Any]:
        """
        Reinicia todos os serviços na ordem correta de dependências
        
        Returns:
            Resultado da operação
        """
        try:
            self.logger.info("🔄 Reiniciando todos os serviços Quality...")
            
            results = {}
            
            # Parar todos os serviços (ordem inversa)
            stop_order = list(reversed(self.startup_order))
            for service_name in stop_order:
                if self._is_service_enabled(service_name):
                    result = self.stop_service(service_name)
                    results[f'stop_{service_name}'] = result
                    time.sleep(1)
            
            # Aguardar um pouco
            time.sleep(3)
            
            # Iniciar todos os serviços (ordem correta)
            for service_name in self.startup_order:
                if self._is_service_enabled(service_name):
                    result = self.start_service(service_name)
                    results[f'start_{service_name}'] = result
                    time.sleep(2)  # Aguardar entre inicializações
            
            self.logger.success("✅ Todos os serviços Quality reiniciados")
            return {
                'success': True,
                'message': 'Todos os serviços reiniciados',
                'details': results
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao reiniciar todos os serviços: {e}")
            return {'success': False, 'error': str(e)}
    
    def _find_service_by_name(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Encontra um serviço pelo nome
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Configuração do serviço ou None
        """
        for service in self.services:
            if service['name'] == service_name:
                return service
        return None
    
    def _is_service_enabled(self, service_name: str) -> bool:
        """
        Verifica se um serviço está habilitado
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            True se o serviço está habilitado
        """
        service = self._find_service_by_name(service_name)
        return service and service.get('enabled', True)
    
    def get_service_dependencies(self, service_name: str) -> List[str]:
        """
        Retorna dependências de um serviço
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Lista de dependências
        """
        return self.dependencies.get(service_name, [])
    
    def check_dependencies(self, service_name: str) -> Dict[str, Any]:
        """
        Verifica se as dependências de um serviço estão atendidas
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Status das dependências
        """
        dependencies = self.get_service_dependencies(service_name)
        status = {}
        
        for dep in dependencies:
            dep_status = self._get_service_status(self._find_service_by_name(dep))
            status[dep] = dep_status['status'] == 'running'
        
        return {
            'service': service_name,
            'dependencies': status,
            'all_satisfied': all(status.values())
        }
