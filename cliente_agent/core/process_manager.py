#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Processos Quality
Monitora e controla processos relacionados aos serviços Quality
"""

import psutil
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.helpers import get_process_by_name, kill_process_by_pid, format_bytes, format_uptime

class QualityProcessManager:
    """Gerenciador de processos para serviços Quality"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.services = config.get('services', [])
        
        # Cache de processos
        self.process_cache = {}
        self.cache_lock = None
        
        self.logger.info("⚙️  Process Manager inicializado")
    
    def get_quality_processes(self) -> Dict[str, Any]:
        """
        Retorna todos os processos relacionados aos serviços Quality
        
        Returns:
            Dicionário com informações dos processos
        """
        try:
            processes = {}
            
            for service in self.services:
                if not service.get('enabled', True):
                    continue
                    
                service_name = service['name']
                service_processes = self._get_service_processes(service)
                processes[service_name] = service_processes
            
            # Adicionar processos órfãos (Quality sem serviço correspondente)
            orphan_processes = self._get_orphan_quality_processes()
            if orphan_processes:
                processes['orphan_processes'] = orphan_processes
            
            return {
                'timestamp': datetime.now().isoformat(),
                'processes': processes,
                'total_processes': sum(len(proc_list) for proc_list in processes.values() if isinstance(proc_list, list))
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter processos Quality: {e}")
            return {'error': str(e)}
    
    def _get_service_processes(self, service: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Obtém processos de um serviço específico
        
        Args:
            service: Configuração do serviço
            
        Returns:
            Lista de processos do serviço
        """
        try:
            service_name = service['name']
            display_name = service['display_name']
            executable_path = service.get('executable_path', '')
            
            # Buscar processos pelo nome do serviço
            processes = get_process_by_name(service_name)
            
            # Se não encontrou, tentar pelo nome do executável
            if not processes:
                exe_name = executable_path.split('\\')[-1] if '\\' in executable_path else executable_path
                processes = get_process_by_name(exe_name)
            
            # Formatar informações dos processos
            formatted_processes = []
            for proc in processes:
                try:
                    process_info = {
                        'pid': proc['pid'],
                        'name': proc['name'],
                        'exe': proc['exe'],
                        'status': proc['status'],
                        'create_time': proc['create_time'],
                        'uptime': format_uptime(time.time() - proc['create_time']),
                        'memory_usage': format_bytes(proc['memory_usage']),
                        'memory_bytes': proc['memory_usage'],
                        'cpu_percent': proc['cpu_percent'],
                        'service_name': service_name,
                        'display_name': display_name
                    }
                    
                    # Adicionar informações extras se possível
                    try:
                        process_obj = psutil.Process(proc['pid'])
                        process_info.update({
                            'num_threads': process_obj.num_threads(),
                            'num_handles': process_obj.num_handles() if hasattr(process_obj, 'num_handles') else None,
                            'working_set': format_bytes(process_obj.memory_info().rss),
                            'virtual_memory': format_bytes(process_obj.memory_info().vms)
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    
                    formatted_processes.append(process_info)
                    
                except Exception as e:
                    self.logger.warning(f"⚠️  Erro ao processar processo {proc.get('pid', 'unknown')}: {e}")
                    continue
            
            return formatted_processes
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter processos do serviço {service.get('name', 'unknown')}: {e}")
            return []
    
    def _get_orphan_quality_processes(self) -> List[Dict[str, Any]]:
        """
        Encontra processos Quality que não estão associados a nenhum serviço configurado
        
        Returns:
            Lista de processos órfãos
        """
        try:
            orphan_processes = []
            quality_keywords = ['quality', 'webposto', 'integra', 'fiscal', 'automacao', 'pulser']
            
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'status', 'create_time', 'memory_info', 'cpu_percent']):
                try:
                    proc_name = proc.info['name'].lower()
                    proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ''
                    
                    # Verificar se é um processo Quality
                    is_quality = any(keyword in proc_name or keyword in proc_exe for keyword in quality_keywords)
                    
                    if is_quality:
                        # Verificar se já está associado a algum serviço
                        is_associated = False
                        for service in self.services:
                            if service.get('enabled', True):
                                service_name = service['name'].lower()
                                exe_name = service.get('executable_path', '').lower()
                                
                                if (service_name in proc_name or 
                                    service_name in proc_exe or
                                    exe_name in proc_exe):
                                    is_associated = True
                                    break
                        
                        if not is_associated:
                            orphan_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'exe': proc.info['exe'],
                                'status': proc.info['status'],
                                'create_time': proc.info['create_time'],
                                'uptime': format_uptime(time.time() - proc.info['create_time']),
                                'memory_usage': format_bytes(proc.info['memory_info'].rss if proc.info['memory_info'] else 0),
                                'memory_bytes': proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                                'cpu_percent': proc.cpu_percent(),
                                'type': 'orphan'
                            })
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return orphan_processes
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao buscar processos órfãos: {e}")
            return []
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """
        Finaliza um processo por PID
        
        Args:
            pid: ID do processo
            
        Returns:
            Resultado da operação
        """
        try:
            # Verificar se o processo existe
            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except psutil.NoSuchProcess:
                return {'success': False, 'error': f'Processo {pid} não encontrado'}
            
            self.logger.info(f"🛑 Finalizando processo: {process_name} (PID: {pid})")
            
            # Tentar finalizar o processo
            success = kill_process_by_pid(pid)
            
            if success:
                self.logger.success(f"✅ Processo {process_name} (PID: {pid}) finalizado com sucesso")
                return {
                    'success': True,
                    'message': f'Processo {process_name} (PID: {pid}) finalizado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'error': f'Falha ao finalizar processo {pid}'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao finalizar processo {pid}: {e}")
            return {'success': False, 'error': str(e)}
    
    def kill_processes_by_name(self, process_name: str) -> Dict[str, Any]:
        """
        Finaliza todos os processos com um nome específico
        
        Args:
            process_name: Nome do processo
            
        Returns:
            Resultado da operação
        """
        try:
            processes = get_process_by_name(process_name)
            
            if not processes:
                return {'success': True, 'message': f'Nenhum processo {process_name} encontrado'}
            
            results = []
            for proc in processes:
                result = self.kill_process(proc['pid'])
                results.append({
                    'pid': proc['pid'],
                    'result': result
                })
            
            successful = sum(1 for r in results if r['result']['success'])
            total = len(results)
            
            return {
                'success': successful > 0,
                'message': f'Finalizados {successful}/{total} processos {process_name}',
                'details': results
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao finalizar processos {process_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_process_resource_usage(self, pid: int) -> Dict[str, Any]:
        """
        Obtém uso de recursos de um processo específico
        
        Args:
            pid: ID do processo
            
        Returns:
            Informações de uso de recursos
        """
        try:
            process = psutil.Process(pid)
            
            # Obter informações básicas
            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            
            # Obter informações de I/O se disponível
            try:
                io_counters = process.io_counters()
                io_info = {
                    'read_count': io_counters.read_count,
                    'write_count': io_counters.write_count,
                    'read_bytes': format_bytes(io_counters.read_bytes),
                    'write_bytes': format_bytes(io_counters.write_bytes)
                }
            except (psutil.AccessDenied, AttributeError):
                io_info = None
            
            # Obter informações de rede se disponível
            try:
                connections = process.connections()
                network_info = {
                    'connections_count': len(connections),
                    'connections': [
                        {
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status
                        } for conn in connections[:10]  # Limitar a 10 conexões
                    ]
                }
            except (psutil.AccessDenied, AttributeError):
                network_info = None
            
            return {
                'pid': pid,
                'name': process.name(),
                'cpu_percent': cpu_percent,
                'memory': {
                    'rss': format_bytes(memory_info.rss),
                    'vms': format_bytes(memory_info.vms),
                    'rss_bytes': memory_info.rss,
                    'vms_bytes': memory_info.vms
                },
                'io': io_info,
                'network': network_info,
                'num_threads': process.num_threads(),
                'create_time': process.create_time(),
                'uptime': format_uptime(time.time() - process.create_time())
            }
            
        except psutil.NoSuchProcess:
            return {'error': f'Processo {pid} não encontrado'}
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter recursos do processo {pid}: {e}")
            return {'error': str(e)}
    
    def get_system_resource_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo de uso de recursos do sistema
        
        Returns:
            Resumo de recursos do sistema
        """
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memória
            memory = psutil.virtual_memory()
            
            # Disco
            disk = psutil.disk_usage('/')
            
            # Processos Quality
            quality_processes = self.get_quality_processes()
            total_quality_memory = 0
            
            for service_name, processes in quality_processes.get('processes', {}).items():
                if isinstance(processes, list):
                    for proc in processes:
                        total_quality_memory += proc.get('memory_bytes', 0)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'total': format_bytes(memory.total),
                    'available': format_bytes(memory.available),
                    'used': format_bytes(memory.used),
                    'percent': memory.percent
                },
                'disk': {
                    'total': format_bytes(disk.total),
                    'used': format_bytes(disk.used),
                    'free': format_bytes(disk.free),
                    'percent': (disk.used / disk.total) * 100
                },
                'quality_processes': {
                    'total_memory': format_bytes(total_quality_memory),
                    'total_memory_bytes': total_quality_memory,
                    'count': quality_processes.get('total_processes', 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter resumo de recursos: {e}")
            return {'error': str(e)}
