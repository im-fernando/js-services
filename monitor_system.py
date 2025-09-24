#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Monitoramento - Sistema Quality Control Panel
Monitora o status e performance do sistema
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path

def print_banner():
    """Exibe banner de monitoramento"""
    print("=" * 70)
    print("📊 QUALITY CONTROL PANEL - MONITORAMENTO DO SISTEMA")
    print("=" * 70)
    print("Monitoramento em tempo real do sistema")
    print("=" * 70)
    print()

def get_system_status():
    """Obtém status do sistema"""
    print("🔍 Verificando status do sistema...")
    
    status = {
        'timestamp': datetime.now().isoformat(),
        'components': {},
        'services': {},
        'network': {},
        'performance': {}
    }
    
    # Verificar componentes
    components = {
        'servidor': 'C:\\Quality\\ControlPanel',
        'atendente': 'C:\\Quality\\AttendantClient',
        'cliente': 'C:\\Quality\\RemoteAgent'
    }
    
    for name, path in components.items():
        if os.path.exists(path):
            status['components'][name] = {
                'installed': True,
                'path': path,
                'last_modified': os.path.getmtime(path)
            }
        else:
            status['components'][name] = {
                'installed': False,
                'path': path
            }
    
    # Verificar serviços Quality
    quality_services = [
        "srvIntegraWeb",
        "srvIntegraFiscal",
        "srvIntegraContabil",
        "srvIntegraEstoque",
        "srvIntegraFinanceiro"
    ]
    
    for service in quality_services:
        try:
            result = subprocess.run([
                "sc", "query", service
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extrair status do serviço
                lines = result.stdout.split('\n')
                state = "Unknown"
                for line in lines:
                    if "STATE" in line:
                        state = line.split("STATE")[1].strip()
                        break
                
                status['services'][service] = {
                    'exists': True,
                    'state': state
                }
            else:
                status['services'][service] = {
                    'exists': False,
                    'state': 'Not Found'
                }
                
        except Exception as e:
            status['services'][service] = {
                'exists': False,
                'state': f'Error: {e}'
            }
    
    # Verificar conectividade de rede
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Testar porta 8765
        result = sock.connect_ex(('localhost', 8765))
        sock.close()
        
        status['network']['port_8765'] = {
            'open': result == 0,
            'status': 'Open' if result == 0 else 'Closed'
        }
        
    except Exception as e:
        status['network']['port_8765'] = {
            'open': False,
            'status': f'Error: {e}'
        }
    
    # Verificar performance
    try:
        import psutil
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        status['performance']['cpu'] = {
            'usage_percent': cpu_percent,
            'status': 'Normal' if cpu_percent < 80 else 'High'
        }
        
        # Memória
        memory = psutil.virtual_memory()
        status['performance']['memory'] = {
            'usage_percent': memory.percent,
            'available_gb': round(memory.available / (1024**3), 2),
            'status': 'Normal' if memory.percent < 80 else 'High'
        }
        
        # Disco
        disk = psutil.disk_usage('C:')
        status['performance']['disk'] = {
            'usage_percent': round((disk.used / disk.total) * 100, 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'status': 'Normal' if (disk.used / disk.total) < 0.8 else 'High'
        }
        
    except ImportError:
        status['performance']['error'] = 'psutil não instalado'
    except Exception as e:
        status['performance']['error'] = f'Erro: {e}'
    
    return status

def display_status(status):
    """Exibe status do sistema"""
    print(f"\n📊 STATUS DO SISTEMA - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # Componentes
    print("\n🔧 COMPONENTES:")
    for name, info in status['components'].items():
        if info['installed']:
            print(f"   ✅ {name.capitalize()}: Instalado")
        else:
            print(f"   ❌ {name.capitalize()}: Não instalado")
    
    # Serviços Quality
    print("\n🖥️  SERVIÇOS QUALITY:")
    for service, info in status['services'].items():
        if info['exists']:
            state_icon = "🟢" if "RUNNING" in info['state'] else "🔴"
            print(f"   {state_icon} {service}: {info['state']}")
        else:
            print(f"   ❌ {service}: Não encontrado")
    
    # Rede
    print("\n🌐 REDE:")
    for port, info in status['network'].items():
        icon = "🟢" if info['open'] else "🔴"
        print(f"   {icon} {port}: {info['status']}")
    
    # Performance
    print("\n⚡ PERFORMANCE:")
    if 'error' in status['performance']:
        print(f"   ❌ Erro: {status['performance']['error']}")
    else:
        for metric, info in status['performance'].items():
            if isinstance(info, dict) and 'usage_percent' in info:
                icon = "🟢" if info['status'] == 'Normal' else "🔴"
                print(f"   {icon} {metric.capitalize()}: {info['usage_percent']}% ({info['status']})")

def monitor_continuously(interval=30):
    """Monitora continuamente o sistema"""
    print(f"\n🔄 Iniciando monitoramento contínuo (intervalo: {interval}s)")
    print("💡 Pressione Ctrl+C para parar")
    
    try:
        while True:
            # Limpar tela
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            
            # Obter e exibir status
            status = get_system_status()
            display_status(status)
            
            # Aguardar próximo ciclo
            print(f"\n⏳ Próxima verificação em {interval} segundos...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoramento interrompido pelo usuário")

def save_status_log(status):
    """Salva log de status"""
    try:
        log_dir = "C:\\Quality\\Logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"system_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Log salvo: {log_file}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar log: {e}")

def check_specific_service(service_name):
    """Verifica status de um serviço específico"""
    print(f"\n🔍 Verificando serviço: {service_name}")
    
    try:
        result = subprocess.run([
            "sc", "query", service_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Serviço encontrado:")
            print(result.stdout)
        else:
            print("❌ Serviço não encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao verificar serviço: {e}")

def restart_service(service_name):
    """Reinicia um serviço"""
    print(f"\n🔄 Reiniciando serviço: {service_name}")
    
    try:
        # Parar serviço
        print("   Parando serviço...")
        result = subprocess.run([
            "net", "stop", service_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Serviço parado")
        else:
            print(f"   ⚠️  Erro ao parar serviço: {result.stderr}")
        
        # Aguardar
        time.sleep(2)
        
        # Iniciar serviço
        print("   Iniciando serviço...")
        result = subprocess.run([
            "net", "start", service_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Serviço iniciado")
        else:
            print(f"   ⚠️  Erro ao iniciar serviço: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro ao reiniciar serviço: {e}")

def show_menu():
    """Exibe menu de opções"""
    print("\n📋 MENU DE MONITORAMENTO:")
    print("1. Verificar status atual")
    print("2. Monitoramento contínuo")
    print("3. Verificar serviço específico")
    print("4. Reiniciar serviço")
    print("5. Salvar log de status")
    print("6. Ver logs do sistema")
    print("0. Sair")
    
    return input("\nEscolha uma opção: ").strip()

def view_system_logs():
    """Visualiza logs do sistema"""
    print("\n📋 LOGS DO SISTEMA:")
    
    log_dirs = [
        "C:\\Quality\\Logs",
        "C:\\Quality\\ControlPanel\\logs",
        "C:\\Windows\\System32\\LogFiles"
    ]
    
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            print(f"\n📁 {log_dir}:")
            try:
                files = os.listdir(log_dir)
                for file in files[:10]:  # Mostrar apenas os primeiros 10
                    file_path = os.path.join(log_dir, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        print(f"   📄 {file} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M')})")
            except Exception as e:
                print(f"   ❌ Erro ao listar: {e}")
        else:
            print(f"   ❌ {log_dir} não encontrado")

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Verificar status atual
            status = get_system_status()
            display_status(status)
            
        elif choice == "2":
            # Monitoramento contínuo
            interval = input("Intervalo em segundos (padrão: 30): ").strip()
            try:
                interval = int(interval) if interval else 30
            except ValueError:
                interval = 30
            
            monitor_continuously(interval)
            
        elif choice == "3":
            # Verificar serviço específico
            service_name = input("Nome do serviço: ").strip()
            if service_name:
                check_specific_service(service_name)
            else:
                print("❌ Nome do serviço é obrigatório")
                
        elif choice == "4":
            # Reiniciar serviço
            service_name = input("Nome do serviço: ").strip()
            if service_name:
                restart_service(service_name)
            else:
                print("❌ Nome do serviço é obrigatório")
                
        elif choice == "5":
            # Salvar log de status
            status = get_system_status()
            save_status_log(status)
            
        elif choice == "6":
            # Ver logs do sistema
            view_system_logs()
            
        elif choice == "0":
            # Sair
            print("\n👋 Encerrando monitoramento...")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Monitoramento encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
