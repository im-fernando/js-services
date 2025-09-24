#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção da Instalação
Corrige problemas encontrados na instalação do sistema
"""

import subprocess
import sys
import os

def print_banner():
    """Exibe banner de correção"""
    print("=" * 60)
    print("🔧 QUALITY CONTROL PANEL - CORREÇÃO DE INSTALAÇÃO")
    print("=" * 60)
    print("Corrigindo problemas encontrados na instalação")
    print("=" * 60)
    print()

def install_missing_dependencies():
    """Instala dependências que estão faltando"""
    print("📦 Instalando dependências que estão faltando...")
    
    try:
        # Instalar websocket-client que está faltando
        print("   Instalando websocket-client...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "websocket-client==1.6.4"
        ], check=True)
        print("   ✅ websocket-client instalado")
        
        # Verificar se outras dependências estão OK
        print("   Verificando outras dependências...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "websocket-server==0.4"
        ], check=True)
        print("   ✅ websocket-server verificado")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erro ao instalar dependências: {e}")
        return False

def test_imports():
    """Testa se os imports estão funcionando"""
    print("\n🧪 Testando imports...")
    
    try:
        # Testar import do websocket
        import websocket
        print("   ✅ websocket importado com sucesso")
        
        # Testar import do websocket_server
        import websocket_server
        print("   ✅ websocket_server importado com sucesso")
        
        # Testar outros imports básicos
        import json
        import threading
        import datetime
        print("   ✅ Imports básicos OK")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro ao importar: {e}")
        return False

def test_server_modules():
    """Testa se os módulos do servidor podem ser importados"""
    print("\n🔍 Testando módulos do servidor...")
    
    try:
        # Adicionar o diretório do servidor ao path
        server_dir = "C:\\Quality\\ControlPanel"
        if os.path.exists(server_dir):
            sys.path.insert(0, server_dir)
            
            # Testar imports dos módulos do servidor
            from config.settings import load_config
            print("   ✅ config.settings importado")
            
            from utils.auth import QualityAuthManager
            print("   ✅ utils.auth importado")
            
            from core.session_manager import SessionManager
            print("   ✅ core.session_manager importado")
            
            from core.attendant_manager import AttendantManager
            print("   ✅ core.attendant_manager importado")
            
            return True
        else:
            print(f"   ❌ Diretório do servidor não encontrado: {server_dir}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao importar módulos do servidor: {e}")
        return False

def test_configuration():
    """Testa se as configurações podem ser carregadas"""
    print("\n⚙️  Testando configurações...")
    
    try:
        server_dir = "C:\\Quality\\ControlPanel"
        if os.path.exists(server_dir):
            sys.path.insert(0, server_dir)
            
            from config.settings import load_config
            
            # Testar carregamento da configuração do servidor
            config_file = os.path.join(server_dir, "config", "server_config.json")
            if os.path.exists(config_file):
                config = load_config(config_file)
                print(f"   ✅ Configuração do servidor carregada")
                print(f"      Host: {config['server']['host']}")
                print(f"      Porta: {config['server']['port']}")
            else:
                print(f"   ❌ Arquivo de configuração não encontrado: {config_file}")
                return False
            
            # Testar carregamento da configuração de usuários
            users_file = os.path.join(server_dir, "config", "users_config.json")
            if os.path.exists(users_file):
                from utils.auth import QualityAuthManager
                auth_manager = QualityAuthManager(users_file)
                users = auth_manager.get_all_users()
                print(f"   ✅ Configuração de usuários carregada ({len(users)} usuários)")
            else:
                print(f"   ❌ Arquivo de usuários não encontrado: {users_file}")
                return False
            
            return True
        else:
            print(f"   ❌ Diretório do servidor não encontrado: {server_dir}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao testar configurações: {e}")
        return False

def main():
    """Função principal de correção"""
    print_banner()
    
    # Instalar dependências faltantes
    if not install_missing_dependencies():
        print("\n❌ Falha ao instalar dependências")
        input("\nPressione Enter para sair...")
        return False
    
    # Testar imports básicos
    if not test_imports():
        print("\n❌ Falha nos imports básicos")
        input("\nPressione Enter para sair...")
        return False
    
    # Testar módulos do servidor
    if not test_server_modules():
        print("\n❌ Falha nos módulos do servidor")
        input("\nPressione Enter para sair...")
        return False
    
    # Testar configurações
    if not test_configuration():
        print("\n❌ Falha nas configurações")
        input("\nPressione Enter para sair...")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("✅ Todas as dependências foram instaladas")
    print("✅ Todos os módulos estão funcionando")
    print("✅ Todas as configurações foram carregadas")
    print()
    print("🚀 O sistema está pronto para uso!")
    print("   Execute: C:\\Quality\\ControlPanel\\start_server.bat")
    print("=" * 60)
    
    input("\nPressione Enter para finalizar...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Correção cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
