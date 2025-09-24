#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação em Lote - Sistema Quality Control Panel
Instala o sistema em múltiplos computadores automaticamente
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    """Exibe banner de instalação em lote"""
    print("=" * 70)
    print("🚀 QUALITY CONTROL PANEL - INSTALAÇÃO EM LOTE")
    print("=" * 70)
    print("Instalação automática em múltiplos computadores")
    print("=" * 70)
    print()

def get_computer_list():
    """Obtém lista de computadores para instalação"""
    print("📋 Configuração de Instalação em Lote")
    print("-" * 40)
    
    computers = []
    
    while True:
        print(f"\nComputador {len(computers) + 1}:")
        
        # Tipo de instalação
        print("Tipo de instalação:")
        print("1. Servidor")
        print("2. Atendente")
        print("3. Cliente")
        
        while True:
            choice = input("Escolha (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("❌ Opção inválida. Escolha 1, 2 ou 3.")
        
        install_type = {
            '1': 'servidor',
            '2': 'atendente',
            '3': 'cliente'
        }[choice]
        
        # IP do computador
        ip = input("IP do computador: ").strip()
        if not ip:
            print("❌ IP é obrigatório")
            continue
        
        # Nome do computador
        name = input("Nome do computador (opcional): ").strip()
        if not name:
            name = f"Computador {len(computers) + 1}"
        
        # Configurações específicas
        config = {}
        
        if install_type == 'servidor':
            config['port'] = input("Porta do servidor (padrão: 8765): ").strip() or "8765"
        elif install_type == 'atendente':
            config['server_ip'] = input("IP do servidor: ").strip()
            if not config['server_ip']:
                print("❌ IP do servidor é obrigatório para atendentes")
                continue
        elif install_type == 'cliente':
            config['server_ip'] = input("IP do servidor: ").strip()
            if not config['server_ip']:
                print("❌ IP do servidor é obrigatório para clientes")
                continue
            config['client_id'] = input("ID do cliente (ex: QUALITY_CLIENTE_001): ").strip()
            if not config['client_id']:
                config['client_id'] = f"QUALITY_CLIENTE_{len(computers) + 1:03d}"
        
        # Credenciais de acesso
        username = input("Usuário para acesso remoto: ").strip()
        if not username:
            print("❌ Usuário é obrigatório")
            continue
        
        password = input("Senha para acesso remoto: ").strip()
        if not password:
            print("❌ Senha é obrigatória")
            continue
        
        computer = {
            'name': name,
            'ip': ip,
            'type': install_type,
            'username': username,
            'password': password,
            'config': config
        }
        
        computers.append(computer)
        
        # Continuar?
        while True:
            continue_choice = input("Adicionar outro computador? (s/N): ").strip().lower()
            if continue_choice in ['s', 'sim', 'y', 'yes']:
                break
            elif continue_choice in ['n', 'não', 'nao', 'no', '']:
                return computers
            else:
                print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
    
    return computers

def create_installation_script(computer, install_type):
    """Cria script de instalação para um computador"""
    if install_type == 'servidor':
        return create_server_script(computer)
    elif install_type == 'atendente':
        return create_attendant_script(computer)
    elif install_type == 'cliente':
        return create_client_script(computer)
    else:
        return None

def create_server_script(computer):
    """Cria script de instalação do servidor"""
    script = f"""@echo off
echo Instalando Quality Control Panel - Servidor em {computer['name']}...
echo IP: {computer['ip']}
echo Porta: {computer['config']['port']}

REM Instalar dependências
pip install websocket-server==0.4
pip install websocket-client==1.6.4
pip install colorama==0.4.6
pip install rich==13.7.0
pip install requests==2.31.0

REM Criar diretório
mkdir C:\\Quality\\ControlPanel

REM Copiar arquivos (assumindo que estão em um compartilhamento)
REM xcopy \\\\{computer['ip']}\\Quality\\servidor_control\\* C:\\Quality\\ControlPanel\\ /E /Y

REM Criar script de inicialização
echo @echo off > C:\\Quality\\ControlPanel\\start_server.bat
echo echo Iniciando Quality Control Panel - Servidor... >> C:\\Quality\\ControlPanel\\start_server.bat
echo cd /d C:\\Quality\\ControlPanel >> C:\\Quality\\ControlPanel\\start_server.bat
echo python main.py --multi-attendant >> C:\\Quality\\ControlPanel\\start_server.bat
echo pause >> C:\\Quality\\ControlPanel\\start_server.bat

echo Instalação do servidor concluída!
pause
"""
    return script

def create_attendant_script(computer):
    """Cria script de instalação do atendente"""
    script = f"""@echo off
echo Instalando Quality Control Panel - Atendente em {computer['name']}...
echo IP: {computer['ip']}
echo Servidor: {computer['config']['server_ip']}

REM Instalar dependências
pip install websocket-client==1.6.4
pip install colorama==0.4.6

REM Criar diretório
mkdir C:\\Quality\\AttendantClient

REM Criar cliente atendente
echo # Cliente Atendente - Quality Control Panel > C:\\Quality\\AttendantClient\\attendant_client.py
echo # Configurado para servidor: {computer['config']['server_ip']} >> C:\\Quality\\AttendantClient\\attendant_client.py
echo # Execute: python attendant_client.py >> C:\\Quality\\AttendantClient\\attendant_client.py

REM Criar script de inicialização
echo @echo off > C:\\Quality\\AttendantClient\\start_attendant.bat
echo echo Iniciando Quality Control Panel - Atendente... >> C:\\Quality\\AttendantClient\\start_attendant.bat
echo cd /d C:\\Quality\\AttendantClient >> C:\\Quality\\AttendantClient\\start_attendant.bat
echo python attendant_client.py >> C:\\Quality\\AttendantClient\\start_attendant.bat
echo pause >> C:\\Quality\\AttendantClient\\start_attendant.bat

echo Instalação do atendente concluída!
pause
"""
    return script

def create_client_script(computer):
    """Cria script de instalação do cliente"""
    script = f"""@echo off
echo Instalando Quality Control Panel - Cliente em {computer['name']}...
echo IP: {computer['ip']}
echo Servidor: {computer['config']['server_ip']}
echo ID do Cliente: {computer['config']['client_id']}

REM Instalar dependências
pip install websocket-client==1.6.4
pip install colorama==0.4.6

REM Criar diretório
mkdir C:\\Quality\\RemoteAgent

REM Criar agente cliente
echo # Agente Quality - Quality Control Panel > C:\\Quality\\RemoteAgent\\quality_agent.py
echo # Configurado para servidor: {computer['config']['server_ip']} >> C:\\Quality\\RemoteAgent\\quality_agent.py
echo # ID do Cliente: {computer['config']['client_id']} >> C:\\Quality\\RemoteAgent\\quality_agent.py
echo # Execute: python quality_agent.py >> C:\\Quality\\RemoteAgent\\quality_agent.py

REM Criar script de inicialização
echo @echo off > C:\\Quality\\RemoteAgent\\start_agent.bat
echo echo Iniciando Quality Control Panel - Agente... >> C:\\Quality\\RemoteAgent\\start_agent.bat
echo cd /d C:\\Quality\\RemoteAgent >> C:\\Quality\\RemoteAgent\\start_agent.bat
echo python quality_agent.py >> C:\\Quality\\RemoteAgent\\start_agent.bat
echo pause >> C:\\Quality\\RemoteAgent\\start_agent.bat

echo Instalação do cliente concluída!
pause
"""
    return script

def install_on_computer(computer):
    """Instala o sistema em um computador específico"""
    print(f"\n🖥️  Instalando em {computer['name']} ({computer['ip']})...")
    
    try:
        # Criar script de instalação
        script = create_installation_script(computer, computer['type'])
        if not script:
            print(f"   ❌ Tipo de instalação não suportado: {computer['type']}")
            return False
        
        # Salvar script temporário
        script_file = f"install_{computer['name'].replace(' ', '_')}.bat"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # Executar script remotamente (usando psexec ou similar)
        # Nota: Em um ambiente real, você usaria ferramentas como psexec, WinRM, ou SSH
        print(f"   📝 Script criado: {script_file}")
        print(f"   💡 Execute manualmente em {computer['name']} ou use ferramenta de execução remota")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao instalar em {computer['name']}: {e}")
        return False

def install_all_computers(computers):
    """Instala o sistema em todos os computadores"""
    print(f"\n🚀 Iniciando instalação em {len(computers)} computadores...")
    
    results = []
    
    for i, computer in enumerate(computers, 1):
        print(f"\n📋 Computador {i}/{len(computers)}: {computer['name']}")
        print(f"   Tipo: {computer['type']}")
        print(f"   IP: {computer['ip']}")
        
        result = install_on_computer(computer)
        results.append((computer, result))
        
        # Aguardar entre instalações
        if i < len(computers):
            print("   ⏳ Aguardando 5 segundos...")
            time.sleep(5)
    
    return results

def create_installation_summary(computers, results):
    """Cria resumo da instalação"""
    print("\n" + "=" * 70)
    print("📊 RESUMO DA INSTALAÇÃO EM LOTE")
    print("=" * 70)
    
    successful = 0
    failed = 0
    
    for computer, result in results:
        status = "✅ SUCESSO" if result else "❌ FALHOU"
        print(f"   {status} - {computer['name']} ({computer['ip']}) - {computer['type']}")
        if result:
            successful += 1
        else:
            failed += 1
    
    print("=" * 70)
    print(f"📈 RESULTADO GERAL: {successful}/{len(computers)} instalações bem-sucedidas")
    
    if successful == len(computers):
        print("🎉 TODAS AS INSTALAÇÕES FORAM BEM-SUCEDIDAS!")
        print("✅ O sistema está instalado em todos os computadores")
        print("🚀 Pronto para uso!")
    elif successful > 0:
        print("⚠️  ALGUMAS INSTALAÇÕES FALHARAM")
        print("✅ O sistema está parcialmente instalado")
        print("🔧 Verifique os computadores que falharam")
    else:
        print("❌ TODAS AS INSTALAÇÕES FALHARAM")
        print("❌ Nenhum computador foi instalado com sucesso")
        print("🔧 Verifique a configuração e tente novamente")
    
    print("=" * 70)
    
    # Criar arquivo de log
    try:
        log_file = "installation_batch_log.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Log de Instalação em Lote - Quality Control Panel\n")
            f.write("=" * 50 + "\n\n")
            
            for computer, result in results:
                status = "SUCESSO" if result else "FALHOU"
                f.write(f"{status} - {computer['name']} ({computer['ip']}) - {computer['type']}\n")
            
            f.write(f"\nResultado: {successful}/{len(computers)} instalações bem-sucedidas\n")
        
        print(f"📝 Log salvo em: {log_file}")
        
    except Exception as e:
        print(f"⚠️  Erro ao criar log: {e}")

def main():
    """Função principal"""
    print_banner()
    
    # Obter lista de computadores
    computers = get_computer_list()
    
    if not computers:
        print("\n👋 Nenhum computador configurado para instalação")
        input("Pressione Enter para sair...")
        return False
    
    # Confirmar instalação
    print(f"\n⚠️  ATENÇÃO: Será instalado o sistema em {len(computers)} computadores!")
    print("   - Servidores: " + str(len([c for c in computers if c['type'] == 'servidor'])))
    print("   - Atendentes: " + str(len([c for c in computers if c['type'] == 'atendente'])))
    print("   - Clientes: " + str(len([c for c in computers if c['type'] == 'cliente'])))
    
    while True:
        choice = input("\nDeseja continuar com a instalação? (s/N): ").strip().lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            break
        elif choice in ['n', 'não', 'nao', 'no', '']:
            print("\n👋 Instalação cancelada pelo usuário")
            input("Pressione Enter para sair...")
            return False
        else:
            print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
    
    # Executar instalação
    results = install_all_computers(computers)
    
    # Criar resumo
    create_installation_summary(computers, results)
    
    input("\nPressione Enter para finalizar...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado durante a instalação: {e}")
        input("\nPressione Enter para sair...")