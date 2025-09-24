#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging para Quality Control Panel
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class QualityControlLogger:
    """Logger personalizado para o Quality Control Panel"""
    
    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.debug_mode = debug
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o logger com formatação personalizada"""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
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
        
        # Handler para arquivo (sempre ativo para servidor)
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
    
    def client_connected(self, client_id: str, client_name: str) -> None:
        """Log específico para conexão de cliente"""
        self.logger.info(f"🔌 Cliente conectado: {client_name} ({client_id})")
    
    def client_disconnected(self, client_id: str, client_name: str) -> None:
        """Log específico para desconexão de cliente"""
        self.logger.info(f"🔌 Cliente desconectado: {client_name} ({client_id})")
    
    def command_executed(self, client_id: str, action: str, success: bool) -> None:
        """Log específico para execução de comandos"""
        status = "✅" if success else "❌"
        self.logger.info(f"{status} Comando executado: {action} para {client_id}")

def setup_logger(name: str, debug: bool = False) -> QualityControlLogger:
    """
    Configura e retorna um logger personalizado
    
    Args:
        name: Nome do logger
        debug: Se deve ativar modo debug
        
    Returns:
        Instância do QualityControlLogger
    """
    return QualityControlLogger(name, debug)
