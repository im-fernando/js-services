#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação - Quality Remote Agent
Instala e configura o agente Quality com verificação de serviços instalados
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
    print("=" * 60)
    print("🚀 QUALITY REMOTE AGENT - INSTALAÇÃO")
    print("=" * 60)
    print("Sistema de monitoramento e controle remoto")
    print("para serviços Quality")
    print("=" * 60)
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

def check_quality_installation():
    """Verifica se o Quality está instalado"""
    print("\n🔍 Verificando instalação do Quality...")
    
    quality_paths = [
        "C:\\Quality",
        "D:\\Quality",
        "E:\\Quality"
    ]
    
    quality_found = False
    for path in quality_paths:
        if os.path.exists(path):
            print(f"✅ Quality encontrado em: {path}")
            quality_found = True
            break
    
    if not quality_found:
        print("⚠️  Quality não encontrado nos caminhos padrão")
        print("   Caminhos verificados:")
        for path in quality_paths:
            print(f"   - {path}")
        print("\n   Você pode continuar a instalação e configurar os caminhos manualmente.")
    
    return quality_found

def check_quality_services():
    """Verifica quais serviços Quality estão instalados"""
    print("\n🔧 Verificando serviços Quality instalados...")
    
    services_config = {
        "srvIntegraWeb": {
            "name": "IntegraWebService",
            "executable_path": "C:\\Quality\\web\\IntegraWebService.exe",
            "log_base_path": "C:\\Quality\\LOG\\Integra",
            "description": "Serviço de Integração Web do Quality"
        },
        "ServicoFiscal": {
            "name": "webPostoFiscalService",
            "executable_path": "C:\\Quality\\Services\\webPostoPayServer\\webPostoFiscalServer.exe",
            "log_base_path": "C:\\Quality\\LOG\\webPostoFiscalServer",
            "description": "Serviço Fiscal do WebPosto"
        },
        "ServicoAutomacao": {
            "name": "webPostoLeituraAutomacao",
            "executable_path": "C:\\Quality\\Services\\webPostoLeituraAutomacao\\webPostoLeituraAutomacao.exe",
            "log_base_path": "C:\\Quality\\LOG\\webPostoLeituraAutomacao",
            "description": "Serviço de Automação e Leitura"
        },
        "webPostoPayServer": {
            "name": "webPostoPayServer",
            "executable_path": "C:\\Quality\\Services\\webPostoPayServer\\winSW\\webPostoPaySW.exe",
            "log_base_path": "C:\\Quality\\LOG\\QualityPDV_PAF",
            "description": "Servidor de Pagamento WebPosto"
        },
        "QualityPulser": {
            "name": "QualityPulserWeb",
            "executable_path": "C:\\Quality\\PulserWeb.exe",
            "log_base_path": "C:\\Quality\\LOG\\WebPostoPulser",
            "description": "Quality Pulser Web Service"
        }
    }
    
    installed_services = []
    missing_services = []
    
    for service_id, service_info in services_config.items():
        executable_path = service_info["executable_path"]
        
        if os.path.exists(executable_path):
            print(f"✅ {service_info['name']} - Encontrado")
            installed_services.append({
                "name": service_id,
                "display_name": service_info["name"],
                "executable_path": executable_path,
                "log_base_path": service_info["log_base_path"],
                "log_structure": "nested_numeric_folders",
                "log_file_pattern": "*.txt",
                "description": service_info["description"],
                "enabled": True
            })
        else:
            print(f"❌ {service_info['name']} - Não encontrado")
            missing_services.append(service_info["name"])
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Serviços instalados: {len(installed_services)}")
    print(f"   ❌ Serviços não encontrados: {len(missing_services)}")
    
    if missing_services:
        print(f"\n⚠️  Serviços não encontrados:")
        for service in missing_services:
            print(f"   - {service}")
        print("\n   Estes serviços não serão monitorados.")
        print("   Você pode adicioná-los manualmente após a instalação.")
    
    return installed_services, missing_services

def get_client_configuration():
    """Obtém configuração do cliente"""
    print("\n⚙️  Configuração do Cliente")
    print("-" * 40)
    
    # ID do cliente
    while True:
        client_id = input("ID do Cliente (ex: QUALITY_CLIENTE_001): ").strip()
        if client_id and client_id.startswith("QUALITY_CLIENTE_"):
            break
        print("❌ ID deve começar com 'QUALITY_CLIENTE_'")
    
    # Nome do cliente
    client_name = input("Nome do Cliente (ex: Posto Quality - Terminal 01): ").strip()
    if not client_name:
        client_name = f"Cliente {client_id}"
    
    # Localização
    location = input("Localização (ex: Matriz, Filial 01): ").strip()
    if not location:
        location = "Não informado"
    
    # Servidor
    print("\n🌐 Configuração do Servidor")
    server_host = input("IP do Servidor (padrão: 192.168.1.100): ").strip()
    if not server_host:
        server_host = "192.168.1.100"
    
    server_port = input("Porta do Servidor (padrão: 8765): ").strip()
    if not server_port:
        server_port = "8765"
    
    try:
        server_port = int(server_port)
    except ValueError:
        server_port = 8765
    
    return {
        "client_id": client_id,
        "client_name": client_name,
        "location": location,
        "server_host": server_host,
        "server_port": server_port
    }

def create_client_config(installed_services: List[Dict[str, Any]], client_config: Dict[str, Any]) -> Dict[str, Any]:
    """Cria configuração do cliente"""
    config = {
        "services": installed_services,
        "server": {
            "host": client_config["server_host"],
            "port": client_config["server_port"],
            "reconnect_interval": 5,
            "heartbeat_interval": 30
        },
        "client": {
            "id": client_config["client_id"],
            "name": client_config["client_name"],
            "location": client_config["location"]
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
    
    return config

def install_dependencies():
    """Instala dependências Python"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Verificar se pip está disponível
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Instalar dependências
        requirements_file = Path(__file__).parent / "cliente_agent" / "requirements.txt"
        
        if requirements_file.exists():
            print("   Instalando dependências do cliente...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            print("✅ Dependências instaladas com sucesso")
        else:
            print("⚠️  Arquivo requirements.txt não encontrado")
            print("   Instalando dependências básicas...")
            
            basic_deps = [
                "websocket-client==1.6.4",
                "psutil==5.9.6",
                "requests==2.31.0",
                "colorama==0.4.6"
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

def create_installation_directory():
    """Cria diretório de instalação"""
    print("\n📁 Criando diretório de instalação...")
    
    install_dir = Path("C:\\Quality\\RemoteAgent")
    
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Diretório criado: {install_dir}")
        return install_dir
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return None

def copy_agent_files(install_dir: Path):
    """Copia arquivos do agente"""
    print("\n📋 Copiando arquivos do agente...")
    
    source_dir = Path(__file__).parent / "cliente_agent"
    
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
        dirs_to_copy = ["config", "core", "utils"]
        
        for dir_name in dirs_to_copy:
            source_dir_path = source_dir / dir_name
            if source_dir_path.exists():
                dest_dir_path = install_dir / dir_name
                if dest_dir_path.exists():
                    shutil.rmtree(dest_dir_path)
                shutil.copytree(source_dir_path, dest_dir_path)
                print(f"   ✅ {dir_name}/")
        
        print("✅ Arquivos copiados com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao copiar arquivos: {e}")
        return False

def save_client_config(install_dir: Path, config: Dict[str, Any]):
    """Salva configuração do cliente"""
    print("\n💾 Salvando configuração...")
    
    try:
        config_file = install_dir / "config" / "services_config.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Configuração salva: {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False

def create_startup_script(install_dir: Path):
    """Cria script de inicialização"""
    print("\n🚀 Criando script de inicialização...")
    
    try:
        # Script batch para Windows
        batch_content = f"""@echo off
echo Iniciando Quality Remote Agent...
cd /d "{install_dir}"
python main.py
pause
"""
        
        batch_file = install_dir / "start_agent.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Script criado: {batch_file}")
        
        # Script Python para inicialização
        python_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(r"{install_dir}")
os.chdir(r"{install_dir}")
from main import main
if __name__ == "__main__":
    main()
"""
        
        python_file = install_dir / "start_agent.py"
        with open(python_file, 'w', encoding='utf-8') as f:
            f.write(python_content)
        
        print(f"✅ Script Python criado: {python_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar scripts: {e}")
        return False

def create_uninstall_script(install_dir: Path):
    """Cria script de desinstalação"""
    print("\n🗑️  Criando script de desinstalação...")
    
    try:
        uninstall_content = f"""@echo off
echo Desinstalando Quality Remote Agent...
echo.
echo Tem certeza que deseja remover o Quality Remote Agent?
echo Pressione qualquer tecla para continuar ou Ctrl+C para cancelar...
pause >nul

echo Removendo arquivos...
cd /d "{install_dir.parent}"
rmdir /s /q "{install_dir.name}"

echo.
echo Quality Remote Agent foi removido com sucesso!
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

def test_installation(install_dir: Path):
    """Testa a instalação"""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testar importação dos módulos
        test_script = f"""
import sys
sys.path.append(r"{install_dir}")

try:
    from config.settings import load_config
    from core.agent import QualityAgent
    from utils.logger import setup_logger
    print("✅ Módulos importados com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar módulos: {{e}}")
    sys.exit(1)

# Testar carregamento de configuração
try:
    config = load_config(r"{install_dir}/config/services_config.json")
    print("✅ Configuração carregada com sucesso")
    print(f"   Cliente: {{config['client']['name']}}")
    print(f"   Serviços: {{len(config['services'])}}")
except Exception as e:
    print(f"❌ Erro ao carregar configuração: {{e}}")
    sys.exit(1)

print("✅ Teste de instalação concluído com sucesso!")
"""
        
        result = subprocess.run([
            sys.executable, "-c", test_script
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Teste de instalação passou")
            return True
        else:
            print("❌ Teste de instalação falhou")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal de instalação"""
    print_banner()
    
    # Verificações iniciais
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return False
    
    # Verificar instalação do Quality
    quality_found = check_quality_installation()
    
    # Verificar serviços instalados
    installed_services, missing_services = check_quality_services()
    
    if not installed_services:
        print("\n❌ Nenhum serviço Quality encontrado!")
        print("   Verifique se o Quality está instalado corretamente.")
        input("\nPressione Enter para sair...")
        return False
    
    # Obter configuração do cliente
    client_config = get_client_configuration()
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        input("\nPressione Enter para sair...")
        return False
    
    # Criar diretório de instalação
    install_dir = create_installation_directory()
    if not install_dir:
        input("\nPressione Enter para sair...")
        return False
    
    # Copiar arquivos
    if not copy_agent_files(install_dir):
        input("\nPressione Enter para sair...")
        return False
    
    # Criar configuração
    config = create_client_config(installed_services, client_config)
    
    # Salvar configuração
    if not save_client_config(install_dir, config):
        input("\nPressione Enter para sair...")
        return False
    
    # Criar scripts
    create_startup_script(install_dir)
    create_uninstall_script(install_dir)
    
    # Testar instalação
    if not test_installation(install_dir):
        print("\n⚠️  Instalação concluída, mas teste falhou")
        print("   Verifique os logs para mais detalhes")
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print(f"📁 Diretório: {install_dir}")
    print(f"👤 Cliente: {client_config['client_name']} ({client_config['client_id']})")
    print(f"🌐 Servidor: {client_config['server_host']}:{client_config['server_port']}")
    print(f"🔧 Serviços monitorados: {len(installed_services)}")
    
    if missing_services:
        print(f"⚠️  Serviços não encontrados: {len(missing_services)}")
    
    print("\n📋 Próximos passos:")
    print("1. Inicie o servidor de controle")
    print("2. Execute o agente: start_agent.bat")
    print("3. Verifique a conexão no painel de controle")
    
    print(f"\n🚀 Para iniciar o agente:")
    print(f"   {install_dir}\\start_agent.bat")
    
    print(f"\n🗑️  Para desinstalar:")
    print(f"   {install_dir}\\uninstall.bat")
    
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
