#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do Cliente Quality Agent
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

def load_config(config_path: str = "config/services_config.json") -> Dict[str, Any]:
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
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validar configuração básica
        validate_config(config)
        
        return config
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar configuração: {e}")

def validate_config(config: Dict[str, Any]) -> None:
    """
    Valida se a configuração possui os campos obrigatórios
    
    Args:
        config: Dicionário de configuração
    """
    required_sections = ['services', 'server', 'client']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Seção obrigatória '{section}' não encontrada na configuração")
    
    # Validar serviços
    if not isinstance(config['services'], list) or len(config['services']) == 0:
        raise ValueError("Lista de serviços não pode estar vazia")
    
    # Validar campos obrigatórios de cada serviço
    required_service_fields = ['name', 'display_name', 'executable_path', 'log_base_path']
    
    for i, service in enumerate(config['services']):
        for field in required_service_fields:
            if field not in service:
                raise ValueError(f"Serviço {i}: campo obrigatório '{field}' não encontrado")

def get_installed_services(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filtra apenas os serviços que estão realmente instalados no sistema
    
    Args:
        config: Configuração completa
        
    Returns:
        Lista de serviços instalados
    """
    installed_services = []
    
    for service in config['services']:
        executable_path = service.get('executable_path', '')
        
        # Verificar se o executável existe
        if os.path.exists(executable_path):
            installed_services.append(service)
        else:
            print(f"⚠️  Serviço {service['display_name']} não encontrado em: {executable_path}")
    
    return installed_services

def create_default_config() -> Dict[str, Any]:
    """
    Cria configuração padrão para os serviços Quality
    
    Returns:
        Configuração padrão
    """
    return {
        "services": [
            {
                "name": "srvIntegraWeb",
                "display_name": "IntegraWebService",
                "executable_path": "C:\\Quality\\web\\IntegraWebService.exe",
                "log_base_path": "C:\\Quality\\LOG\\Integra",
                "log_structure": "nested_numeric_folders",
                "log_file_pattern": "*.txt",
                "description": "Serviço de Integração Web do Quality",
                "enabled": True
            },
            {
                "name": "ServicoFiscal",
                "display_name": "webPostoFiscalService", 
                "executable_path": "C:\\Quality\\Services\\webPostoPayServer\\webPostoFiscalServer.exe",
                "log_base_path": "C:\\Quality\\LOG\\webPostoFiscalServer",
                "log_structure": "nested_numeric_folders",
                "log_file_pattern": "*.txt",
                "description": "Serviço Fiscal do WebPosto",
                "enabled": True
            },
            {
                "name": "ServicoAutomacao",
                "display_name": "webPostoLeituraAutomacao",
                "executable_path": "C:\\Quality\\Services\\webPostoLeituraAutomacao\\webPostoLeituraAutomacao.exe", 
                "log_base_path": "C:\\Quality\\LOG\\webPostoLeituraAutomacao",
                "log_structure": "nested_numeric_folders",
                "log_file_pattern": "*.txt",
                "description": "Serviço de Automação e Leitura",
                "enabled": True
            },
            {
                "name": "webPostoPayServer",
                "display_name": "webPostoPayServer",
                "executable_path": "C:\\Quality\\Services\\webPostoPayServer\\winSW\\webPostoPaySW.exe",
                "log_base_path": "C:\\Quality\\LOG\\QualityPDV_PAF", 
                "log_structure": "nested_numeric_folders",
                "log_file_pattern": "*.txt",
                "description": "Servidor de Pagamento WebPosto",
                "enabled": True
            },
            {
                "name": "QualityPulser",
                "display_name": "QualityPulserWeb",
                "executable_path": "C:\\Quality\\PulserWeb.exe",
                "log_base_path": "C:\\Quality\\LOG\\WebPostoPulser",
                "log_structure": "nested_numeric_folders", 
                "log_file_pattern": "*.txt",
                "description": "Quality Pulser Web Service",
                "enabled": True
            }
        ],
        "server": {
            "host": "192.168.1.100",
            "port": 8765,
            "reconnect_interval": 5,
            "heartbeat_interval": 30
        },
        "client": {
            "id": "QUALITY_CLIENTE_001",
            "name": "Posto Quality - Terminal 01",
            "location": "Matriz"
        },
        "log_monitoring": {
            "refresh_interval": 1,
            "max_lines_buffer": 1000,
            "encoding": "utf-8"
        },
        "service_dependencies": {
            "ServicoFiscal": ["srvIntegraWeb"],
            "ServicoAutomacao": ["srvIntegraWeb", "ServicoFiscal"], 
            "webPostoPayServer": ["ServicoFiscal"],
            "QualityPulser": ["srvIntegraWeb"]
        },
        "startup_order": [
            "srvIntegraWeb",
            "ServicoFiscal", 
            "ServicoAutomacao",
            "webPostoPayServer",
            "QualityPulser"
        ]
    }
