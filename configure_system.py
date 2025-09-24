#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Configuração Automática - Sistema Quality Control Panel
Configura automaticamente o sistema após a instalação
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de configuração"""
    print("=" * 70)
    print("⚙️  QUALITY CONTROL PANEL - CONFIGURAÇÃO AUTOMÁTICA")
    print("=" * 70)
    print("Configuração automática do sistema após instalação")
    print("=" * 70)
    print()

def get_system_info():
    """Obtém informações do sistema"""
    print("📋 Coletando informações do sistema...")
    
    try:
        # Nome do computador
        computer_name = os.environ.get('COMPUTERNAME', 'Desconhecido')
        print(f"   ✅ Nome do computador: {computer_name}")
        
        # IP do computador
        ip = get_local_ip()
        print(f"   ✅ IP local: {ip}")
        
        # Usuário atual
        username = os.environ.get('USERNAME', 'Desconhecido')
        print(f"   ✅ Usuário atual: {username}")
        
        # Diretório de instalação
        install_dir = "C:\\Quality\\ControlPanel"
        if os.path.exists(install_dir):
            print(f"   ✅ Diretório de instalação: {install_dir}")
        else:
            print(f"   ❌ Diretório de instalação não encontrado: {install_dir}")
            return None
        
        return {
            'computer_name': computer_name,
            'ip': ip,
            'username': username,
            'install_dir': install_dir
        }
        
    except Exception as e:
        print(f"❌ Erro ao coletar informações: {e}")
        return None

def get_local_ip():
    """Obtém IP local do computador"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def configure_server(server_info):
    """Configura o servidor"""
    print("\n🖥️  Configurando servidor...")
    
    try:
        # Configurar server_config.json
        server_config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8765,
                "name": f"Servidor {server_info['computer_name']}",
                "description": "Servidor Quality Control Panel"
            },
            "quality_services": [
                {
                    "name": "srvIntegraWeb",
                    "display_name": "Serviço Integração Web",
                    "executable_path": "C:\\Quality\\srvIntegraWeb.exe",
                    "log_base_path": "C:\\Quality\\LOG\\srvIntegraWeb",
                    "log_structure": "numeric",
                    "log_file_pattern": "*.txt",
                    "description": "Serviço de integração web"
                },
                {
                    "name": "srvIntegraFiscal",
                    "display_name": "Serviço Integração Fiscal",
                    "executable_path": "C:\\Quality\\srvIntegraFiscal.exe",
                    "log_base_path": "C:\\Quality\\LOG\\srvIntegraFiscal",
                    "log_structure": "numeric",
                    "log_file_pattern": "*.txt",
                    "description": "Serviço de integração fiscal"
                },
                {
                    "name": "srvIntegraContabil",
                    "display_name": "Serviço Integração Contábil",
                    "executable_path": "C:\\Quality\\srvIntegraContabil.exe",
                    "log_base_path": "C:\\Quality\\LOG\\srvIntegraContabil",
                    "log_structure": "numeric",
                    "log_file_pattern": "*.txt",
                    "description": "Serviço de integração contábil"
                },
                {
                    "name": "srvIntegraEstoque",
                    "display_name": "Serviço Integração Estoque",
                    "executable_path": "C:\\Quality\\srvIntegraEstoque.exe",
                    "log_base_path": "C:\\Quality\\LOG\\srvIntegraEstoque",
                    "log_structure": "numeric",
                    "log_file_pattern": "*.txt",
                    "description": "Serviço de integração estoque"
                },
                {
                    "name": "srvIntegraFinanceiro",
                    "display_name": "Serviço Integração Financeiro",
                    "executable_path": "C:\\Quality\\srvIntegraFinanceiro.exe",
                    "log_base_path": "C:\\Quality\\LOG\\srvIntegraFinanceiro",
                    "log_structure": "numeric",
                    "log_file_pattern": "*.txt",
                    "description": "Serviço de integração financeiro"
                }
            ],
            "log_monitoring": {
                "enabled": True,
                "max_lines": 1000,
                "refresh_interval": 5
            }
        }
        
        config_file = os.path.join(server_info['install_dir'], "config", "server_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(server_config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Configuração do servidor salva: {config_file}")
        
        # Configurar users_config.json
        users_config = {
            "attendants": [
                {
                    "id": "ATD001",
                    "username": "admin",
                    "display_name": "Administrador",
                    "password_hash": "sha256_hash_here",
                    "role": "administrator",
                    "permissions": {
                        "can_restart_services": True,
                        "can_kill_processes": True,
                        "can_view_logs": True,
                        "can_manage_all_clients": True,
                        "can_perform_critical_actions": True,
                        "can_manage_attendants": True,
                        "can_view_all_sessions": True
                    },
                    "assigned_clients": ["*"],
                    "shift": "any",
                    "created_at": "2025-01-22T08:00:00Z"
                },
                {
                    "id": "ATD002",
                    "username": "joao.silva",
                    "display_name": "João Silva",
                    "password_hash": "sha256_hash_here",
                    "role": "senior_support",
                    "permissions": {
                        "can_restart_services": True,
                        "can_kill_processes": True,
                        "can_view_logs": True,
                        "can_manage_all_clients": True,
                        "can_perform_critical_actions": True
                    },
                    "assigned_clients": ["*"],
                    "shift": "morning",
                    "created_at": "2025-01-22T08:00:00Z"
                },
                {
                    "id": "ATD003",
                    "username": "maria.santos",
                    "display_name": "Maria Santos",
                    "password_hash": "sha256_hash_here",
                    "role": "junior_support",
                    "permissions": {
                        "can_restart_services": True,
                        "can_kill_processes": False,
                        "can_view_logs": True,
                        "can_manage_all_clients": False,
                        "can_perform_critical_actions": False
                    },
                    "assigned_clients": ["QUALITY_CLIENTE_001", "QUALITY_CLIENTE_002"],
                    "shift": "afternoon",
                    "created_at": "2025-01-22T08:00:00Z"
                }
            ],
            "roles": {
                "administrator": {
                    "description": "Acesso total ao sistema",
                    "level": 3
                },
                "senior_support": {
                    "description": "Suporte sênior com acesso amplo",
                    "level": 2
                },
                "junior_support": {
                    "description": "Suporte júnior com acesso limitado",
                    "level": 1
                }
            }
        }
        
        users_file = os.path.join(server_info['install_dir'], "config", "users_config.json")
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users_config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Configuração de usuários salva: {users_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar servidor: {e}")
        return False

def configure_attendant(attendant_info):
    """Configura o atendente"""
    print("\n👥 Configurando atendente...")
    
    try:
        # Configurar cliente atendente
        attendant_dir = "C:\\Quality\\AttendantClient"
        if not os.path.exists(attendant_dir):
            print(f"   ❌ Diretório do atendente não encontrado: {attendant_dir}")
            return False
        
        # Configurar servidor padrão
        server_ip = input("IP do servidor (padrão: 192.168.1.100): ").strip()
        if not server_ip:
            server_ip = "192.168.1.100"
        
        server_port = input("Porta do servidor (padrão: 8765): ").strip()
        if not server_port:
            server_port = "8765"
        
        # Criar arquivo de configuração
        config = {
            "server": {
                "host": server_ip,
                "port": int(server_port)
            },
            "attendant": {
                "name": attendant_info['username'],
                "computer": attendant_info['computer_name']
            }
        }
        
        config_file = os.path.join(attendant_dir, "config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Configuração do atendente salva: {config_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar atendente: {e}")
        return False

def configure_client(client_info):
    """Configura o cliente"""
    print("\n🖥️  Configurando cliente...")
    
    try:
        # Configurar agente cliente
        client_dir = "C:\\Quality\\RemoteAgent"
        if not os.path.exists(client_dir):
            print(f"   ❌ Diretório do cliente não encontrado: {client_dir}")
            return False
        
        # Configurar servidor padrão
        server_ip = input("IP do servidor (padrão: 192.168.1.100): ").strip()
        if not server_ip:
            server_ip = "192.168.1.100"
        
        server_port = input("Porta do servidor (padrão: 8765): ").strip()
        if not server_port:
            server_port = "8765"
        
        # ID do cliente
        client_id = input(f"ID do cliente (padrão: QUALITY_CLIENTE_{client_info['computer_name']}): ").strip()
        if not client_id:
            client_id = f"QUALITY_CLIENTE_{client_info['computer_name']}"
        
        # Nome do cliente
        client_name = input(f"Nome do cliente (padrão: {client_info['computer_name']}): ").strip()
        if not client_name:
            client_name = client_info['computer_name']
        
        # Criar arquivo de configuração
        config = {
            "server": {
                "host": server_ip,
                "port": int(server_port)
            },
            "client": {
                "id": client_id,
                "name": client_name,
                "location": "Local",
                "computer": client_info['computer_name']
            }
        }
        
        config_file = os.path.join(client_dir, "config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Configuração do cliente salva: {config_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar cliente: {e}")
        return False

def configure_firewall():
    """Configura firewall para permitir conexões"""
    print("\n🔥 Configurando firewall...")
    
    try:
        # Permitir porta 8765 no firewall
        result = subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            "name=Quality Control Panel",
            "dir=in",
            "action=allow",
            "protocol=TCP",
            "localport=8765"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Regra de firewall adicionada para porta 8765")
        else:
            print("   ⚠️  Erro ao configurar firewall (pode já estar configurado)")
            print(f"      {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar firewall: {e}")
        return False

def configure_services():
    """Configura serviços Windows"""
    print("\n🔧 Configurando serviços Windows...")
    
    try:
        # Verificar se os serviços Quality existem
        quality_services = [
            "srvIntegraWeb",
            "srvIntegraFiscal",
            "srvIntegraContabil",
            "srvIntegraEstoque",
            "srvIntegraFinanceiro"
        ]
        
        existing_services = []
        for service in quality_services:
            try:
                result = subprocess.run([
                    "sc", "query", service
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    existing_services.append(service)
                    print(f"   ✅ Serviço encontrado: {service}")
                else:
                    print(f"   ℹ️  Serviço não encontrado: {service}")
                    
            except Exception as e:
                print(f"   ⚠️  Erro ao verificar serviço {service}: {e}")
        
        if existing_services:
            print(f"   📊 Total de serviços Quality encontrados: {len(existing_services)}")
        else:
            print("   ⚠️  Nenhum serviço Quality encontrado")
            print("      Configure os serviços Quality manualmente se necessário")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar serviços: {e}")
        return False

def create_startup_scripts():
    """Cria scripts de inicialização automática"""
    print("\n🚀 Criando scripts de inicialização...")
    
    try:
        # Script de inicialização do servidor
        server_script = """@echo off
echo Iniciando Quality Control Panel - Servidor...
cd /d C:\\Quality\\ControlPanel
python main.py --multi-attendant
pause
"""
        
        server_file = "C:\\Quality\\ControlPanel\\start_server.bat"
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(server_script)
        
        print(f"   ✅ Script do servidor criado: {server_file}")
        
        # Script de inicialização do atendente
        attendant_script = """@echo off
echo Iniciando Quality Control Panel - Atendente...
cd /d C:\\Quality\\AttendantClient
python attendant_client.py
pause
"""
        
        attendant_file = "C:\\Quality\\AttendantClient\\start_attendant.bat"
        with open(attendant_file, 'w', encoding='utf-8') as f:
            f.write(attendant_script)
        
        print(f"   ✅ Script do atendente criado: {attendant_file}")
        
        # Script de inicialização do cliente
        client_script = """@echo off
echo Iniciando Quality Control Panel - Cliente...
cd /d C:\\Quality\\RemoteAgent
python quality_agent.py
pause
"""
        
        client_file = "C:\\Quality\\RemoteAgent\\start_agent.bat"
        with open(client_file, 'w', encoding='utf-8') as f:
            f.write(client_script)
        
        print(f"   ✅ Script do cliente criado: {client_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar scripts: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Obter informações do sistema
    system_info = get_system_info()
    if not system_info:
        input("\nPressione Enter para sair...")
        return False
    
    # Determinar tipo de instalação
    print("\n🔍 Determinando tipo de instalação...")
    
    install_type = None
    
    if os.path.exists("C:\\Quality\\ControlPanel"):
        install_type = "servidor"
        print("   ✅ Instalação do servidor detectada")
    elif os.path.exists("C:\\Quality\\AttendantClient"):
        install_type = "atendente"
        print("   ✅ Instalação do atendente detectada")
    elif os.path.exists("C:\\Quality\\RemoteAgent"):
        install_type = "cliente"
        print("   ✅ Instalação do cliente detectada")
    else:
        print("   ❌ Nenhuma instalação detectada")
        print("      Execute primeiro o script de instalação")
        input("\nPressione Enter para sair...")
        return False
    
    # Configurar baseado no tipo
    success = True
    
    if install_type == "servidor":
        if not configure_server(system_info):
            success = False
    elif install_type == "atendente":
        if not configure_attendant(system_info):
            success = False
    elif install_type == "cliente":
        if not configure_client(system_info):
            success = False
    
    # Configurações comuns
    if not configure_firewall():
        success = False
    
    if not configure_services():
        success = False
    
    if not create_startup_scripts():
        success = False
    
    # Resumo final
    print("\n" + "=" * 70)
    if success:
        print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("✅ Sistema configurado e pronto para uso")
        print("✅ Firewall configurado")
        print("✅ Scripts de inicialização criados")
        print()
        print("🚀 PRÓXIMOS PASSOS:")
        if install_type == "servidor":
            print("   1. Execute: C:\\Quality\\ControlPanel\\start_server.bat")
            print("   2. Configure os atendentes e clientes")
        elif install_type == "atendente":
            print("   1. Execute: C:\\Quality\\AttendantClient\\start_attendant.bat")
            print("   2. Faça login com suas credenciais")
        elif install_type == "cliente":
            print("   1. Execute: C:\\Quality\\RemoteAgent\\start_agent.bat")
            print("   2. Aguarde conexão com o servidor")
    else:
        print("⚠️  CONFIGURAÇÃO CONCLUÍDA COM AVISOS")
        print("=" * 70)
        print("✅ Configuração principal concluída")
        print("⚠️  Alguns itens podem precisar de configuração manual")
        print("🔧 Verifique os logs para mais detalhes")
    
    print("=" * 70)
    
    input("\nPressione Enter para finalizar...")
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Configuração cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado durante a configuração: {e}")
        input("\nPressione Enter para sair...")
