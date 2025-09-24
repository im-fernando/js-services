#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico - Sistema Quality Control Panel
Diagnostica problemas e fornece soluções
"""

import os
import sys
import json
import subprocess
import socket
import time
from datetime import datetime
from pathlib import Path

def print_banner():
    """Exibe banner de diagnóstico"""
    print("=" * 70)
    print("🔍 QUALITY CONTROL PANEL - DIAGNÓSTICO DO SISTEMA")
    print("=" * 70)
    print("Diagnóstico completo de problemas e soluções")
    print("=" * 70)
    print()

def check_python_environment():
    """Verifica ambiente Python"""
    print("🐍 Verificando ambiente Python...")
    
    issues = []
    
    # Versão do Python
    python_version = sys.version_info
    if python_version < (3, 7):
        issues.append({
            'type': 'error',
            'message': f'Python {python_version.major}.{python_version.minor} é muito antigo',
            'solution': 'Atualize para Python 3.7 ou superior'
        })
    else:
        print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
    
    # Dependências Python
    dependencies = [
        'websocket',
        'websocket_server',
        'colorama',
        'rich',
        'requests'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep} - OK")
        except ImportError:
            issues.append({
                'type': 'error',
                'message': f'Dependência {dep} não instalada',
                'solution': f'Execute: pip install {dep}'
            })
    
    return issues

def check_system_files():
    """Verifica arquivos do sistema"""
    print("\n📁 Verificando arquivos do sistema...")
    
    issues = []
    
    # Componentes principais
    components = {
        'servidor': 'C:\\Quality\\ControlPanel',
        'atendente': 'C:\\Quality\\AttendantClient',
        'cliente': 'C:\\Quality\\RemoteAgent'
    }
    
    for name, path in components.items():
        if os.path.exists(path):
            print(f"   ✅ {name.capitalize()}: {path}")
            
            # Verificar arquivos principais
            if name == 'servidor':
                main_files = [
                    'main.py',
                    'config/server_config.json',
                    'config/users_config.json',
                    'core/server.py'
                ]
                
                for file in main_files:
                    file_path = os.path.join(path, file)
                    if os.path.exists(file_path):
                        print(f"      ✅ {file}")
                    else:
                        issues.append({
                            'type': 'error',
                            'message': f'Arquivo {file} não encontrado no servidor',
                            'solution': f'Reinstale o componente servidor'
                        })
            
        else:
            issues.append({
                'type': 'error',
                'message': f'Componente {name} não instalado',
                'solution': f'Execute: python install_{name}_quick.py'
            })
    
    return issues

def check_network_connectivity():
    """Verifica conectividade de rede"""
    print("\n🌐 Verificando conectividade de rede...")
    
    issues = []
    
    # Verificar porta 8765
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 8765))
        sock.close()
        
        if result == 0:
            print("   ✅ Porta 8765 está em uso (servidor pode estar rodando)")
        else:
            print("   ℹ️  Porta 8765 está livre (servidor não está rodando)")
            
    except Exception as e:
        issues.append({
            'type': 'warning',
            'message': f'Erro ao verificar porta 8765: {e}',
            'solution': 'Verifique se o servidor está rodando'
        })
    
    # Verificar conectividade com internet
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('8.8.8.8', 53))
        sock.close()
        
        if result == 0:
            print("   ✅ Conectividade com internet - OK")
        else:
            issues.append({
                'type': 'warning',
                'message': 'Sem conectividade com internet',
                'solution': 'Verifique sua conexão de rede'
            })
            
    except Exception as e:
        issues.append({
            'type': 'warning',
            'message': f'Erro ao verificar conectividade: {e}',
            'solution': 'Verifique sua conexão de rede'
        })
    
    return issues

def check_services():
    """Verifica serviços Quality"""
    print("\n🖥️  Verificando serviços Quality...")
    
    issues = []
    
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
                
                if "RUNNING" in state:
                    print(f"   ✅ {service}: {state}")
                else:
                    issues.append({
                        'type': 'warning',
                        'message': f'Serviço {service} não está rodando: {state}',
                        'solution': f'Execute: net start {service}'
                    })
            else:
                issues.append({
                    'type': 'info',
                    'message': f'Serviço {service} não encontrado',
                    'solution': f'Instale o serviço {service} se necessário'
                })
                
        except Exception as e:
            issues.append({
                'type': 'error',
                'message': f'Erro ao verificar serviço {service}: {e}',
                'solution': 'Verifique permissões de administrador'
            })
    
    return issues

def check_permissions():
    """Verifica permissões do sistema"""
    print("\n🔐 Verificando permissões...")
    
    issues = []
    
    # Verificar se está rodando como administrador
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        
        if is_admin:
            print("   ✅ Executando como administrador")
        else:
            issues.append({
                'type': 'warning',
                'message': 'Não está executando como administrador',
                'solution': 'Execute o script como administrador'
            })
            
    except Exception as e:
        issues.append({
            'type': 'error',
            'message': f'Erro ao verificar permissões: {e}',
            'solution': 'Verifique se está executando como administrador'
        })
    
    # Verificar permissões de escrita
    test_dirs = [
        "C:\\Quality",
        "C:\\Quality\\ControlPanel",
        "C:\\Quality\\Logs"
    ]
    
    for test_dir in test_dirs:
        try:
            if os.path.exists(test_dir):
                test_file = os.path.join(test_dir, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"   ✅ Permissão de escrita: {test_dir}")
            else:
                print(f"   ℹ️  Diretório não existe: {test_dir}")
                
        except Exception as e:
            issues.append({
                'type': 'error',
                'message': f'Sem permissão de escrita em {test_dir}',
                'solution': 'Execute como administrador ou ajuste permissões'
            })
    
    return issues

def check_configuration():
    """Verifica configurações"""
    print("\n⚙️  Verificando configurações...")
    
    issues = []
    
    # Verificar configuração do servidor
    server_config_file = "C:\\Quality\\ControlPanel\\config\\server_config.json"
    if os.path.exists(server_config_file):
        try:
            with open(server_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Verificar configurações essenciais
            if 'server' in config:
                server_config = config['server']
                if 'host' in server_config and 'port' in server_config:
                    print(f"   ✅ Configuração do servidor: {server_config['host']}:{server_config['port']}")
                else:
                    issues.append({
                        'type': 'error',
                        'message': 'Configuração do servidor incompleta',
                        'solution': 'Execute: python configure_system.py'
                    })
            else:
                issues.append({
                    'type': 'error',
                    'message': 'Seção server não encontrada na configuração',
                    'solution': 'Execute: python configure_system.py'
                })
                
        except Exception as e:
            issues.append({
                'type': 'error',
                'message': f'Erro ao ler configuração do servidor: {e}',
                'solution': 'Execute: python configure_system.py'
            })
    else:
        issues.append({
            'type': 'error',
            'message': 'Arquivo de configuração do servidor não encontrado',
            'solution': 'Execute: python configure_system.py'
        })
    
    # Verificar configuração de usuários
    users_config_file = "C:\\Quality\\ControlPanel\\config\\users_config.json"
    if os.path.exists(users_config_file):
        try:
            with open(users_config_file, 'r', encoding='utf-8') as f:
                users_config = json.load(f)
            
            if 'attendants' in users_config and len(users_config['attendants']) > 0:
                print(f"   ✅ Configuração de usuários: {len(users_config['attendants'])} usuários")
            else:
                issues.append({
                    'type': 'error',
                    'message': 'Nenhum usuário configurado',
                    'solution': 'Execute: python configure_system.py'
                })
                
        except Exception as e:
            issues.append({
                'type': 'error',
                'message': f'Erro ao ler configuração de usuários: {e}',
                'solution': 'Execute: python configure_system.py'
            })
    else:
        issues.append({
            'type': 'error',
            'message': 'Arquivo de configuração de usuários não encontrado',
            'solution': 'Execute: python configure_system.py'
        })
    
    return issues

def check_logs():
    """Verifica logs do sistema"""
    print("\n📋 Verificando logs...")
    
    issues = []
    
    # Verificar diretório de logs
    log_dirs = [
        "C:\\Quality\\Logs",
        "C:\\Quality\\ControlPanel\\logs"
    ]
    
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            try:
                files = os.listdir(log_dir)
                if files:
                    print(f"   ✅ Logs encontrados em {log_dir}: {len(files)} arquivos")
                    
                    # Verificar tamanho dos logs
                    total_size = 0
                    for file in files:
                        file_path = os.path.join(log_dir, file)
                        if os.path.isfile(file_path):
                            total_size += os.path.getsize(file_path)
                    
                    total_size_mb = total_size / (1024 * 1024)
                    if total_size_mb > 100:  # Mais de 100MB
                        issues.append({
                            'type': 'warning',
                            'message': f'Logs muito grandes: {total_size_mb:.1f}MB',
                            'solution': 'Execute: python backup_restore_system.py (opção 5)'
                        })
                    else:
                        print(f"   ✅ Tamanho dos logs: {total_size_mb:.1f}MB")
                else:
                    print(f"   ℹ️  Nenhum log encontrado em {log_dir}")
                    
            except Exception as e:
                issues.append({
                    'type': 'error',
                    'message': f'Erro ao verificar logs em {log_dir}: {e}',
                    'solution': 'Verifique permissões de acesso'
                })
        else:
            print(f"   ℹ️  Diretório de logs não encontrado: {log_dir}")
    
    return issues

def check_performance():
    """Verifica performance do sistema"""
    print("\n⚡ Verificando performance...")
    
    issues = []
    
    try:
        import psutil
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            issues.append({
                'type': 'warning',
                'message': f'Uso de CPU alto: {cpu_percent}%',
                'solution': 'Verifique processos em execução'
            })
        else:
            print(f"   ✅ CPU: {cpu_percent}%")
        
        # Memória
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            issues.append({
                'type': 'warning',
                'message': f'Uso de memória alto: {memory.percent}%',
                'solution': 'Reinicie o sistema ou feche aplicações desnecessárias'
            })
        else:
            print(f"   ✅ Memória: {memory.percent}%")
        
        # Disco
        disk = psutil.disk_usage('C:')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 80:
            issues.append({
                'type': 'warning',
                'message': f'Uso de disco alto: {disk_percent:.1f}%',
                'solution': 'Libere espaço em disco'
            })
        else:
            print(f"   ✅ Disco: {disk_percent:.1f}%")
        
    except ImportError:
        issues.append({
            'type': 'info',
            'message': 'psutil não instalado - não é possível verificar performance',
            'solution': 'Execute: pip install psutil'
        })
    except Exception as e:
        issues.append({
            'type': 'error',
            'message': f'Erro ao verificar performance: {e}',
            'solution': 'Verifique se o sistema está funcionando normalmente'
        })
    
    return issues

def generate_diagnostic_report(issues):
    """Gera relatório de diagnóstico"""
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO DE DIAGNÓSTICO")
    print("=" * 70)
    
    if not issues:
        print("🎉 NENHUM PROBLEMA ENCONTRADO!")
        print("✅ O sistema está funcionando corretamente")
        return
    
    # Agrupar por tipo
    errors = [i for i in issues if i['type'] == 'error']
    warnings = [i for i in issues if i['type'] == 'warning']
    info = [i for i in issues if i['type'] == 'info']
    
    print(f"📈 RESUMO:")
    print(f"   ❌ Erros: {len(errors)}")
    print(f"   ⚠️  Avisos: {len(warnings)}")
    print(f"   ℹ️  Informações: {len(info)}")
    
    # Exibir problemas
    if errors:
        print(f"\n❌ ERROS CRÍTICOS ({len(errors)}):")
        for i, issue in enumerate(errors, 1):
            print(f"   {i}. {issue['message']}")
            print(f"      💡 Solução: {issue['solution']}")
            print()
    
    if warnings:
        print(f"\n⚠️  AVISOS ({len(warnings)}):")
        for i, issue in enumerate(warnings, 1):
            print(f"   {i}. {issue['message']}")
            print(f"      💡 Solução: {issue['solution']}")
            print()
    
    if info:
        print(f"\nℹ️  INFORMAÇÕES ({len(info)}):")
        for i, issue in enumerate(info, 1):
            print(f"   {i}. {issue['message']}")
            print(f"      💡 Solução: {issue['solution']}")
            print()
    
    # Salvar relatório
    try:
        report_file = f"C:\\Quality\\Logs\\diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Relatório de Diagnóstico - Quality Control Panel\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de problemas: {len(issues)}\n\n")
            
            for issue in issues:
                f.write(f"[{issue['type'].upper()}] {issue['message']}\n")
                f.write(f"Solução: {issue['solution']}\n\n")
        
        print(f"📝 Relatório salvo: {report_file}")
        
    except Exception as e:
        print(f"⚠️  Erro ao salvar relatório: {e}")

def show_menu():
    """Exibe menu de diagnóstico"""
    print("\n📋 MENU DE DIAGNÓSTICO:")
    print("1. Diagnóstico completo")
    print("2. Verificar ambiente Python")
    print("3. Verificar arquivos do sistema")
    print("4. Verificar conectividade de rede")
    print("5. Verificar serviços Quality")
    print("6. Verificar permissões")
    print("7. Verificar configurações")
    print("8. Verificar logs")
    print("9. Verificar performance")
    print("0. Sair")
    
    return input("\nEscolha uma opção: ").strip()

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Diagnóstico completo
            print("\n🔍 Executando diagnóstico completo...")
            
            all_issues = []
            all_issues.extend(check_python_environment())
            all_issues.extend(check_system_files())
            all_issues.extend(check_network_connectivity())
            all_issues.extend(check_services())
            all_issues.extend(check_permissions())
            all_issues.extend(check_configuration())
            all_issues.extend(check_logs())
            all_issues.extend(check_performance())
            
            generate_diagnostic_report(all_issues)
            
        elif choice == "2":
            # Verificar ambiente Python
            issues = check_python_environment()
            generate_diagnostic_report(issues)
            
        elif choice == "3":
            # Verificar arquivos do sistema
            issues = check_system_files()
            generate_diagnostic_report(issues)
            
        elif choice == "4":
            # Verificar conectividade de rede
            issues = check_network_connectivity()
            generate_diagnostic_report(issues)
            
        elif choice == "5":
            # Verificar serviços Quality
            issues = check_services()
            generate_diagnostic_report(issues)
            
        elif choice == "6":
            # Verificar permissões
            issues = check_permissions()
            generate_diagnostic_report(issues)
            
        elif choice == "7":
            # Verificar configurações
            issues = check_configuration()
            generate_diagnostic_report(issues)
            
        elif choice == "8":
            # Verificar logs
            issues = check_logs()
            generate_diagnostic_report(issues)
            
        elif choice == "9":
            # Verificar performance
            issues = check_performance()
            generate_diagnostic_report(issues)
            
        elif choice == "0":
            # Sair
            print("\n👋 Encerrando diagnóstico...")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Diagnóstico encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
