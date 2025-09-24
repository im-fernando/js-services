#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Log de Atividades
Registra todas as atividades dos atendentes para auditoria
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

class ActivityLogger:
    """Logger de atividades para auditoria"""
    
    def __init__(self, logger, log_dir: str = "logs/activities"):
        self.logger = logger
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Lock para thread safety
        self.log_lock = threading.Lock()
        
        # Configurações
        self.max_log_size = 10 * 1024 * 1024  # 10MB
        self.max_log_files = 30  # 30 dias
        
        self.logger.info("📋 Activity Logger inicializado")
    
    def log_attendant_action(self, session_id: str, attendant_id: str, attendant_name: str,
                           action: str, client_id: str = None, client_name: str = None,
                           details: Dict[str, Any] = None, result: str = "success",
                           ip_address: str = None) -> None:
        """
        Registra ação de um atendente
        
        Args:
            session_id: ID da sessão
            attendant_id: ID do atendente
            attendant_name: Nome do atendente
            action: Ação executada
            client_id: ID do cliente (opcional)
            client_name: Nome do cliente (opcional)
            details: Detalhes da ação
            result: Resultado da ação
            ip_address: Endereço IP
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "attendant_id": attendant_id,
                "attendant_name": attendant_name,
                "client_id": client_id,
                "client_name": client_name,
                "action": action,
                "details": details or {},
                "result": result,
                "ip_address": ip_address
            }
            
            self._write_log_entry(log_entry)
            
            # Log para console também
            self.logger.info(f"📋 {attendant_name} executou {action} em {client_name or 'sistema'}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar atividade: {e}")
    
    def log_system_event(self, event_type: str, description: str, 
                        details: Dict[str, Any] = None, severity: str = "info") -> None:
        """
        Registra evento do sistema
        
        Args:
            event_type: Tipo do evento
            description: Descrição do evento
            details: Detalhes adicionais
            severity: Severidade (info, warning, error, critical)
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "system_event",
                "event_type": event_type,
                "description": description,
                "details": details or {},
                "severity": severity
            }
            
            self._write_log_entry(log_entry)
            
            # Log para console baseado na severidade
            if severity == "error" or severity == "critical":
                self.logger.error(f"🚨 Sistema: {description}")
            elif severity == "warning":
                self.logger.warning(f"⚠️  Sistema: {description}")
            else:
                self.logger.info(f"ℹ️  Sistema: {description}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar evento do sistema: {e}")
    
    def log_client_event(self, client_id: str, client_name: str, event_type: str,
                        description: str, details: Dict[str, Any] = None) -> None:
        """
        Registra evento de cliente
        
        Args:
            client_id: ID do cliente
            client_name: Nome do cliente
            event_type: Tipo do evento
            description: Descrição do evento
            details: Detalhes adicionais
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "client_event",
                "client_id": client_id,
                "client_name": client_name,
                "event_type": event_type,
                "description": description,
                "details": details or {}
            }
            
            self._write_log_entry(log_entry)
            
            self.logger.info(f"🖥️  {client_name}: {description}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar evento do cliente: {e}")
    
    def log_security_event(self, event_type: str, description: str,
                          attendant_id: str = None, ip_address: str = None,
                          details: Dict[str, Any] = None) -> None:
        """
        Registra evento de segurança
        
        Args:
            event_type: Tipo do evento
            description: Descrição do evento
            attendant_id: ID do atendente (se aplicável)
            ip_address: Endereço IP
            details: Detalhes adicionais
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "security_event",
                "event_type": event_type,
                "description": description,
                "attendant_id": attendant_id,
                "ip_address": ip_address,
                "details": details or {}
            }
            
            self._write_log_entry(log_entry)
            
            # Logs de segurança sempre como warning ou error
            self.logger.warning(f"🔒 Segurança: {description}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar evento de segurança: {e}")
    
    def _write_log_entry(self, log_entry: Dict[str, Any]) -> None:
        """
        Escreve entrada no log
        
        Args:
            log_entry: Entrada do log
        """
        try:
            with self.log_lock:
                # Determinar arquivo de log baseado na data
                date_str = datetime.now().strftime("%Y%m%d")
                log_file = self.log_dir / f"activity_{date_str}.jsonl"
                
                # Escrever entrada
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
                # Verificar tamanho do arquivo
                self._check_log_rotation(log_file)
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao escrever entrada do log: {e}")
    
    def _check_log_rotation(self, log_file: Path) -> None:
        """
        Verifica se é necessário fazer rotação do log
        
        Args:
            log_file: Arquivo de log
        """
        try:
            if not log_file.exists():
                return
            
            # Verificar tamanho
            if log_file.stat().st_size > self.max_log_size:
                # Fazer backup do arquivo atual
                backup_file = log_file.with_suffix('.jsonl.bak')
                if backup_file.exists():
                    backup_file.unlink()
                
                log_file.rename(backup_file)
                
                # Criar novo arquivo
                log_file.touch()
                
                self.logger.info(f"📋 Log rotacionado: {log_file.name}")
            
            # Limpar logs antigos
            self._cleanup_old_logs()
            
        except Exception as e:
            self.logger.error(f"❌ Erro na rotação do log: {e}")
    
    def _cleanup_old_logs(self) -> None:
        """Remove logs antigos"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.max_log_files)
            
            for log_file in self.log_dir.glob("activity_*.jsonl*"):
                try:
                    # Extrair data do nome do arquivo
                    date_str = log_file.stem.split('_')[1]
                    file_date = datetime.strptime(date_str, "%Y%m%d")
                    
                    if file_date < cutoff_date:
                        log_file.unlink()
                        self.logger.info(f"📋 Log antigo removido: {log_file.name}")
                        
                except (ValueError, IndexError):
                    # Ignorar arquivos com formato inválido
                    continue
                    
        except Exception as e:
            self.logger.error(f"❌ Erro na limpeza de logs antigos: {e}")
    
    def get_activity_logs(self, start_date: datetime = None, end_date: datetime = None,
                         attendant_id: str = None, action: str = None,
                         client_id: str = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Obtém logs de atividades com filtros
        
        Args:
            start_date: Data de início
            end_date: Data de fim
            attendant_id: ID do atendente
            action: Ação específica
            client_id: ID do cliente
            limit: Limite de resultados
            
        Returns:
            Lista de logs
        """
        try:
            logs = []
            
            # Se não especificou datas, usar últimos 7 dias
            if not start_date:
                start_date = datetime.now() - timedelta(days=7)
            if not end_date:
                end_date = datetime.now()
            
            # Buscar arquivos de log no período
            current_date = start_date.date()
            end_date_only = end_date.date()
            
            while current_date <= end_date_only:
                date_str = current_date.strftime("%Y%m%d")
                log_file = self.log_dir / f"activity_{date_str}.jsonl"
                
                if log_file.exists():
                    with open(log_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                log_entry = json.loads(line.strip())
                                
                                # Aplicar filtros
                                if self._matches_filters(log_entry, attendant_id, action, client_id, start_date, end_date):
                                    logs.append(log_entry)
                                    
                                    if len(logs) >= limit:
                                        break
                                        
                            except json.JSONDecodeError:
                                continue
                
                if len(logs) >= limit:
                    break
                    
                current_date += timedelta(days=1)
            
            # Ordenar por timestamp (mais recente primeiro)
            logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return logs[:limit]
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter logs de atividade: {e}")
            return []
    
    def _matches_filters(self, log_entry: Dict[str, Any], attendant_id: str = None,
                        action: str = None, client_id: str = None,
                        start_date: datetime = None, end_date: datetime = None) -> bool:
        """
        Verifica se entrada do log corresponde aos filtros
        
        Args:
            log_entry: Entrada do log
            attendant_id: ID do atendente
            action: Ação
            client_id: ID do cliente
            start_date: Data de início
            end_date: Data de fim
            
        Returns:
            True se corresponde aos filtros
        """
        try:
            # Filtro por atendente
            if attendant_id and log_entry.get('attendant_id') != attendant_id:
                return False
            
            # Filtro por ação
            if action and log_entry.get('action') != action:
                return False
            
            # Filtro por cliente
            if client_id and log_entry.get('client_id') != client_id:
                return False
            
            # Filtro por data
            if start_date or end_date:
                timestamp_str = log_entry.get('timestamp')
                if timestamp_str:
                    try:
                        log_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        
                        if start_date and log_timestamp < start_date:
                            return False
                        if end_date and log_timestamp > end_date:
                            return False
                            
                    except ValueError:
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na verificação de filtros: {e}")
            return False
    
    def get_attendant_statistics(self, attendant_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Obtém estatísticas de um atendente
        
        Args:
            attendant_id: ID do atendente
            days: Número de dias para análise
            
        Returns:
            Estatísticas do atendente
        """
        try:
            start_date = datetime.now() - timedelta(days=days)
            logs = self.get_activity_logs(start_date=start_date, attendant_id=attendant_id)
            
            # Calcular estatísticas
            total_actions = len(logs)
            successful_actions = sum(1 for log in logs if log.get('result') == 'success')
            
            # Contar ações por tipo
            action_counts = {}
            for log in logs:
                action = log.get('action', 'unknown')
                action_counts[action] = action_counts.get(action, 0) + 1
            
            # Contar clientes atendidos
            clients_attended = set()
            for log in logs:
                client_id = log.get('client_id')
                if client_id:
                    clients_attended.add(client_id)
            
            # Calcular tempo médio de sessão (simulado)
            sessions = set()
            for log in logs:
                session_id = log.get('session_id')
                if session_id:
                    sessions.add(session_id)
            
            return {
                "attendant_id": attendant_id,
                "period_days": days,
                "total_actions": total_actions,
                "successful_actions": successful_actions,
                "success_rate": (successful_actions / total_actions * 100) if total_actions > 0 else 0,
                "action_breakdown": action_counts,
                "clients_attended": len(clients_attended),
                "unique_sessions": len(sessions),
                "average_actions_per_day": total_actions / days if days > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas do atendente: {e}")
            return {"error": str(e)}
    
    def get_system_statistics(self, days: int = 7) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais do sistema
        
        Args:
            days: Número de dias para análise
            
        Returns:
            Estatísticas do sistema
        """
        try:
            start_date = datetime.now() - timedelta(days=days)
            logs = self.get_activity_logs(start_date=start_date)
            
            # Calcular estatísticas
            total_actions = len(logs)
            successful_actions = sum(1 for log in logs if log.get('result') == 'success')
            
            # Contar por tipo de evento
            event_types = {}
            for log in logs:
                event_type = log.get('type', 'unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Contar atendentes únicos
            attendants = set()
            for log in logs:
                attendant_id = log.get('attendant_id')
                if attendant_id:
                    attendants.add(attendant_id)
            
            # Contar clientes únicos
            clients = set()
            for log in logs:
                client_id = log.get('client_id')
                if client_id:
                    clients.add(client_id)
            
            return {
                "period_days": days,
                "total_actions": total_actions,
                "successful_actions": successful_actions,
                "success_rate": (successful_actions / total_actions * 100) if total_actions > 0 else 0,
                "event_types": event_types,
                "unique_attendants": len(attendants),
                "unique_clients": len(clients),
                "average_actions_per_day": total_actions / days if days > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter estatísticas do sistema: {e}")
            return {"error": str(e)}
