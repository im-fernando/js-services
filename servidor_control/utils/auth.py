#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Autenticação para Quality Control Panel
"""

import hashlib
import json
import os
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

class QualityAuthManager:
    """Gerenciador de autenticação para atendentes"""
    
    def __init__(self, config_path: str = "config/users_config.json"):
        self.config_path = config_path
        self.users_config = self._load_users_config()
    
    def _load_users_config(self) -> Dict[str, Any]:
        """Carrega configuração de usuários"""
        try:
            if not os.path.exists(self.config_path):
                return self._create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"❌ Erro ao carregar configuração de usuários: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Cria configuração padrão de usuários"""
        default_config = {
            "attendants": [
                {
                    "id": "ATD001",
                    "username": "admin",
                    "display_name": "Administrador",
                    "password_hash": self._hash_password("admin123"),
                    "role": "administrator",
                    "permissions": {
                        "can_restart_services": True,
                        "can_kill_processes": True,
                        "can_view_logs": True,
                        "can_manage_all_clients": True,
                        "can_perform_critical_actions": True,
                        "can_manage_attendants": True,
                        "can_view_all_sessions": True
                    },
                    "assigned_clients": ["*"],
                    "shift": "any",
                    "created_at": datetime.now().isoformat()
                }
            ],
            "roles": {
                "administrator": {
                    "description": "Acesso total ao sistema",
                    "level": 3
                },
                "senior_support": {
                    "description": "Suporte sênior com acesso amplo",
                    "level": 2
                },
                "junior_support": {
                    "description": "Suporte júnior com acesso limitado",
                    "level": 1
                }
            },
            "default_password": "quality123"
        }
        
        # Salvar configuração padrão
        self._save_users_config(default_config)
        return default_config
    
    def _save_users_config(self, config: Dict[str, Any]) -> None:
        """Salva configuração de usuários"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar configuração de usuários: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Gera hash SHA-256 da senha"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Autentica um usuário
        
        Args:
            username: Nome de usuário
            password: Senha
            
        Returns:
            Tupla (sucesso, dados_usuário, mensagem)
        """
        try:
            # Buscar usuário
            user = self._find_user_by_username(username)
            if not user:
                return False, None, "Usuário não encontrado"
            
            # Verificar senha
            password_hash = self._hash_password(password)
            if user["password_hash"] != password_hash:
                return False, None, "Senha incorreta"
            
            # Remover hash da senha dos dados retornados
            user_data = user.copy()
            del user_data["password_hash"]
            
            return True, user_data, "Login realizado com sucesso"
            
        except Exception as e:
            return False, None, f"Erro na autenticação: {e}"
    
    def _find_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Encontra usuário pelo nome de usuário"""
        for attendant in self.users_config.get("attendants", []):
            if attendant["username"] == username:
                return attendant
        return None
    
    def _find_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Encontra usuário pelo ID"""
        for attendant in self.users_config.get("attendants", []):
            if attendant["id"] == user_id:
                return attendant
        return None
    
    def get_user_permissions(self, user_id: str) -> Dict[str, bool]:
        """
        Obtém permissões de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário de permissões
        """
        user = self._find_user_by_id(user_id)
        if not user:
            return {}
        
        return user.get("permissions", {})
    
    def can_access_client(self, user_id: str, client_id: str) -> bool:
        """
        Verifica se usuário pode acessar um cliente específico
        
        Args:
            user_id: ID do usuário
            client_id: ID do cliente
            
        Returns:
            True se pode acessar
        """
        user = self._find_user_by_id(user_id)
        if not user:
            return False
        
        assigned_clients = user.get("assigned_clients", [])
        
        # Se tem acesso a todos os clientes
        if "*" in assigned_clients:
            return True
        
        # Verificar se o cliente está na lista
        return client_id in assigned_clients
    
    def can_perform_action(self, user_id: str, action: str, client_id: str = None) -> Tuple[bool, str]:
        """
        Verifica se usuário pode executar uma ação
        
        Args:
            user_id: ID do usuário
            action: Ação a executar
            client_id: ID do cliente (opcional)
            
        Returns:
            Tupla (pode_executar, mensagem)
        """
        try:
            user = self._find_user_by_id(user_id)
            if not user:
                return False, "Usuário não encontrado"
            
            # Verificar acesso ao cliente
            if client_id and not self.can_access_client(user_id, client_id):
                return False, f"Sem permissão para acessar cliente {client_id}"
            
            # Mapear ações para permissões
            permission_map = {
                "restart_service": "can_restart_services",
                "stop_service": "can_restart_services",
                "start_service": "can_restart_services",
                "restart_all_services": "can_restart_services",
                "kill_process": "can_kill_processes",
                "get_logs": "can_view_logs",
                "start_log_monitoring": "can_view_logs",
                "stop_log_monitoring": "can_view_logs",
                "critical_action": "can_perform_critical_actions"
            }
            
            required_permission = permission_map.get(action)
            if not required_permission:
                return True, "Ação permitida"  # Ação não requer permissão especial
            
            permissions = user.get("permissions", {})
            if not permissions.get(required_permission, False):
                return False, f"Sem permissão para executar: {action}"
            
            return True, "Permissão concedida"
            
        except Exception as e:
            return False, f"Erro na verificação de permissão: {e}"
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um usuário (sem senha)
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Informações do usuário ou None
        """
        user = self._find_user_by_id(user_id)
        if not user:
            return None
        
        # Remover informações sensíveis
        user_info = user.copy()
        del user_info["password_hash"]
        
        return user_info
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Obtém lista de todos os usuários (sem senhas)
        
        Returns:
            Lista de usuários
        """
        users = []
        for attendant in self.users_config.get("attendants", []):
            user_info = attendant.copy()
            del user_info["password_hash"]
            users.append(user_info)
        
        return users
    
    def create_user(self, username: str, display_name: str, role: str, 
                   assigned_clients: List[str] = None, permissions: Dict[str, bool] = None) -> Tuple[bool, str]:
        """
        Cria um novo usuário
        
        Args:
            username: Nome de usuário
            display_name: Nome para exibição
            role: Papel do usuário
            assigned_clients: Lista de clientes designados
            permissions: Permissões específicas
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Verificar se usuário já existe
            if self._find_user_by_username(username):
                return False, "Usuário já existe"
            
            # Gerar novo ID
            existing_ids = [att["id"] for att in self.users_config.get("attendants", [])]
            new_id = f"ATD{len(existing_ids) + 1:03d}"
            
            # Usar permissões padrão se não fornecidas
            if not permissions:
                permissions = self._get_default_permissions_for_role(role)
            
            # Criar usuário
            new_user = {
                "id": new_id,
                "username": username,
                "display_name": display_name,
                "password_hash": self._hash_password(self.users_config.get("default_password", "quality123")),
                "role": role,
                "permissions": permissions,
                "assigned_clients": assigned_clients or ["*"],
                "shift": "any",
                "created_at": datetime.now().isoformat()
            }
            
            # Adicionar à configuração
            self.users_config["attendants"].append(new_user)
            self._save_users_config(self.users_config)
            
            return True, f"Usuário {username} criado com sucesso (ID: {new_id})"
            
        except Exception as e:
            return False, f"Erro ao criar usuário: {e}"
    
    def _get_default_permissions_for_role(self, role: str) -> Dict[str, bool]:
        """Obtém permissões padrão para um papel"""
        default_permissions = {
            "administrator": {
                "can_restart_services": True,
                "can_kill_processes": True,
                "can_view_logs": True,
                "can_manage_all_clients": True,
                "can_perform_critical_actions": True,
                "can_manage_attendants": True,
                "can_view_all_sessions": True
            },
            "senior_support": {
                "can_restart_services": True,
                "can_kill_processes": True,
                "can_view_logs": True,
                "can_manage_all_clients": True,
                "can_perform_critical_actions": True
            },
            "junior_support": {
                "can_restart_services": True,
                "can_kill_processes": False,
                "can_view_logs": True,
                "can_manage_all_clients": False,
                "can_perform_critical_actions": False
            }
        }
        
        return default_permissions.get(role, {})
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Altera senha de um usuário
        
        Args:
            user_id: ID do usuário
            old_password: Senha atual
            new_password: Nova senha
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            user = self._find_user_by_id(user_id)
            if not user:
                return False, "Usuário não encontrado"
            
            # Verificar senha atual
            old_hash = self._hash_password(old_password)
            if user["password_hash"] != old_hash:
                return False, "Senha atual incorreta"
            
            # Atualizar senha
            user["password_hash"] = self._hash_password(new_password)
            self._save_users_config(self.users_config)
            
            return True, "Senha alterada com sucesso"
            
        except Exception as e:
            return False, f"Erro ao alterar senha: {e}"
    
    def get_roles(self) -> Dict[str, Any]:
        """
        Obtém informações dos papéis disponíveis
        
        Returns:
            Dicionário com papéis
        """
        return self.users_config.get("roles", {})
