#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Logs Quality
Implementa streaming de logs em tempo real com navegação automática
"""

import os
import time
import threading
import queue
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from utils.log_finder import QualityLogFinder
from utils.helpers import validate_path, get_file_size_mb

class QualityLogMonitor:
    """Monitor de logs em tempo real para serviços Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.services = config.get('services', [])
        self.log_config = config.get('log_monitoring', {})
        
        # Configurações de monitoramento
        self.refresh_interval = self.log_config.get('refresh_interval', 1)
        self.max_lines_buffer = self.log_config.get('max_lines_buffer', 1000)
        self.encoding = self.log_config.get('encoding', 'utf-8')
        
        # Estado do monitoramento
        self.monitoring_services = {}  # service_name -> monitor_info
        self.monitor_threads = {}
        self.stop_events = {}
        
        # Callbacks para streaming
        self.stream_callbacks = {}
        
        self.logger.info("📋 Log Monitor inicializado")
    
    def get_recent_logs(self, service_name: str, lines: int = 100) -> Dict[str, Any]:
        """
        Obtém as últimas linhas de log de um serviço
        
        Args:
            service_name: Nome do serviço
            lines: Número de linhas para retornar
            
        Returns:
            Dicionário com as linhas de log
        """
        try:
            service = self._find_service_by_name(service_name)
            if not service:
                return {'error': f'Serviço {service_name} não encontrado'}
            
            log_base_path = service.get('log_base_path', '')
            if not validate_path(log_base_path):
                return {'error': f'Caminho de log não encontrado: {log_base_path}'}
            
            # Encontrar arquivo de log mais recente
            log_finder = QualityLogFinder(log_base_path)
            latest_log_file = log_finder.find_latest_log_file()
            
            if not latest_log_file:
                return {'error': 'Nenhum arquivo de log encontrado'}
            
            # Ler as últimas linhas
            log_lines = self._read_last_lines(latest_log_file, lines)
            
            return {
                'service_name': service_name,
                'log_file': latest_log_file,
                'file_size_mb': get_file_size_mb(latest_log_file),
                'lines_count': len(log_lines),
                'lines': log_lines,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter logs do serviço {service_name}: {e}")
            return {'error': str(e)}
    
    def start_monitoring(self, service_name: str, callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Inicia monitoramento de logs em tempo real
        
        Args:
            service_name: Nome do serviço
            callback: Função callback para receber novas linhas
            
        Returns:
            Resultado da operação
        """
        try:
            if service_name in self.monitoring_services:
                return {'success': True, 'message': f'Monitoramento de {service_name} já está ativo'}
            
            service = self._find_service_by_name(service_name)
            if not service:
                return {'error': f'Serviço {service_name} não encontrado'}
            
            log_base_path = service.get('log_base_path', '')
            if not validate_path(log_base_path):
                return {'error': f'Caminho de log não encontrado: {log_base_path}'}
            
            # Configurar callback se fornecido
            if callback:
                self.stream_callbacks[service_name] = callback
            
            # Criar evento de parada
            stop_event = threading.Event()
            self.stop_events[service_name] = stop_event
            
            # Iniciar thread de monitoramento
            monitor_thread = threading.Thread(
                target=self._monitor_service_logs,
                args=(service_name, stop_event),
                name=f"LogMonitor-{service_name}",
                daemon=True
            )
            
            self.monitor_threads[service_name] = monitor_thread
            monitor_thread.start()
            
            # Registrar serviço como sendo monitorado
            self.monitoring_services[service_name] = {
                'start_time': datetime.now().isoformat(),
                'log_base_path': log_base_path,
                'status': 'monitoring'
            }
            
            self.logger.info(f"📋 Iniciado monitoramento de logs: {service['display_name']}")
            
            return {
                'success': True,
                'message': f'Monitoramento de {service_name} iniciado',
                'service': service['display_name']
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar monitoramento de {service_name}: {e}")
            return {'error': str(e)}
    
    def stop_monitoring(self, service_name: str) -> Dict[str, Any]:
        """
        Para o monitoramento de logs de um serviço
        
        Args:
            service_name: Nome do serviço
            
        Returns:
            Resultado da operação
        """
        try:
            if service_name not in self.monitoring_services:
                return {'success': True, 'message': f'Monitoramento de {service_name} não está ativo'}
            
            # Sinalizar parada
            if service_name in self.stop_events:
                self.stop_events[service_name].set()
            
            # Aguardar thread terminar
            if service_name in self.monitor_threads:
                thread = self.monitor_threads[service_name]
                thread.join(timeout=5)
                del self.monitor_threads[service_name]
            
            # Limpar registros
            if service_name in self.monitoring_services:
                del self.monitoring_services[service_name]
            
            if service_name in self.stop_events:
                del self.stop_events[service_name]
            
            if service_name in self.stream_callbacks:
                del self.stream_callbacks[service_name]
            
            service = self._find_service_by_name(service_name)
            service_display = service['display_name'] if service else service_name
            
            self.logger.info(f"📋 Parado monitoramento de logs: {service_display}")
            
            return {
                'success': True,
                'message': f'Monitoramento de {service_name} parado'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar monitoramento de {service_name}: {e}")
            return {'error': str(e)}
    
    def _monitor_service_logs(self, service_name: str, stop_event: threading.Event) -> None:
        """
        Thread de monitoramento de logs para um serviço
        
        Args:
            service_name: Nome do serviço
            stop_event: Evento para sinalizar parada
        """
        try:
            service = self._find_service_by_name(service_name)
            if not service:
                return
            
            log_base_path = service.get('log_base_path', '')
            log_finder = QualityLogFinder(log_base_path)
            
            last_file = None
            last_position = 0
            
            while not stop_event.is_set():
                try:
                    # Encontrar arquivo de log mais recente
                    current_file = log_finder.find_latest_log_file()
                    
                    if not current_file:
                        time.sleep(self.refresh_interval)
                        continue
                    
                    # Se mudou o arquivo, resetar posição
                    if current_file != last_file:
                        last_file = current_file
                        last_position = 0
                        self.logger.debug(f"📄 Novo arquivo de log detectado: {current_file}")
                    
                    # Ler novas linhas
                    new_lines = self._read_new_lines(current_file, last_position)
                    
                    if new_lines:
                        last_position = os.path.getsize(current_file)
                        
                        # Processar novas linhas
                        for line in new_lines:
                            self._process_log_line(service_name, line.strip())
                    
                    time.sleep(self.refresh_interval)
                    
                except Exception as e:
                    self.logger.error(f"❌ Erro no monitoramento de {service_name}: {e}")
                    time.sleep(self.refresh_interval * 2)
            
        except Exception as e:
            self.logger.error(f"❌ Erro fatal no monitoramento de {service_name}: {e}")
    
    def _read_last_lines(self, file_path: str, lines: int) -> List[str]:
        """
        Lê as últimas N linhas de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            lines: Número de linhas
            
        Returns:
            Lista de linhas
        """
        try:
            with open(file_path, 'r', encoding=self.encoding, errors='ignore') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.logger.error(f"❌ Erro ao ler arquivo {file_path}: {e}")
            return []
    
    def _read_new_lines(self, file_path: str, last_position: int) -> List[str]:
        """
        Lê novas linhas de um arquivo a partir de uma posição
        
        Args:
            file_path: Caminho do arquivo
            last_position: Última posição lida
            
        Returns:
            Lista de novas linhas
        """
        try:
            current_size = os.path.getsize(file_path)
            
            if current_size <= last_position:
                return []
            
            with open(file_path, 'r', encoding=self.encoding, errors='ignore') as f:
                f.seek(last_position)
                new_content = f.read()
                
                if new_content:
                    return new_content.splitlines()
                else:
                    return []
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao ler novas linhas de {file_path}: {e}")
            return []
    
    def _process_log_line(self, service_name: str, line: str) -> None:
        """
        Processa uma linha de log
        
        Args:
            service_name: Nome do serviço
            line: Linha de log
        """
        try:
            if not line.strip():
                return
            
            # Detectar nível de log
            log_level = self._detect_log_level(line)
            
            # Criar estrutura de log
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'service': service_name,
                'level': log_level,
                'message': line,
                'raw_line': line
            }
            
            # Chamar callback se configurado
            if service_name in self.stream_callbacks:
                try:
                    self.stream_callbacks[service_name](log_entry)
                except Exception as e:
                    self.logger.error(f"❌ Erro no callback de {service_name}: {e}")
            
            # Log local se for erro crítico
            if log_level in ['ERROR', 'FATAL', 'CRITICAL']:
                self.logger.warning(f"🚨 {service_name}: {line}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar linha de log: {e}")
    
    def _detect_log_level(self, line: str) -> str:
        """
        Detecta o nível de log de uma linha
        
        Args:
            line: Linha de log
            
        Returns:
            Nível de log detectado
        """
        line_upper = line.upper()
        
        if any(level in line_upper for level in ['FATAL', 'CRITICAL']):
            return 'FATAL'
        elif any(level in line_upper for level in ['ERROR', 'ERRO']):
            return 'ERROR'
        elif any(level in line_upper for level in ['WARN', 'WARNING', 'AVISO']):
            return 'WARNING'
        elif any(level in line_upper for level in ['INFO', 'INFORMACAO']):
            return 'INFO'
        elif any(level in line_upper for level in ['DEBUG', 'TRACE']):
            return 'DEBUG'
        else:
            return 'INFO'
    
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
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        Retorna status do monitoramento
        
        Returns:
            Status do monitoramento
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'monitoring_services': list(self.monitoring_services.keys()),
            'active_threads': len(self.monitor_threads),
            'services_info': self.monitoring_services
        }
    
    def stop_all_monitoring(self) -> None:
        """Para todo o monitoramento"""
        try:
            services_to_stop = list(self.monitoring_services.keys())
            
            for service_name in services_to_stop:
                self.stop_monitoring(service_name)
            
            self.logger.info("📋 Todo o monitoramento de logs parado")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar todo o monitoramento: {e}")
