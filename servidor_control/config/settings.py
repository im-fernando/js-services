#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do Servidor Quality Control Panel
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = "config/server_config.json") -> Dict[str, Any]:
    """
    Carrega configuração do arquivo JSON
    
    Args:
        config_path: Caminho para o arquivo de configuração
        
    Returns:
        Dicionário com as configurações carregadas
    """
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(config_path):
            # Criar configuração padrão se não existir
            default_config = create_default_config()
            save_config(default_config, config_path)
            return default_config
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validar configuração básica
        validate_config(config)
        
        return config
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar configuração: {e}")

def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Salva configuração em arquivo JSON
    
    Args:
        config: Dicionário de configuração
        config_path: Caminho para salvar
    """
    try:
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar configuração: {e}")

def validate_config(config: Dict[str, Any]) -> None:
    """
    Valida se a configuração possui os campos obrigatórios
    
    Args:
        config: Dicionário de configuração
    """
    required_sections = ['server', 'quality_services']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Seção obrigatória '{section}' não encontrada na configuração")

def create_default_config() -> Dict[str, Any]:
    """
    Cria configuração padrão para o servidor
    
    Returns:
        Configuração padrão
    """
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8765,
            "max_clients": 50,
            "heartbeat_timeout": 60,
            "log_level": "INFO"
        },
        "quality_services": {
            "srvIntegraWeb": {
                "name": "IntegraWebService",
                "description": "Serviço de Integração Web do Quality",
                "icon": "🌐",
                "critical": True,
                "dependencies": []
            },
            "ServicoFiscal": {
                "name": "webPostoFiscalService",
                "description": "Serviço Fiscal do WebPosto",
                "icon": "💰",
                "critical": True,
                "dependencies": ["srvIntegraWeb"]
            },
            "ServicoAutomacao": {
                "name": "webPostoLeituraAutomacao",
                "description": "Serviço de Automação e Leitura",
                "icon": "🤖",
                "critical": False,
                "dependencies": ["srvIntegraWeb", "ServicoFiscal"]
            },
            "webPostoPayServer": {
                "name": "webPostoPayServer",
                "description": "Servidor de Pagamento WebPosto",
                "icon": "💳",
                "critical": True,
                "dependencies": ["ServicoFiscal"]
            },
            "QualityPulser": {
                "name": "QualityPulserWeb",
                "description": "Quality Pulser Web Service",
                "icon": "⚡",
                "critical": False,
                "dependencies": ["srvIntegraWeb"]
            }
        },
        "interface": {
            "theme": "quality",
            "auto_refresh": 5,
            "show_system_info": True,
            "log_lines_limit": 1000
        },
        "alerts": {
            "service_down": True,
            "high_cpu_usage": 80,
            "high_memory_usage": 85,
            "log_errors": True
        },
        "logging": {
            "level": "INFO",
            "file": "logs/quality_control.log",
            "max_size_mb": 10,
            "backup_count": 5
        }
    }
