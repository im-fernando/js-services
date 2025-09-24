#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funções auxiliares para o Quality Agent
"""

import os
import sys
import platform
import subprocess
import psutil
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

def get_system_info() -> Dict[str, Any]:
    """
    Coleta informações do sistema
    
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
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:\\').percent
        }
    except Exception as e:
        return {'error': str(e)}

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

def format_uptime(seconds: float) -> str:
    """
    Formata tempo de execução em formato legível
    
    Args:
        seconds: Tempo em segundos
        
    Returns:
        String formatada (ex: "2 days, 14:30:52")
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
    return f"{days} days, {hours:02d}:{minutes % 60:02d}:{seconds % 60:02.0f}"

def is_windows_service_running(service_name: str) -> bool:
    """
    Verifica se um serviço Windows está rodando
    
    Args:
        service_name: Nome do serviço
        
    Returns:
        True se o serviço está rodando
    """
    try:
        if platform.system() != 'Windows':
            return False
        
        result = subprocess.run(
            ['sc', 'query', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return 'RUNNING' in result.stdout
        
    except Exception:
        return False

def get_process_by_name(process_name: str) -> List[Dict[str, Any]]:
    """
    Busca processos por nome
    
    Args:
        process_name: Nome do processo
        
    Returns:
        Lista de processos encontrados
    """
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'status', 'create_time', 'memory_info', 'cpu_percent']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': proc.info['exe'],
                        'status': proc.info['status'],
                        'create_time': proc.info['create_time'],
                        'memory_usage': proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                        'cpu_percent': proc.cpu_percent()
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"❌ Erro ao buscar processos: {e}")
    
    return processes

def kill_process_by_pid(pid: int) -> bool:
    """
    Finaliza processo por PID
    
    Args:
        pid: ID do processo
        
    Returns:
        True se conseguiu finalizar
    """
    try:
        process = psutil.Process(pid)
        process.terminate()
        
        # Aguardar até 5 segundos para o processo terminar
        try:
            process.wait(timeout=5)
        except psutil.TimeoutExpired:
            # Se não terminou, forçar kill
            process.kill()
            process.wait(timeout=2)
        
        return True
        
    except psutil.NoSuchProcess:
        return True  # Processo já não existe
    except Exception as e:
        print(f"❌ Erro ao finalizar processo {pid}: {e}")
        return False

def validate_path(path: str) -> bool:
    """
    Valida se um caminho existe e é acessível
    
    Args:
        path: Caminho para validar
        
    Returns:
        True se o caminho é válido
    """
    try:
        return os.path.exists(path) and os.access(path, os.R_OK)
    except Exception:
        return False

def get_file_size_mb(file_path: str) -> float:
    """
    Retorna tamanho do arquivo em MB
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Tamanho em MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0

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

def get_network_interfaces() -> List[Dict[str, str]]:
    """
    Retorna informações das interfaces de rede
    
    Returns:
        Lista de interfaces de rede
    """
    interfaces = []
    
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == 2:  # IPv4
                    interfaces.append({
                        'interface': interface,
                        'ip': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
    except Exception as e:
        print(f"❌ Erro ao obter interfaces de rede: {e}")
    
    return interfaces

def is_port_in_use(port: int) -> bool:
    """
    Verifica se uma porta está em uso
    
    Args:
        port: Número da porta
        
    Returns:
        True se a porta está em uso
    """
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result == 0
    except Exception:
        return False
