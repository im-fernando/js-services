#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funções auxiliares para o Quality Control Panel
"""

import os
import sys
import platform
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def format_timestamp(timestamp: str) -> str:
    """
    Formata timestamp para exibição
    
    Args:
        timestamp: Timestamp ISO
        
    Returns:
        String formatada
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except Exception:
        return timestamp

def format_uptime(uptime_str: str) -> str:
    """
    Formata tempo de execução para exibição
    
    Args:
        uptime_str: String de uptime
        
    Returns:
        String formatada
    """
    if not uptime_str:
        return "N/A"
    
    # Se já está formatado, retornar como está
    if "days" in uptime_str or "h" in uptime_str or "m" in uptime_str:
        return uptime_str
    
    try:
        # Tentar converter de segundos
        seconds = float(uptime_str)
        return format_seconds_to_readable(seconds)
    except Exception:
        return uptime_str

def format_seconds_to_readable(seconds: float) -> str:
    """
    Converte segundos para formato legível
    
    Args:
        seconds: Segundos
        
    Returns:
        String formatada
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    
    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes}m {seconds % 60:.0f}s"
    
    hours = int(minutes // 60)
    if hours < 24:
        return f"{hours}h {minutes % 60}m"
    
    days = int(hours // 24)
    hours = hours % 24
    return f"{days} dias, {hours:02d}:{minutes % 60:02d}:{seconds % 60:02.0f}"

def get_status_emoji(status: str) -> str:
    """
    Retorna emoji para status de serviço
    
    Args:
        status: Status do serviço
        
    Returns:
        Emoji correspondente
    """
    status_emojis = {
        'running': '🟢',
        'stopped': '🔴',
        'starting': '🟡',
        'stopping': '🟡',
        'error': '❌',
        'unknown': '❓'
    }
    return status_emojis.get(status.lower(), '❓')

def get_critical_emoji(is_critical: bool) -> str:
    """
    Retorna emoji para serviços críticos
    
    Args:
        is_critical: Se é crítico
        
    Returns:
        Emoji correspondente
    """
    return '🚨' if is_critical else 'ℹ️'

def format_memory_usage(memory_str: str) -> str:
    """
    Formata uso de memória para exibição
    
    Args:
        memory_str: String de memória
        
    Returns:
        String formatada
    """
    if not memory_str:
        return "N/A"
    
    # Se já está formatado (contém MB, GB, etc), retornar como está
    if any(unit in memory_str.upper() for unit in ['B', 'KB', 'MB', 'GB', 'TB']):
        return memory_str
    
    try:
        # Tentar converter de bytes
        bytes_value = int(memory_str)
        return format_bytes(bytes_value)
    except Exception:
        return memory_str

def format_bytes(bytes_value: int) -> str:
    """
    Formata bytes em formato legível
    
    Args:
        bytes_value: Valor em bytes
        
    Returns:
        String formatada (ex: "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def get_cpu_usage_color(cpu_percent: float) -> str:
    """
    Retorna cor para uso de CPU
    
    Args:
        cpu_percent: Percentual de CPU
        
    Returns:
        String com cor
    """
    if cpu_percent < 30:
        return "🟢"  # Verde
    elif cpu_percent < 70:
        return "🟡"  # Amarelo
    else:
        return "🔴"  # Vermelho

def get_memory_usage_color(memory_percent: float) -> str:
    """
    Retorna cor para uso de memória
    
    Args:
        memory_percent: Percentual de memória
        
    Returns:
        String com cor
    """
    if memory_percent < 50:
        return "🟢"  # Verde
    elif memory_percent < 80:
        return "🟡"  # Amarelo
    else:
        return "🔴"  # Vermelho

def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Trunca string se for muito longa
    
    Args:
        text: Texto para truncar
        max_length: Tamanho máximo
        
    Returns:
        String truncada
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def safe_json_serialize(obj: Any) -> Any:
    """
    Serializa objeto para JSON de forma segura
    
    Args:
        obj: Objeto para serializar
        
    Returns:
        Objeto serializável
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return str(obj)
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)

def create_directory_if_not_exists(path: str) -> bool:
    """
    Cria diretório se não existir
    
    Args:
        path: Caminho do diretório
        
    Returns:
        True se criou ou já existia
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ Erro ao criar diretório {path}: {e}")
        return False

def get_system_info() -> Dict[str, Any]:
    """
    Coleta informações do sistema servidor
    
    Returns:
        Dicionário com informações do sistema
    """
    try:
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node(),
            'python_version': sys.version,
            'server_time': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def validate_client_id(client_id: str) -> bool:
    """
    Valida se o ID do cliente é válido
    
    Args:
        client_id: ID do cliente
        
    Returns:
        True se válido
    """
    if not client_id or not isinstance(client_id, str):
        return False
    
    # Aceitar IDs que começam com QUALITY_CLIENTE_ ou SERVIDOR_
    return (client_id.startswith('QUALITY_CLIENTE_') or 
            client_id.startswith('SERVIDOR_') or
            client_id.startswith('CLIENT_'))

def format_client_name(client_id: str, client_name: str) -> str:
    """
    Formata nome do cliente para exibição
    
    Args:
        client_id: ID do cliente
        client_name: Nome do cliente
        
    Returns:
        Nome formatado
    """
    if client_name and client_name != "Unknown Client":
        return client_name
    
    # Extrair número do ID se possível
    try:
        number = client_id.split('_')[-1]
        return f"Cliente Quality #{number}"
    except Exception:
        return f"Cliente {client_id}"

def get_service_priority(service_name: str, quality_services: Dict[str, Any]) -> int:
    """
    Retorna prioridade de um serviço (para ordenação)
    
    Args:
        service_name: Nome do serviço
        quality_services: Configuração dos serviços
        
    Returns:
        Prioridade (menor = mais importante)
    """
    service_config = quality_services.get(service_name, {})
    
    if service_config.get('critical', False):
        return 1  # Críticos primeiro
    
    # Ordem baseada em dependências
    dependencies = service_config.get('dependencies', [])
    if not dependencies:
        return 2  # Sem dependências
    
    return 3  # Com dependências

def sort_services_by_priority(services: List[str], quality_services: Dict[str, Any]) -> List[str]:
    """
    Ordena serviços por prioridade
    
    Args:
        services: Lista de serviços
        quality_services: Configuração dos serviços
        
    Returns:
        Lista ordenada
    """
    return sorted(services, key=lambda s: get_service_priority(s, quality_services))

def calculate_uptime_percentage(services_status: Dict[str, Any]) -> float:
    """
    Calcula percentual de serviços rodando
    
    Args:
        services_status: Status dos serviços
        
    Returns:
        Percentual (0-100)
    """
    if not services_status:
        return 0.0
    
    running_count = sum(1 for status in services_status.values() 
                       if isinstance(status, dict) and status.get('status') == 'running')
    
    total_count = len(services_status)
    return (running_count / total_count) * 100 if total_count > 0 else 0.0

def get_health_status(services_status: Dict[str, Any], quality_services: Dict[str, Any]) -> str:
    """
    Determina status geral de saúde do sistema
    
    Args:
        services_status: Status dos serviços
        quality_services: Configuração dos serviços
        
    Returns:
        Status de saúde
    """
    if not services_status:
        return "unknown"
    
    critical_services_down = 0
    total_critical = 0
    
    for service_name, status in services_status.items():
        service_config = quality_services.get(service_name, {})
        
        if service_config.get('critical', False):
            total_critical += 1
            if not (isinstance(status, dict) and status.get('status') == 'running'):
                critical_services_down += 1
    
    if total_critical == 0:
        return "unknown"
    
    if critical_services_down == 0:
        return "healthy"
    elif critical_services_down < total_critical:
        return "degraded"
    else:
        return "critical"
