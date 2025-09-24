#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste da Instalação
Testa se a instalação está funcionando corretamente
"""

import sys
import os
import subprocess

def test_installation():
    """Testa a instalação completa"""
    print("🧪 TESTE DE INSTALAÇÃO - QUALITY CONTROL PANEL")
    print("=" * 50)
    
    # Teste 1: Verificar se o diretório existe
    print("\n1. Verificando diretório de instalação...")
    server_dir = "C:\\Quality\\ControlPanel"
    if os.path.exists(server_dir):
        print(f"   ✅ Diretório encontrado: {server_dir}")
    else:
        print(f"   ❌ Diretório não encontrado: {server_dir}")
        return False
    
    # Teste 2: Verificar arquivos principais
    print("\n2. Verificando arquivos principais...")
    main_files = [
        "main.py",
        "config/server_config.json",
        "config/users_config.json",
        "core/server.py",
        "core/session_manager.py",
        "core/attendant_manager.py",
        "utils/auth.py"
    ]
    
    for file in main_files:
        file_path = os.path.join(server_dir, file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO ENCONTRADO")
            return False
    
    # Teste 3: Verificar dependências Python
    print("\n3. Verificando dependências Python...")
    try:
        import websocket
        print("   ✅ websocket")
    except ImportError:
        print("   ❌ websocket - NÃO INSTALADO")
        return False
    
    try:
        import websocket_server
        print("   ✅ websocket_server")
    except ImportError:
        print("   ❌ websocket_server - NÃO INSTALADO")
        return False
    
    try:
        import colorama
        print("   ✅ colorama")
    except ImportError:
        print("   ❌ colorama - NÃO INSTALADO")
        return False
    
    # Teste 4: Verificar imports dos módulos
    print("\n4. Verificando imports dos módulos...")
    try:
        sys.path.insert(0, server_dir)
        
        from config.settings import load_config
        print("   ✅ config.settings")
        
        from utils.auth import QualityAuthManager
        print("   ✅ utils.auth")
        
        from core.session_manager import SessionManager
        print("   ✅ core.session_manager")
        
        from core.attendant_manager import AttendantManager
        print("   ✅ core.attendant_manager")
        
    except Exception as e:
        print(f"   ❌ Erro ao importar módulos: {e}")
        return False
    
    # Teste 5: Verificar configurações
    print("\n5. Verificando configurações...")
    try:
        config_file = os.path.join(server_dir, "config", "server_config.json")
        config = load_config(config_file)
        print(f"   ✅ Configuração do servidor carregada")
        print(f"      Host: {config['server']['host']}")
        print(f"      Porta: {config['server']['port']}")
        
        users_file = os.path.join(server_dir, "config", "users_config.json")
        auth_manager = QualityAuthManager(users_file)
        users = auth_manager.get_all_users()
        print(f"   ✅ Configuração de usuários carregada ({len(users)} usuários)")
        
    except Exception as e:
        print(f"   ❌ Erro ao carregar configurações: {e}")
        return False
    
    # Teste 6: Verificar scripts de inicialização
    print("\n6. Verificando scripts de inicialização...")
    scripts = [
        "start_server.bat",
        "start_attendant.bat",
        "start_admin.bat"
    ]
    
    for script in scripts:
        script_path = os.path.join(server_dir, script)
        if os.path.exists(script_path):
            print(f"   ✅ {script}")
        else:
            print(f"   ❌ {script} - NÃO ENCONTRADO")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    print("✅ A instalação está funcionando corretamente")
    print("✅ Todos os módulos podem ser importados")
    print("✅ Todas as configurações foram carregadas")
    print("✅ Todos os scripts estão disponíveis")
    print()
    print("🚀 O sistema está pronto para uso!")
    print("   Execute: C:\\Quality\\ControlPanel\\start_server.bat")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        if test_installation():
            print("\n✅ Instalação verificada com sucesso!")
        else:
            print("\n❌ Problemas encontrados na instalação")
            print("   Execute: python fix_installation.py")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
    
    input("\nPressione Enter para sair...")
