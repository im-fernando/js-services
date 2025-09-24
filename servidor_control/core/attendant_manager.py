#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Atendentes
Gerencia informações e atividades dos atendentes conectados
"""

import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from utils.auth import QualityAuthManager

class AttendantManager:
    """Gerenciador de atendentes conectados"""
    
    def __init__(self, config: Dict[str, Any], logger):
        self.config = config
        self.logger = logger
        self.auth_manager = QualityAuthManager()
        
        # Armazenamento de atendentes ativos
        self.active_attendants = {}  # {attendant_id: AttendantInfo}
        self.attendant_lock = threading.Lock()
        
        # Estatísticas
        self.total_logins = 0
        self.total_logouts = 0
        
        self.logger.info("👥 Attendant Manager inicializado")
    
    def login_attendant(self, username: str, password: str, websocket) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Realiza login de um atendente
        
        Args:
            username: Nome de usuário
            password: Senha
            websocket: Conexão WebSocket
            
        Returns:
            Tupla (sucesso, dados_atendente, mensagem)
        """
        try:
            # Autenticar usuário
            success, user_data, message = self.auth_manager.authenticate_user(username, password)
            
            if not success:
                self.logger.warning(f"⚠️  Tentativa de login falhada: {username} - {message}")
                return False, None, message
            
            attendant_id = user_data["id"]
            
            # Verificar se já está logado
            with self.attendant_lock:
                if attendant_id in self.active_attendants:
                    return False, None, "Atendente já está logado em outra sessão"
                
                # Registrar atendente ativo
                self.active_attendants[attendant_id] = {
                    "attendant_id": attendant_id,
                    "username": user_data["username"],
                    "display_name": user_data["display_name"],
                    "role": user_data["role"],
                    "permissions": user_data["permissions"],
                    "assigned_clients": user_data["assigned_clients"],
                    "websocket": websocket,
                    "login_time": datetime.now(),
                    "last_activity": datetime.now(),
                    "current_client": None,
                    "commands_executed": 0,
                    "status": "active"
                }
                
                self.total_logins += 1
                
                self.logger.info(f"👤 Atendente logado: {user_data['display_name']} ({attendant_id})")
                
                return True, user_data, message
                
        except Exception as e:
            self.logger.error(f"❌ Erro no login do atendente: {e}")
            return False, None, f"Erro no login: {e}"
    
    def logout_attendant(self, attendant_id: str) -> bool:
        """
        Realiza logout de um atendente
        
        Args:
            attendant_id: ID do atendente
            
        Returns:
            True se fez logout com sucesso
        """
        try:
            with self.attendant_lock:
                if attendant_id not in self.active_attendants:
                    return False
                
                attendant_info = self.active_attendants[attendant_id]
                display_name = attendant_info["display_name"]
                
                # Remover atendente
                del self.active_attendants[attendant_id]
                self.total_logouts += 1
                
                self.logger.info(f"👤 Atendente deslogado: {display_name} ({attendant_id})")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Erro no logout do atendente: {e}")
            return False
    
    def update_attendant_activity(self, attendant_id: str) -> bool:
        """
        Atualiza última atividade de um atendente
        
        Args:
            attendant_id: ID do atendente
            
        Returns:
            True se atualizou com sucesso
        """
        try:
            with self.attendant_lock:
                if attendant_id in self.active_attendants:
                    self.active_attendants[attendant_id]["last_activity"] = datetime.now()
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar atividade do atendente: {e}")
            return False
    
    def set_attendant_current_client(self, attendant_id: str, client_id: str) -> bool:
        """
        Define cliente atual de um atendente
        
        Args:
            attendant_id: ID do atendente
            client_id: ID do cliente
            
        Returns:
            True se definiu com sucesso
        """
        try:
            with self.attendant_lock:
                if attendant_id in self.active_attendants:
                    self.active_attendants[attendant_id]["current_client"] = client_id
                    self.active_attendants[attendant_id]["last_activity"] = datetime.now()
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao definir cliente atual do atendente: {e}")
            return False
    
    def increment_commands_executed(self, attendant_id: str) -> bool:
        """
        Incrementa contador de comandos executados
        
        Args:
            attendant_id: ID do atendente
            
        Returns:
            True se incrementou com sucesso
        """
        try:
            with self.attendant_lock:
                if attendant_id in self.active_attendants:
                    self.active_attendants[attendant_id]["commands_executed"] += 1
                    self.active_attendants[attendant_id]["last_activity"] = datetime.now()
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao incrementar comandos do atendente: {e}")
            return False
    
    def get_attendant_info(self, attendant_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um atendente
        
        Args:
            attendant_id: ID do atendente
            
        Returns:
            Informações do atendente ou None
        """
        try:
            with self.attendant_lock:
                attendant = self.active_attendants.get(attendant_id)
                if not attendant:
                    return None
                
                # Retornar cópia sem websocket
                attendant_info = attendant.copy()
                del attendant_info["websocket"]
                
                return attendant_info
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter informações do atendente: {e}")
            return None
    
    def get_attendant_websocket(self, attendant_id: str):
        """
        Obtém WebSocket de um atendente
        
        Args:
            attendant_id: ID do atendente
            
        Returns:
            WebSocket ou None
        """
        try:
            with self.attendant_lock:
                attendant = self.active_attendants.get(attendant_id)
                return attendant["websocket"] if attendant else None
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter WebSocket do atendente: {e}")
            return None
    
    def get_all_active_attendants(self) -> List[Dict[str, Any]]:
        """
        Obtém lista de todos os atendentes ativos
        
        Returns:
            Lista de atendentes ativos
        """
        try:
            with self.attendant_lock:
                attendants = []
                for attendant_id, attendant_info in self.active_attendants.items():
                    attendant_data = {
                        "attendant_id": attendant_id,
                        "username": attendant_info["username"],
                        "display_name": attendant_info["display_name"],
                        "role": attendant_info["role"],
                        "login_time": attendant_info["login_time"].isoformat(),
                        "last_activity": attendant_info["last_activity"].isoformat(),
                        "current_client": attendant_info["current_client"],
                        "commands_executed": attendant_info["commands_executed"],
                        "status": attendant_info["status"]
                    }
                    attendants.append(attendant_data)
                
                return attendants
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter atendentes ativos: {e}")
            return []
    
    def can_attendant_access_client(self, attendant_id: str, client_id: str) -> bool:
        """
        Verifica se atendente pode acessar um cliente
        
        Args:
            attendant_id: ID do atendente
            client_id: ID do cliente
            
        Returns:
            True se pode acessar
        """
        try:
            attendant_info = self.get_attendant_info(attendant_id)
            if not attendant_info:
                return False
            
            assigned_clients = attendant_info.get("assigned_clients", [])
            
            # Se tem acesso a todos os clientes
            if "*" in assigned_clients:
                return True
            
            # Verificar se o cliente está na lista
            return client_id in assigned_clients
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar acesso do atendente: {e}")
            return False
    
    def can_attendant_perform_action(self, attendant_id: str, action: str, client_id: str = None) -> Tuple[bool, str]:
        """
        Verifica se atendente pode executar uma ação
        
        Args:
            attendant_id: ID do atendente
            action: Ação a executar
            client_id: ID do cliente (opcional)
            
        Returns:
            Tupla (pode_executar, mensagem)
        """
        try:
            attendant_info = self.get_attendant_info(attendant_id)
            if not attendant_info:
                return False, "Atendente não encontrado"
            
            # Verificar acesso ao cliente
            if client_id and not self.can_attendant_access_client(attendant_id, client_id):
                return False, f"Sem permissão para acessar cliente {client_id}"
            
            # Verificar permissões específicas
            return self.auth_manager.can_perform_action(attendant_id, action, client_id)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar permissão do atendente: {e}")
            return False, f"Erro na verificação: {e}"
    
    def get_attendants_by_client(self, client_id: str) -> List[Dict[str, Any]]:
        """
        Obtém atendentes que podem acessar um cliente específico
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Lista de atendentes
        """
        try:
            with self.attendant_lock:
                authorized_attendants = []
                
                for attendant_id, attendant_info in self.active_attendants.items():
                    if self.can_attendant_access_client(attendant_id, client_id):
                        attendant_data = {
                            "attendant_id": attendant_id,
                            "display_name": attendant_info["display_name"],
                            "role": attendant_info["role"],
                            "current_client": attendant_info["current_client"]
                        }
                        authorized_attendants.append(attendant_data)
                
                return authorized_attendants
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter atendentes por cliente: {e}")
            return []
    
    def get_attendant_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas dos atendentes
        
        Returns:
            Estatísticas dos atendentes
        """
        try:
            with self.attendant_lock:
                total_attendants = len(self.active_attendants)
                
                # Contar por papel
                roles_count = {}
                for attendant_info in self.active_attendants.values():
                    role = attendant_info["role"]
                    roles_count[role] = roles_count.get(role, 0) + 1
                
                # Calcular tempo médio de sessão
                total_session_time = 0
                for attendant_info in self.active_attendants.values():
                    session_duration = datetime.now() - attendant_info["login_time"]
                    total_session_time += session_duration.total_seconds()
                
                avg_session_time = total_session_time / total_attendants if total_attendants > 0 else 0
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "total_active_attendants": total_attendants,
                    "total_logins": self.total_logins,
                    "total_logouts": self.total_logouts,
                    "roles_distribution": roles_count,
                    "average_session_time_minutes": round(avg_session_time / 60, 2),
                    "attendants": self.get_all_active_attendants()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas dos atendentes: {e}")
            return {"error": str(e)}
    
    def cleanup_inactive_attendants(self, timeout_minutes: int = 60) -> int:
        """
        Remove atendentes inativos
        
        Args:
            timeout_minutes: Timeout em minutos
            
        Returns:
            Número de atendentes removidos
        """
        try:
            cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
            removed_count = 0
            
            with self.attendant_lock:
                attendants_to_remove = []
                
                for attendant_id, attendant_info in self.active_attendants.items():
                    if attendant_info["last_activity"] < cutoff_time:
                        attendants_to_remove.append(attendant_id)
                
                for attendant_id in attendants_to_remove:
                    attendant_info = self.active_attendants[attendant_id]
                    display_name = attendant_info["display_name"]
                    
                    del self.active_attendants[attendant_id]
                    removed_count += 1
                    
                    self.logger.warning(f"⚠️  Atendente inativo removido: {display_name} ({attendant_id})")
            
            if removed_count > 0:
                self.logger.info(f"🧹 Removidos {removed_count} atendentes inativos")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar atendentes inativos: {e}")
            return 0
    
    def send_notification_to_attendant(self, attendant_id: str, notification: Dict[str, Any]) -> bool:
        """
        Envia notificação para um atendente específico
        
        Args:
            attendant_id: ID do atendente
            notification: Dados da notificação
            
        Returns:
            True se enviou com sucesso
        """
        try:
            websocket = self.get_attendant_websocket(attendant_id)
            if not websocket:
                return False
            
            # Aqui seria implementado o envio via WebSocket
            # Por enquanto, apenas log
            self.logger.info(f"📢 Notificação enviada para {attendant_id}: {notification.get('type', 'unknown')}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar notificação: {e}")
            return False
    
    def broadcast_notification(self, notification: Dict[str, Any], exclude_attendant: str = None) -> int:
        """
        Envia notificação para todos os atendentes ativos
        
        Args:
            notification: Dados da notificação
            exclude_attendant: ID do atendente a excluir
            
        Returns:
            Número de atendentes que receberam a notificação
        """
        try:
            sent_count = 0
            
            with self.attendant_lock:
                for attendant_id in self.active_attendants.keys():
                    if exclude_attendant and attendant_id == exclude_attendant:
                        continue
                    
                    if self.send_notification_to_attendant(attendant_id, notification):
                        sent_count += 1
            
            self.logger.info(f"📢 Notificação broadcast enviada para {sent_count} atendentes")
            return sent_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro no broadcast de notificação: {e}")
            return 0
