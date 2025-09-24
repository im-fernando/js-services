#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality Remote Agent - Cliente
Sistema de monitoramento e controle remoto para serviços Quality
"""

import sys
import os
import argparse
import signal
import time
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from core.agent import QualityAgent
from utils.logger import setup_logger
from config.settings import load_config

def signal_handler(signum, frame):
    """Handler para sinais de interrupção"""
    print("\n🛑 Recebido sinal de interrupção. Encerrando agente...")
    sys.exit(0)

def main():
    """Função principal do agente Quality"""
    parser = argparse.ArgumentParser(description='Quality Remote Agent')
    parser.add_argument('--config', '-c', default='config/services_config.json',
                       help='Caminho para arquivo de configuração')
    parser.add_argument('--install-service', action='store_true',
                       help='Instalar como serviço Windows')
    parser.add_argument('--debug', action='store_true',
                       help='Modo debug com logs detalhados')
    
    args = parser.parse_args()
    
    # Configurar handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Carregar configuração
        config = load_config(args.config)
        
        # Configurar logger
        logger = setup_logger('quality_agent', debug=args.debug)
        logger.info("🚀 Iniciando Quality Remote Agent...")
        
        # Criar e iniciar agente
        agent = QualityAgent(config, logger)
        
        if args.install_service:
            logger.info("📦 Instalando como serviço Windows...")
            agent.install_as_service()
        else:
            logger.info("🔄 Iniciando agente em modo interativo...")
            agent.start()
            
    except KeyboardInterrupt:
        print("\n👋 Agente encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
