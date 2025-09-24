#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Completo - Sistema Quality Control Panel
Testa todos os componentes do sistema
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    """Exibe banner de teste"""
    print("=" * 70)
    print("🧪 QUALITY CONTROL PANEL - TESTE COMPLETO DO SISTEMA")
    print("=" * 70)
    print("Testando todos os componentes instalados")
    print("=" * 70)
    print()

def test_dependencies():
    """Testa dependências Python"""
    print("📦 Testando dependências Python...")
    
    deps = [
        ("websocket", "websocket-client"),
        ("websocket_server", "websocket-server"),
        ("colorama", "colorama"),
        ("rich", "rich"),
        ("requests", "requests")
    ]
    
    success = True
    for module, package in deps:
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NÃO INSTALADO")
            success = False
    
    return success

def test_directories():
    """Testa diretórios de instalação"""
    print("\n📁 Testando diretórios de instalação...")
    
    directories = [
        ("C:\\Quality\\ControlPanel", "Servidor"),
        ("C:\\Quality\\AttendantClient", "Atendentes"),
        ("C:\\Quality\\RemoteAgent", "Clientes"),
        ("C:\\Quality\\Documentation", "Documentação")
    ]
    
    success = True
    for directory, description in directories:
        if os.path.exists(directory):
            print(f"   ✅ {description}: {directory}")
        else:
            print(f"   ❌ {description}: {directory} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_server_files():
    """Testa arquivos do servidor"""
    print("\n🖥️  Testando arquivos do servidor...")
    
    server_files = [
        "main.py",
        "config/server_config.json",
        "config/users_config.json",
        "core/server.py",
        "core/session_manager.py",
        "core/attendant_manager.py",
        "utils/auth.py",
        "start_server.bat"
    ]
    
    success = True
    for file in server_files:
        file_path = os.path.join("C:\\Quality\\ControlPanel", file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_attendant_files():
    """Testa arquivos dos atendentes"""
    print("\n👥 Testando arquivos dos atendentes...")
    
    attendant_files = [
        "attendant_client.py",
        "start_attendant.bat"
    ]
    
    success = True
    for file in attendant_files:
        file_path = os.path.join("C:\\Quality\\AttendantClient", file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_client_files():
    """Testa arquivos dos clientes"""
    print("\n🖥️  Testando arquivos dos clientes...")
    
    client_files = [
        "quality_agent.py",
        "start_agent.bat"
    ]
    
    success = True
    for file in client_files:
        file_path = os.path.join("C:\\Quality\\RemoteAgent", file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_server_imports():
    """Testa imports do servidor"""
    print("\n🔍 Testando imports do servidor...")
    
    try:
        server_dir = "C:\\Quality\\ControlPanel"
        if os.path.exists(server_dir):
            sys.path.insert(0, server_dir)
            
            # Testar imports principais
            from config.settings import load_config
            print("   ✅ config.settings")
            
            from utils.auth import QualityAuthManager
            print("   ✅ utils.auth")
            
            from core.session_manager import SessionManager
            print("   ✅ core.session_manager")
            
            from core.attendant_manager import AttendantManager
            print("   ✅ core.attendant_manager")
            
            return True
        else:
            print("   ❌ Diretório do servidor não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao importar módulos do servidor: {e}")
        return False

def test_server_config():
    """Testa configuração do servidor"""
    print("\n⚙️  Testando configuração do servidor...")
    
    try:
        server_dir = "C:\\Quality\\ControlPanel"
        if os.path.exists(server_dir):
            sys.path.insert(0, server_dir)
            
            from config.settings import load_config
            
            # Testar configuração do servidor
            config_file = os.path.join(server_dir, "config", "server_config.json")
            if os.path.exists(config_file):
                config = load_config(config_file)
                print(f"   ✅ Configuração do servidor carregada")
                print(f"      Host: {config['server']['host']}")
                print(f"      Porta: {config['server']['port']}")
            else:
                print(f"   ❌ Arquivo de configuração não encontrado")
                return False
            
            # Testar configuração de usuários
            users_file = os.path.join(server_dir, "config", "users_config.json")
            if os.path.exists(users_file):
                from utils.auth import QualityAuthManager
                auth_manager = QualityAuthManager(users_file)
                users = auth_manager.get_all_users()
                print(f"   ✅ Configuração de usuários carregada ({len(users)} usuários)")
            else:
                print(f"   ❌ Arquivo de usuários não encontrado")
                return False
            
            return True
        else:
            print("   ❌ Diretório do servidor não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao testar configurações: {e}")
        return False

def test_network_connectivity():
    """Testa conectividade de rede"""
    print("\n🌐 Testando conectividade de rede...")
    
    try:
        import socket
        
        # Testar porta 8765 (porta padrão do servidor)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Tentar conectar na porta local
        result = sock.connect_ex(('localhost', 8765))
        sock.close()
        
        if result == 0:
            print("   ✅ Porta 8765 está em uso (servidor pode estar rodando)")
        else:
            print("   ℹ️  Porta 8765 está livre (servidor não está rodando)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao testar conectividade: {e}")
        return False

def test_python_scripts():
    """Testa scripts Python"""
    print("\n🐍 Testando scripts Python...")
    
    scripts = [
        ("C:\\Quality\\ControlPanel\\main.py", "Servidor"),
        ("C:\\Quality\\AttendantClient\\attendant_client.py", "Atendente"),
        ("C:\\Quality\\RemoteAgent\\quality_agent.py", "Cliente")
    ]
    
    success = True
    for script_path, description in scripts:
        if os.path.exists(script_path):
            try:
                # Testar sintaxe do script
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_content = f.read()
                
                # Compilar para verificar sintaxe
                compile(script_content, script_path, 'exec')
                print(f"   ✅ {description}: {os.path.basename(script_path)}")
                
            except SyntaxError as e:
                print(f"   ❌ {description}: Erro de sintaxe em {os.path.basename(script_path)}")
                print(f"      Linha {e.lineno}: {e.msg}")
                success = False
            except Exception as e:
                print(f"   ❌ {description}: Erro ao testar {os.path.basename(script_path)}: {e}")
                success = False
        else:
            print(f"   ❌ {description}: {os.path.basename(script_path)} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_batch_scripts():
    """Testa scripts batch"""
    print("\n📜 Testando scripts batch...")
    
    batch_scripts = [
        ("C:\\Quality\\ControlPanel\\start_server.bat", "Servidor"),
        ("C:\\Quality\\AttendantClient\\start_attendant.bat", "Atendente"),
        ("C:\\Quality\\RemoteAgent\\start_agent.bat", "Cliente")
    ]
    
    success = True
    for script_path, description in batch_scripts:
        if os.path.exists(script_path):
            print(f"   ✅ {description}: {os.path.basename(script_path)}")
        else:
            print(f"   ❌ {description}: {os.path.basename(script_path)} - NÃO ENCONTRADO")
            success = False
    
    return success

def test_documentation():
    """Testa documentação"""
    print("\n📚 Testando documentação...")
    
    doc_files = [
        "README.txt"
    ]
    
    success = True
    for file in doc_files:
        file_path = os.path.join("C:\\Quality\\Documentation", file)
        if os.path.exists(file_path):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO ENCONTRADO")
            success = False
    
    return success

def run_comprehensive_test():
    """Executa teste abrangente"""
    print("🚀 Executando teste abrangente...")
    
    tests = [
        ("Dependências Python", test_dependencies),
        ("Diretórios de Instalação", test_directories),
        ("Arquivos do Servidor", test_server_files),
        ("Arquivos dos Atendentes", test_attendant_files),
        ("Arquivos dos Clientes", test_client_files),
        ("Imports do Servidor", test_server_imports),
        ("Configuração do Servidor", test_server_config),
        ("Conectividade de Rede", test_network_connectivity),
        ("Scripts Python", test_python_scripts),
        ("Scripts Batch", test_batch_scripts),
        ("Documentação", test_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    return results

def main():
    """Função principal"""
    print_banner()
    
    # Executar testes
    results = run_comprehensive_test()
    
    # Resumo dos resultados
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print("=" * 70)
    print(f"📈 RESULTADO GERAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está funcionando corretamente")
        print("✅ Todos os componentes estão instalados")
        print("✅ Todas as configurações estão corretas")
        print()
        print("🚀 O sistema está pronto para uso!")
        print("   Execute: C:\\Quality\\ControlPanel\\start_server.bat")
    elif passed >= total * 0.8:
        print("⚠️  MAIORIA DOS TESTES PASSOU")
        print("✅ O sistema está funcionando com pequenos problemas")
        print("⚠️  Verifique os itens que falharam")
        print("💡 O sistema pode funcionar normalmente")
    else:
        print("❌ MUITOS TESTES FALHARAM")
        print("❌ O sistema pode não estar funcionando corretamente")
        print("🔧 Execute: python fix_installation.py")
        print("🔄 Ou reinstale o sistema")
    
    print("=" * 70)
    
    input("\nPressione Enter para finalizar...")
    return passed == total

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado durante o teste: {e}")
        input("\nPressione Enter para sair...")
