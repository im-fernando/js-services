#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação - Cliente Atendente
Instala apenas a interface de atendente nos computadores dos atendentes
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de instalação"""
    print("=" * 70)
    print("👥 QUALITY CONTROL PANEL - INSTALAÇÃO ATENDENTE")
    print("=" * 70)
    print("Interface de atendente para conexão com o servidor")
    print("=" * 70)
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

def install_dependencies():
    """Instala dependências mínimas"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Dependências mínimas para o cliente atendente
        deps = [
            "websocket-client==1.6.4",
            "colorama==0.4.6"
        ]
        
        for dep in deps:
            print(f"   Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
        
        print("✅ Dependências instaladas com sucesso")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_installation_directory():
    """Cria diretório de instalação"""
    print("\n📁 Criando diretório de instalação...")
    
    install_dir = Path("C:\\Quality\\AttendantClient")
    
    try:
        install_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Diretório criado: {install_dir}")
        return install_dir
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return None

def copy_attendant_files(install_dir: Path):
    """Copia arquivos necessários para o atendente"""
    print("\n📋 Copiando arquivos do atendente...")
    
    try:
        # Copiar interface de atendente
        source_file = Path(__file__).parent / "servidor_control" / "interface" / "attendant_cli.py"
        if source_file.exists():
            shutil.copy2(source_file, install_dir / "attendant_cli.py")
            print("   ✅ attendant_cli.py")
        else:
            print("   ❌ attendant_cli.py não encontrado")
            return False
        
        # Copiar utils necessários
        utils_source = Path(__file__).parent / "servidor_control" / "utils"
        utils_dest = install_dir / "utils"
        
        if utils_source.exists():
            if utils_dest.exists():
                shutil.rmtree(utils_dest)
            shutil.copytree(utils_source, utils_dest)
            print("   ✅ utils/")
        
        # Copiar config de usuários (para autenticação local)
        config_source = Path(__file__).parent / "servidor_control" / "config" / "users_config.json"
        config_dest = install_dir / "config"
        
        if config_source.exists():
            config_dest.mkdir(exist_ok=True)
            shutil.copy2(config_source, config_dest / "users_config.json")
            print("   ✅ config/users_config.json")
        
        print("✅ Arquivos copiados com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao copiar arquivos: {e}")
        return False

def create_startup_script(install_dir: Path, server_host: str, server_port: int):
    """Cria script de inicialização"""
    print("\n🚀 Criando script de inicialização...")
    
    try:
        # Script batch para Windows
        batch_content = f"""@echo off
echo Iniciando Quality Control Panel - Atendente...
cd /d "{install_dir}"
python attendant_cli.py --server {server_host}:{server_port}
pause
"""
        
        batch_file = install_dir / "start_attendant.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Script criado: {batch_file}")
        
        # Script Python alternativo
        python_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(r"{install_dir}")
os.chdir(r"{install_dir}")
from attendant_cli import main
if __name__ == "__main__":
    main()
"""
        
        python_file = install_dir / "start_attendant.py"
        with open(python_file, 'w', encoding='utf-8') as f:
            f.write(python_content)
        
        print(f"✅ Script Python criado: {python_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar scripts: {e}")
        return False

def get_server_configuration():
    """Obtém configuração do servidor"""
    print("\n🌐 Configuração do Servidor")
    print("-" * 40)
    
    # IP do servidor
    server_host = input("IP do Servidor (ex: 192.168.1.100): ").strip()
    if not server_host:
        server_host = "192.168.1.100"
    
    # Porta do servidor
    server_port = input("Porta do Servidor (padrão: 8765): ").strip()
    if not server_port:
        server_port = "8765"
    
    try:
        server_port = int(server_port)
    except ValueError:
        server_port = 8765
    
    return server_host, server_port

def test_connection(server_host: str, server_port: int):
    """Testa conexão com o servidor"""
    print(f"\n🔍 Testando conexão com {server_host}:{server_port}...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((server_host, server_port))
        sock.close()
        
        if result == 0:
            print("✅ Conexão com servidor OK")
            return True
        else:
            print("❌ Não foi possível conectar ao servidor")
            print("   Verifique se o servidor está rodando e acessível")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
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
    from attendant_cli import AttendantCLI
    print("✅ Interface de atendente importada com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar interface: {{e}}")
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

def show_installation_summary(install_dir: Path, server_host: str, server_port: int):
    """Exibe resumo da instalação"""
    print("\n" + "=" * 70)
    print("🎉 INSTALAÇÃO DO ATENDENTE CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print(f"📁 Diretório: {install_dir}")
    print(f"🌐 Servidor: {server_host}:{server_port}")
    print()
    print("🚀 COMO USAR:")
    print(f"   {install_dir}\\start_attendant.bat")
    print()
    print("👤 USUÁRIOS DISPONÍVEIS:")
    print("   admin / admin123 (Administrador)")
    print("   joao.silva / quality123 (Suporte Sênior)")
    print("   maria.santos / quality123 (Suporte Júnior)")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Altere as senhas padrão após o primeiro login")
    print("   - Certifique-se de que o servidor está rodando")
    print("   - Verifique a conectividade de rede")
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Execute o script de inicialização")
    print("2. Faça login com suas credenciais")
    print("3. Conecte-se ao servidor")
    print("4. Comece a gerenciar os clientes Quality")
    print("=" * 70)

def main():
    """Função principal de instalação"""
    print_banner()
    
    # Verificações iniciais
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return False
    
    # Obter configuração do servidor
    server_host, server_port = get_server_configuration()
    
    # Testar conexão
    if not test_connection(server_host, server_port):
        print("\n⚠️  Continuando instalação mesmo sem conexão...")
        print("   Você pode testar a conexão depois")
    
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
    if not copy_attendant_files(install_dir):
        input("\nPressione Enter para sair...")
        return False
    
    # Criar scripts
    create_startup_script(install_dir, server_host, server_port)
    
    # Testar instalação
    if not test_installation(install_dir):
        print("\n⚠️  Instalação concluída, mas teste falhou")
        print("   Verifique os logs para mais detalhes")
    
    # Resumo final
    show_installation_summary(install_dir, server_host, server_port)
    
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
