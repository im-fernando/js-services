#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação - Sistema Multi-Atendente
Instala e configura o sistema Quality com suporte a múltiplos atendentes
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List

def print_banner():
    """Exibe banner de instalação"""
    print("=" * 80)
    print("🚀 QUALITY REMOTE CONTROL SYSTEM - INSTALAÇÃO MULTI-ATENDENTE")
    print("=" * 80)
    print("Sistema de monitoramento e controle remoto")
    print("para serviços Quality com suporte a múltiplos atendentes")
    print("=" * 80)
    print()

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_server_dependencies():
    """Instala dependências do servidor"""
    print("\n📦 Instalando dependências do servidor...")
    
    try:
        # Verificar se pip está disponível
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Instalar dependências do servidor
        requirements_file = Path(__file__).parent / "servidor_control" / "requirements.txt"
        
        if requirements_file.exists():
            print("   Instalando dependências do servidor...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            print("✅ Dependências do servidor instaladas com sucesso")
        else:
            print("⚠️  Arquivo requirements.txt não encontrado")
            print("   Instalando dependências básicas...")
            
            basic_deps = [
                "websocket-server==0.4",
                "colorama==0.4.6",
                "rich==13.7.0",
                "requests==2.31.0"
            ]
            
            for dep in basic_deps:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            
            print("✅ Dependências básicas instaladas")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_server_installation_directory():
    """Cria diretório de instalação do servidor"""
    print("\n📁 Criando diretório de instalação do servidor...")
    
    install_dir = Path("C:\\Quality\\ControlPanel")
    
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Diretório criado: {install_dir}")
        return install_dir
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return None

def copy_server_files(install_dir: Path):
    """Copia arquivos do servidor"""
    print("\n📋 Copiando arquivos do servidor...")
    
    source_dir = Path(__file__).parent / "servidor_control"
    
    try:
        # Copiar arquivos principais
        files_to_copy = [
            "main.py",
            "requirements.txt"
        ]
        
        for file_name in files_to_copy:
            source_file = source_dir / file_name
            if source_file.exists():
                shutil.copy2(source_file, install_dir / file_name)
                print(f"   ✅ {file_name}")
        
        # Copiar diretórios
        dirs_to_copy = ["config", "core", "interface", "utils", "database"]
        
        for dir_name in dirs_to_copy:
            source_dir_path = source_dir / dir_name
            if source_dir_path.exists():
                dest_dir_path = install_dir / dir_name
                if dest_dir_path.exists():
                    shutil.rmtree(dest_dir_path)
                shutil.copytree(source_dir_path, dest_dir_path)
                print(f"   ✅ {dir_name}/")
        
        print("✅ Arquivos do servidor copiados com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao copiar arquivos: {e}")
        return False

def setup_initial_users():
    """Configura usuários iniciais"""
    print("\n👥 Configurando usuários iniciais...")
    
    try:
        # Verificar se arquivo de usuários existe
        users_config_file = Path("servidor_control/config/users_config.json")
        
        if users_config_file.exists():
            print("✅ Configuração de usuários encontrada")
            
            # Mostrar usuários padrão
            with open(users_config_file, 'r', encoding='utf-8') as f:
                users_config = json.load(f)
            
            print("\n👤 Usuários padrão configurados:")
            for attendant in users_config.get("attendants", []):
                print(f"   - {attendant['display_name']} ({attendant['username']})")
                print(f"     Papel: {attendant['role']}")
                print(f"     Senha padrão: quality123")
                print()
            
            print("⚠️  IMPORTANTE: Altere as senhas padrão após a instalação!")
            return True
        else:
            print("⚠️  Arquivo de configuração de usuários não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao configurar usuários: {e}")
        return False

def create_server_startup_scripts(install_dir: Path):
    """Cria scripts de inicialização do servidor"""
    print("\n🚀 Criando scripts de inicialização do servidor...")
    
    try:
        # Script batch para Windows - Servidor
        server_batch_content = f"""@echo off
echo Iniciando Quality Control Panel Server...
cd /d "{install_dir}"
python main.py --multi-attendant --quality-mode
pause
"""
        
        server_batch_file = install_dir / "start_server.bat"
        with open(server_batch_file, 'w', encoding='utf-8') as f:
            f.write(server_batch_content)
        
        print(f"✅ Script do servidor criado: {server_batch_file}")
        
        # Script para atendentes
        attendant_batch_content = f"""@echo off
echo Iniciando Interface de Atendente...
cd /d "{install_dir}"
python interface/attendant_cli.py
pause
"""
        
        attendant_batch_file = install_dir / "start_attendant.bat"
        with open(attendant_batch_file, 'w', encoding='utf-8') as f:
            f.write(attendant_batch_content)
        
        print(f"✅ Script de atendente criado: {attendant_batch_file}")
        
        # Script administrativo
        admin_batch_content = f"""@echo off
echo Iniciando Interface Administrativa...
cd /d "{install_dir}"
python interface/admin_cli.py
pause
"""
        
        admin_batch_file = install_dir / "start_admin.bat"
        with open(admin_batch_file, 'w', encoding='utf-8') as f:
            f.write(admin_batch_content)
        
        print(f"✅ Script administrativo criado: {admin_batch_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar scripts: {e}")
        return False

def create_uninstall_script(install_dir: Path):
    """Cria script de desinstalação"""
    print("\n🗑️  Criando script de desinstalação...")
    
    try:
        uninstall_content = f"""@echo off
echo Desinstalando Quality Control Panel...
echo.
echo Tem certeza que deseja remover o Quality Control Panel?
echo Pressione qualquer tecla para continuar ou Ctrl+C para cancelar...
pause >nul

echo Parando serviços...
taskkill /f /im python.exe 2>nul

echo Removendo arquivos...
cd /d "{install_dir.parent}"
rmdir /s /q "{install_dir.name}"

echo.
echo Quality Control Panel foi removido com sucesso!
pause
"""
        
        uninstall_file = install_dir / "uninstall.bat"
        with open(uninstall_file, 'w', encoding='utf-8') as f:
            f.write(uninstall_content)
        
        print(f"✅ Script de desinstalação criado: {uninstall_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar script de desinstalação: {e}")
        return False

def test_server_installation(install_dir: Path):
    """Testa a instalação do servidor"""
    print("\n🧪 Testando instalação do servidor...")
    
    try:
        # Testar importação dos módulos
        test_script = f"""
import sys
sys.path.append(r"{install_dir}")

try:
    from config.settings import load_config
    from core.server import QualityControlServer
    from core.session_manager import SessionManager
    from core.attendant_manager import AttendantManager
    from utils.auth import QualityAuthManager
    print("✅ Módulos do servidor importados com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar módulos: {{e}}")
    sys.exit(1)

# Testar carregamento de configuração
try:
    config = load_config(r"{install_dir}/config/server_config.json")
    print("✅ Configuração do servidor carregada com sucesso")
    print(f"   Host: {{config['server']['host']}}")
    print(f"   Porta: {{config['server']['port']}}")
    print(f"   Serviços Quality: {{len(config['quality_services'])}}")
except Exception as e:
    print(f"❌ Erro ao carregar configuração: {{e}}")
    sys.exit(1)

# Testar sistema de autenticação
try:
    auth_manager = QualityAuthManager(r"{install_dir}/config/users_config.json")
    users = auth_manager.get_all_users()
    print(f"✅ Sistema de autenticação funcionando - {{len(users)}} usuários")
except Exception as e:
    print(f"❌ Erro no sistema de autenticação: {{e}}")
    sys.exit(1)

print("✅ Teste de instalação do servidor concluído com sucesso!")
"""
        
        result = subprocess.run([
            sys.executable, "-c", test_script
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Teste de instalação do servidor passou")
            return True
        else:
            print("❌ Teste de instalação do servidor falhou")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def show_installation_summary(install_dir: Path):
    """Exibe resumo da instalação"""
    print("\n" + "=" * 80)
    print("🎉 INSTALAÇÃO MULTI-ATENDENTE CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print(f"📁 Diretório do Servidor: {install_dir}")
    print()
    print("🚀 COMO USAR O SISTEMA:")
    print()
    print("1. INICIAR O SERVIDOR:")
    print(f"   {install_dir}\\start_server.bat")
    print("   (Execute como Administrador)")
    print()
    print("2. CONECTAR ATENDENTES:")
    print(f"   {install_dir}\\start_attendant.bat")
    print("   (Execute para cada atendente)")
    print()
    print("3. ACESSAR PAINEL ADMINISTRATIVO:")
    print(f"   {install_dir}\\start_admin.bat")
    print("   (Apenas para administradores)")
    print()
    print("👤 USUÁRIOS PADRÃO:")
    print("   admin / admin123 (Administrador)")
    print("   joao.silva / quality123 (Suporte Sênior)")
    print("   maria.santos / quality123 (Suporte Júnior)")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Altere as senhas padrão após a instalação")
    print("   - Configure os IPs dos clientes no servidor")
    print("   - Instale o agente nos computadores dos clientes")
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Instalar agentes nos computadores dos clientes")
    print("2. Configurar rede e firewall")
    print("3. Testar conectividade")
    print("4. Treinar atendentes no sistema")
    print()
    print(f"🗑️  Para desinstalar: {install_dir}\\uninstall.bat")
    print("=" * 80)

def main():
    """Função principal de instalação"""
    print_banner()
    
    # Verificações iniciais
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return False
    
    # Instalar dependências do servidor
    if not install_server_dependencies():
        print("\n❌ Falha na instalação das dependências")
        input("\nPressione Enter para sair...")
        return False
    
    # Criar diretório de instalação
    install_dir = create_server_installation_directory()
    if not install_dir:
        input("\nPressione Enter para sair...")
        return False
    
    # Copiar arquivos
    if not copy_server_files(install_dir):
        input("\nPressione Enter para sair...")
        return False
    
    # Configurar usuários iniciais
    setup_initial_users()
    
    # Criar scripts
    create_server_startup_scripts(install_dir)
    create_uninstall_script(install_dir)
    
    # Testar instalação
    if not test_server_installation(install_dir):
        print("\n⚠️  Instalação concluída, mas teste falhou")
        print("   Verifique os logs para mais detalhes")
    
    # Resumo final
    show_installation_summary(install_dir)
    
    input("\nPressione Enter para finalizar...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado durante a instalação: {e}")
        input("\nPressione Enter para sair...")
