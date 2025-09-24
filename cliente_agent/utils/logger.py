#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging para Quality Agent
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class QualityLogger:
    """Logger personalizado para o sistema Quality"""
    
    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.debug = debug
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o logger com formatação personalizada"""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # Evitar duplicação de handlers
        if logger.handlers:
            return logger
        
        # Formatter personalizado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para arquivo (se debug ativado)
        if self.debug:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def info(self, message: str) -> None:
        """Log de informação"""
        self.logger.info(f"ℹ️  {message}")
    
    def debug(self, message: str) -> None:
        """Log de debug"""
        self.logger.debug(f"🔍 {message}")
    
    def warning(self, message: str) -> None:
        """Log de aviso"""
        self.logger.warning(f"⚠️  {message}")
    
    def error(self, message: str) -> None:
        """Log de erro"""
        self.logger.error(f"❌ {message}")
    
    def critical(self, message: str) -> None:
        """Log crítico"""
        self.logger.critical(f"🚨 {message}")
    
    def success(self, message: str) -> None:
        """Log de sucesso"""
        self.logger.info(f"✅ {message}")
    
    def service_status(self, service_name: str, status: str, details: str = "") -> None:
        """Log específico para status de serviços"""
        status_emoji = {
            'running': '🟢',
            'stopped': '🔴',
            'starting': '🟡',
            'stopping': '🟡',
            'error': '❌'
        }
        emoji = status_emoji.get(status, '❓')
        self.logger.info(f"{emoji} {service_name}: {status.upper()}{' - ' + details if details else ''}")

def setup_logger(name: str, debug: bool = False) -> QualityLogger:
    """
    Configura e retorna um logger personalizado
    
    Args:
        name: Nome do logger
        debug: Se deve ativar modo debug
        
    Returns:
        Instância do QualityLogger
    """
    return QualityLogger(name, debug)
