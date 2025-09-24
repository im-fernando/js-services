#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Sessões Multi-Atendente
Gerencia sessões simultâneas e controle de conflitos
"""

import time
import threading
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta

class SessionManager:
    """Gerenciador de sessões para múltiplos atendentes"""
    
    def __init__(self, logger):
        self.logger = logger
        self.active_sessions = {}  # {session_id: SessionInfo}
        self.client_locks = {}     # {client_id: LockInfo}
        self.session_lock = threading.Lock()
        self.client_lock = threading.Lock()
        
        # Configurações
        self.session_timeout = 3600  # 1 hora
        self.client_lock_timeout = 300  # 5 minutos
        
        self.logger.info("🔐 Session Manager inicializado")
    
    def create_session(self, attendant_id: str, attendant_name: str, websocket) -> str:
        """
        Cria uma nova sessão para um atendente
        
        Args:
            attendant_id: ID do atendente
            attendant_name: Nome do atendente
            websocket: Conexão WebSocket
            
        Returns:
            ID da sessão criada
        """
        try:
            with self.session_lock:
                session_id = f"SES_{attendant_id}_{int(time.time())}"
                
                session_info = {
                    "session_id": session_id,
                    "attendant_id": attendant_id,
                    "attendant_name": attendant_name,
                    "websocket": websocket,
                    "login_time": datetime.now(),
                    "last_activity": datetime.now(),
                    "current_client": None,
                    "active_commands": [],
                    "status": "active"
                }
                
                self.active_sessions[session_id] = session_info
                
                self.logger.info(f"🔐 Nova sessão criada: {attendant_name} ({session_id})")
                return session_id
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar sessão: {e}")
            return None
    
    def close_session(self, session_id: str) -> bool:
        """
        Fecha uma sessão
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se fechou com sucesso
        """
        try:
            with self.session_lock:
                if session_id not in self.active_sessions:
                    return False
                
                session = self.active_sessions[session_id]
                attendant_name = session["attendant_name"]
                
                # Liberar cliente se estiver bloqueado
                if session["current_client"]:
                    self.unlock_client(session["current_client"], session_id)
                
                # Remover sessão
                del self.active_sessions[session_id]
                
                self.logger.info(f"🔐 Sessão fechada: {attendant_name} ({session_id})")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao fechar sessão: {e}")
            return False
    
    def update_session_activity(self, session_id: str) -> bool:
        """
        Atualiza última atividade de uma sessão
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se atualizou com sucesso
        """
        try:
            with self.session_lock:
                if session_id in self.active_sessions:
                    self.active_sessions[session_id]["last_activity"] = datetime.now()
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar atividade da sessão: {e}")
            return False
    
    def set_current_client(self, session_id: str, client_id: str) -> bool:
        """
        Define cliente atual de uma sessão
        
        Args:
            session_id: ID da sessão
            client_id: ID do cliente
            
        Returns:
            True se definiu com sucesso
        """
        try:
            with self.session_lock:
                if session_id in self.active_sessions:
                    self.active_sessions[session_id]["current_client"] = client_id
                    self.active_sessions[session_id]["last_activity"] = datetime.now()
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao definir cliente atual: {e}")
            return False
    
    def add_active_command(self, session_id: str, command: str) -> bool:
        """
        Adiciona comando ativo a uma sessão
        
        Args:
            session_id: ID da sessão
            command: Comando sendo executado
            
        Returns:
            True se adicionou com sucesso
        """
        try:
            with self.session_lock:
                if session_id in self.active_sessions:
                    self.active_sessions[session_id]["active_commands"].append({
                        "command": command,
                        "start_time": datetime.now()
                    })
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao adicionar comando ativo: {e}")
            return False
    
    def remove_active_command(self, session_id: str, command: str) -> bool:
        """
        Remove comando ativo de uma sessão
        
        Args:
            session_id: ID da sessão
            command: Comando a remover
            
        Returns:
            True se removeu com sucesso
        """
        try:
            with self.session_lock:
                if session_id in self.active_sessions:
                    commands = self.active_sessions[session_id]["active_commands"]
                    self.active_sessions[session_id]["active_commands"] = [
                        cmd for cmd in commands if cmd["command"] != command
                    ]
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao remover comando ativo: {e}")
            return False
    
    def lock_client_for_action(self, client_id: str, session_id: str, action: str) -> Tuple[bool, str]:
        """
        Bloqueia um cliente para uma ação específica
        
        Args:
            client_id: ID do cliente
            session_id: ID da sessão
            action: Ação sendo executada
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            with self.client_lock:
                # Verificar se cliente já está bloqueado
                if client_id in self.client_locks:
                    lock_info = self.client_locks[client_id]
                    if lock_info["session_id"] != session_id:
                        # Cliente bloqueado por outra sessão
                        attendant_name = self.get_attendant_name_by_session(lock_info["session_id"])
                        return False, f"Cliente bloqueado por {attendant_name} ({lock_info['action']})"
                
                # Obter informações da sessão
                session = self.get_session_info(session_id)
                if not session:
                    return False, "Sessão não encontrada"
                
                # Bloquear cliente
                self.client_locks[client_id] = {
                    "session_id": session_id,
                    "attendant_id": session["attendant_id"],
                    "attendant_name": session["attendant_name"],
                    "action": action,
                    "lock_time": datetime.now()
                }
                
                # Atualizar cliente atual da sessão
                self.set_current_client(session_id, client_id)
                
                self.logger.info(f"🔒 Cliente {client_id} bloqueado por {session['attendant_name']} para {action}")
                return True, "Cliente bloqueado com sucesso"
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao bloquear cliente: {e}")
            return False, f"Erro ao bloquear cliente: {e}"
    
    def unlock_client(self, client_id: str, session_id: str = None) -> bool:
        """
        Desbloqueia um cliente
        
        Args:
            client_id: ID do cliente
            session_id: ID da sessão (opcional, para verificação)
            
        Returns:
            True se desbloqueou com sucesso
        """
        try:
            with self.client_lock:
                if client_id not in self.client_locks:
                    return True  # Já está desbloqueado
                
                lock_info = self.client_locks[client_id]
                
                # Verificar se a sessão tem permissão para desbloquear
                if session_id and lock_info["session_id"] != session_id:
                    return False  # Outra sessão bloqueou
                
                # Desbloquear
                attendant_name = lock_info["attendant_name"]
                del self.client_locks[client_id]
                
                self.logger.info(f"🔓 Cliente {client_id} desbloqueado (era de {attendant_name})")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao desbloquear cliente: {e}")
            return False
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de uma sessão
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Informações da sessão ou None
        """
        try:
            with self.session_lock:
                return self.active_sessions.get(session_id)
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter informações da sessão: {e}")
            return None
    
    def get_attendant_name_by_session(self, session_id: str) -> str:
        """
        Obtém nome do atendente por sessão
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Nome do atendente ou "Desconhecido"
        """
        session = self.get_session_info(session_id)
        return session["attendant_name"] if session else "Desconhecido"
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """
        Obtém lista de todas as sessões ativas
        
        Returns:
            Lista de sessões
        """
        try:
            with self.session_lock:
                sessions = []
                for session_id, session_info in self.active_sessions.items():
                    session_data = {
                        "session_id": session_id,
                        "attendant_id": session_info["attendant_id"],
                        "attendant_name": session_info["attendant_name"],
                        "login_time": session_info["login_time"].isoformat(),
                        "last_activity": session_info["last_activity"].isoformat(),
                        "current_client": session_info["current_client"],
                        "active_commands": len(session_info["active_commands"]),
                        "status": session_info["status"]
                    }
                    sessions.append(session_data)
                
                return sessions
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter sessões: {e}")
            return []
    
    def get_client_lock_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de bloqueio de um cliente
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Informações de bloqueio ou None
        """
        try:
            with self.client_lock:
                if client_id not in self.client_locks:
                    return None
                
                lock_info = self.client_locks[client_id]
                return {
                    "client_id": client_id,
                    "session_id": lock_info["session_id"],
                    "attendant_id": lock_info["attendant_id"],
                    "attendant_name": lock_info["attendant_name"],
                    "action": lock_info["action"],
                    "lock_time": lock_info["lock_time"].isoformat(),
                    "duration": str(datetime.now() - lock_info["lock_time"])
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter informações de bloqueio: {e}")
            return None
    
    def get_available_clients(self, all_clients: List[str]) -> List[str]:
        """
        Obtém lista de clientes disponíveis (não bloqueados)
        
        Args:
            all_clients: Lista de todos os clientes
            
        Returns:
            Lista de clientes disponíveis
        """
        try:
            with self.client_lock:
                locked_clients = set(self.client_locks.keys())
                return [client for client in all_clients if client not in locked_clients]
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter clientes disponíveis: {e}")
            return all_clients
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove sessões expiradas
        
        Returns:
            Número de sessões removidas
        """
        try:
            cutoff_time = datetime.now() - timedelta(seconds=self.session_timeout)
            removed_count = 0
            
            with self.session_lock:
                sessions_to_remove = []
                
                for session_id, session_info in self.active_sessions.items():
                    if session_info["last_activity"] < cutoff_time:
                        sessions_to_remove.append(session_id)
                
                for session_id in sessions_to_remove:
                    session = self.active_sessions[session_id]
                    attendant_name = session["attendant_name"]
                    
                    # Liberar cliente se bloqueado
                    if session["current_client"]:
                        self.unlock_client(session["current_client"], session_id)
                    
                    del self.active_sessions[session_id]
                    removed_count += 1
                    
                    self.logger.warning(f"⚠️  Sessão expirada removida: {attendant_name} ({session_id})")
            
            if removed_count > 0:
                self.logger.info(f"🧹 Removidas {removed_count} sessões expiradas")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar sessões expiradas: {e}")
            return 0
    
    def cleanup_expired_locks(self) -> int:
        """
        Remove bloqueios expirados
        
        Returns:
            Número de bloqueios removidos
        """
        try:
            cutoff_time = datetime.now() - timedelta(seconds=self.client_lock_timeout)
            removed_count = 0
            
            with self.client_lock:
                locks_to_remove = []
                
                for client_id, lock_info in self.client_locks.items():
                    if lock_info["lock_time"] < cutoff_time:
                        locks_to_remove.append(client_id)
                
                for client_id in locks_to_remove:
                    lock_info = self.client_locks[client_id]
                    attendant_name = lock_info["attendant_name"]
                    
                    del self.client_locks[client_id]
                    removed_count += 1
                    
                    self.logger.warning(f"⚠️  Bloqueio expirado removido: {client_id} (era de {attendant_name})")
            
            if removed_count > 0:
                self.logger.info(f"🧹 Removidos {removed_count} bloqueios expirados")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar bloqueios expirados: {e}")
            return 0
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas das sessões
        
        Returns:
            Estatísticas das sessões
        """
        try:
            with self.session_lock:
                total_sessions = len(self.active_sessions)
                
                # Contar por papel (se disponível)
                roles_count = {}
                for session in self.active_sessions.values():
                    # Aqui seria necessário acessar informações do usuário
                    # Por simplicidade, vamos contar apenas o total
                    pass
                
                # Contar clientes bloqueados
                with self.client_lock:
                    locked_clients = len(self.client_locks)
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "total_sessions": total_sessions,
                    "locked_clients": locked_clients,
                    "available_clients": "N/A",  # Seria calculado com lista de clientes
                    "sessions": self.get_all_sessions()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas das sessões: {e}")
            return {"error": str(e)}
