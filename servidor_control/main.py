#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality Control Panel - Servidor
Sistema de controle remoto para serviços Quality
"""

import sys
import os
import argparse
import signal
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from core.server import QualityControlServer
from utils.logger import setup_logger
from config.settings import load_config

def signal_handler(signum, frame):
    """Handler para sinais de interrupção"""
    print("\n🛑 Recebido sinal de interrupção. Encerrando servidor...")
    sys.exit(0)

def main():
    """Função principal do servidor de controle"""
    parser = argparse.ArgumentParser(description='Quality Control Panel Server')
    parser.add_argument('--config', '-c', default='config/server_config.json',
                       help='Caminho para arquivo de configuração')
    parser.add_argument('--port', '-p', type=int, default=8765,
                       help='Porta do servidor')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host do servidor')
    parser.add_argument('--debug', action='store_true',
                       help='Modo debug com logs detalhados')
    parser.add_argument('--quality-mode', action='store_true',
                       help='Modo específico para serviços Quality')
    parser.add_argument('--multi-attendant', action='store_true',
                       help='Modo multi-atendente (padrão)')
    
    args = parser.parse_args()
    
    # Configurar handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Carregar configuração
        config = load_config(args.config)
        
        # Sobrescrever configurações da linha de comando
        if args.port:
            config['server']['port'] = args.port
        if args.host:
            config['server']['host'] = args.host
        
        # Configurar logger
        logger = setup_logger('quality_control_server', debug=args.debug)
        logger.info("🚀 Iniciando Quality Control Panel Server...")
        
        # Criar e iniciar servidor
        server = QualityControlServer(config, logger)
        
        if args.quality_mode:
            logger.info("🎯 Modo Quality ativado - Interface específica para serviços Quality")
            server.set_quality_mode(True)
        
        logger.info(f"🌐 Servidor iniciando em {config['server']['host']}:{config['server']['port']}")
        server.start()
            
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
