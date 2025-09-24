#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Clientes Quality
Gerencia conexões e informações dos clientes conectados
"""

import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from utils.helpers import format_client_name, calculate_uptime_percentage, get_health_status

class QualityClientManager:
    """Gerenciador de clientes conectados"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.quality_services = config.get('quality_services', {})
        
        # Armazenamento de clientes
        self.clients = {}  # client_id -> client_info
        self.client_lock = threading.Lock()
        
        # Estatísticas
        self.total_connections = 0
        self.total_disconnections = 0
        
        self.logger.info("👥 Client Manager inicializado")
    
    def add_client(self, client_handler, client_id: str) -> None:
        """
        Adiciona um novo cliente
        
        Args:
            client_handler: Handler do cliente WebSocket
            client_id: ID do cliente
        """
        try:
            with self.client_lock:
                self.clients[client_id] = {
                    'handler': client_handler,
                    'client_id': client_id,
                    'real_client_id': None,
                    'name': 'Unknown Client',
                    'location': 'Unknown',
                    'version': '1.0.0',
                    'capabilities': [],
                    'system_info': {},
                    'installed_services': [],
                    'status': {},
                    'connected_at': datetime.now().isoformat(),
                    'last_activity': datetime.now().isoformat(),
                    'last_heartbeat': datetime.now().isoformat()
                }
                
                self.total_connections += 1
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar cliente {client_id}: {e}")
    
    def remove_client(self, client_id: str) -> None:
        """
        Remove um cliente
        
        Args:
            client_id: ID do cliente
        """
        try:
            with self.client_lock:
                if client_id in self.clients:
                    del self.clients[client_id]
                    self.total_disconnections += 1
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao remover cliente {client_id}: {e}")
    
    def update_client_info(self, client_id: str, info: Dict[str, Any]) -> None:
        """
        Atualiza informações de um cliente
        
        Args:
            client_id: ID do cliente
            info: Informações para atualizar
        """
        try:
            with self.client_lock:
                if client_id in self.clients:
                    self.clients[client_id].update(info)
                    self.clients[client_id]['last_activity'] = datetime.now().isoformat()
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar informações do cliente {client_id}: {e}")
    
    def update_client_status(self, client_id: str, status: Dict[str, Any]) -> None:
        """
        Atualiza status de um cliente
        
        Args:
            client_id: ID do cliente
            status: Status para atualizar
        """
        try:
            with self.client_lock:
                if client_id in self.clients:
                    self.clients[client_id]['status'] = status
                    self.clients[client_id]['last_activity'] = datetime.now().isoformat()
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar status do cliente {client_id}: {e}")
    
    def update_client_activity(self, client_id: str) -> None:
        """
        Atualiza última atividade de um cliente
        
        Args:
            client_id: ID do cliente
        """
        try:
            with self.client_lock:
                if client_id in self.clients:
                    now = datetime.now().isoformat()
                    self.clients[client_id]['last_activity'] = now
                    self.clients[client_id]['last_heartbeat'] = now
                    
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar atividade do cliente {client_id}: {e}")
    
    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um cliente
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Informações do cliente ou None
        """
        try:
            with self.client_lock:
                return self.clients.get(client_id)
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter cliente {client_id}: {e}")
            return None
    
    def get_client_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações básicas de um cliente
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Informações básicas do cliente ou None
        """
        try:
            client = self.get_client(client_id)
            if not client:
                return None
            
            return {
                'client_id': client.get('real_client_id', client_id),
                'name': client.get('name', 'Unknown Client'),
                'location': client.get('location', 'Unknown'),
                'version': client.get('version', '1.0.0'),
                'connected_at': client.get('connected_at'),
                'last_activity': client.get('last_activity'),
                'capabilities': client.get('capabilities', [])
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter informações do cliente {client_id}: {e}")
            return None
    
    def get_all_clients(self) -> List[str]:
        """
        Retorna lista de IDs de todos os clientes
        
        Returns:
            Lista de IDs de clientes
        """
        try:
            with self.client_lock:
                return list(self.clients.keys())
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter lista de clientes: {e}")
            return []
    
    def get_clients_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo de todos os clientes
        
        Returns:
            Resumo dos clientes
        """
        try:
            with self.client_lock:
                clients_list = []
                
                for client_id, client in self.clients.items():
                    # Informações básicas
                    client_summary = {
                        'client_id': client.get('real_client_id', client_id),
                        'name': client.get('name', 'Unknown Client'),
                        'location': client.get('location', 'Unknown'),
                        'version': client.get('version', '1.0.0'),
                        'connected_at': client.get('connected_at'),
                        'last_activity': client.get('last_activity'),
                        'capabilities': client.get('capabilities', [])
                    }
                    
                    # Status dos serviços
                    services_status = client.get('status', {}).get('services', {})
                    if services_status:
                        client_summary['services'] = {
                            'total': len(services_status),
                            'running': sum(1 for s in services_status.values() 
                                          if isinstance(s, dict) and s.get('status') == 'running'),
                            'stopped': sum(1 for s in services_status.values() 
                                          if isinstance(s, dict) and s.get('status') == 'stopped'),
                            'uptime_percentage': calculate_uptime_percentage(services_status),
                            'health_status': get_health_status(services_status, self.quality_services)
                        }
                    
                    # Informações do sistema
                    system_info = client.get('system_info', {})
                    if system_info:
                        client_summary['system'] = {
                            'platform': system_info.get('platform', 'Unknown'),
                            'hostname': system_info.get('hostname', 'Unknown'),
                            'cpu_count': system_info.get('cpu_count', 0),
                            'memory_total': system_info.get('memory_total', 0)
                        }
                    
                    clients_list.append(client_summary)
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_clients': len(clients_list),
                    'total_connections': self.total_connections,
                    'total_disconnections': self.total_disconnections,
                    'clients': clients_list
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter resumo dos clientes: {e}")
            return {'error': str(e)}
    
    def get_client_services_status(self, client_id: str) -> Dict[str, Any]:
        """
        Obtém status dos serviços de um cliente
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Status dos serviços
        """
        try:
            client = self.get_client(client_id)
            if not client:
                return {'error': f'Cliente {client_id} não encontrado'}
            
            services_status = client.get('status', {}).get('services', {})
            
            return {
                'client_id': client.get('real_client_id', client_id),
                'client_name': client.get('name', 'Unknown Client'),
                'timestamp': client.get('last_activity'),
                'services': services_status,
                'summary': {
                    'total': len(services_status),
                    'running': sum(1 for s in services_status.values() 
                                  if isinstance(s, dict) and s.get('status') == 'running'),
                    'stopped': sum(1 for s in services_status.values() 
                                  if isinstance(s, dict) and s.get('status') == 'stopped'),
                    'uptime_percentage': calculate_uptime_percentage(services_status),
                    'health_status': get_health_status(services_status, self.quality_services)
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter status dos serviços do cliente {client_id}: {e}")
            return {'error': str(e)}
    
    def cleanup_inactive_clients(self, timeout_seconds: int = 60) -> int:
        """
        Remove clientes inativos
        
        Args:
            timeout_seconds: Timeout em segundos
            
        Returns:
            Número de clientes removidos
        """
        try:
            cutoff_time = datetime.now() - timedelta(seconds=timeout_seconds)
            removed_count = 0
            
            with self.client_lock:
                clients_to_remove = []
                
                for client_id, client in self.clients.items():
                    last_activity_str = client.get('last_activity')
                    if last_activity_str:
                        try:
                            last_activity = datetime.fromisoformat(last_activity_str)
                            if last_activity < cutoff_time:
                                clients_to_remove.append(client_id)
                        except Exception:
                            # Se não conseguir parsear a data, considerar inativo
                            clients_to_remove.append(client_id)
                
                # Remover clientes inativos
                for client_id in clients_to_remove:
                    client_name = self.clients[client_id].get('name', 'Unknown')
                    self.logger.warning(f"⚠️  Removendo cliente inativo: {client_name} ({client_id})")
                    del self.clients[client_id]
                    removed_count += 1
            
            if removed_count > 0:
                self.logger.info(f"🧹 Removidos {removed_count} clientes inativos")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar clientes inativos: {e}")
            return 0
    
    def disconnect_all_clients(self) -> None:
        """Desconecta todos os clientes"""
        try:
            with self.client_lock:
                for client_id, client in self.clients.items():
                    try:
                        handler = client.get('handler')
                        if handler:
                            handler.close()
                    except Exception as e:
                        self.logger.error(f"❌ Erro ao desconectar cliente {client_id}: {e}")
                
                self.clients.clear()
                
            self.logger.info("🔌 Todos os clientes desconectados")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao desconectar todos os clientes: {e}")
    
    def get_client_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas dos clientes
        
        Returns:
            Estatísticas dos clientes
        """
        try:
            with self.client_lock:
                total_clients = len(self.clients)
                
                # Contar clientes por localização
                locations = {}
                for client in self.clients.values():
                    location = client.get('location', 'Unknown')
                    locations[location] = locations.get(location, 0) + 1
                
                # Contar clientes por versão
                versions = {}
                for client in self.clients.values():
                    version = client.get('version', 'Unknown')
                    versions[version] = versions.get(version, 0) + 1
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'total_clients': total_clients,
                    'total_connections': self.total_connections,
                    'total_disconnections': self.total_disconnections,
                    'locations': locations,
                    'versions': versions,
                    'active_clients': total_clients
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas dos clientes: {e}")
            return {'error': str(e)}
