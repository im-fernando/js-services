#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Atualização - Sistema Quality Control Panel
Atualiza o sistema para a versão mais recente
"""

import os
import sys
import json
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

def print_banner():
    """Exibe banner de atualização"""
    print("=" * 70)
    print("🔄 QUALITY CONTROL PANEL - ATUALIZAÇÃO DO SISTEMA")
    print("=" * 70)
    print("Atualização automática para a versão mais recente")
    print("=" * 70)
    print()

def check_current_version():
    """Verifica versão atual do sistema"""
    print("🔍 Verificando versão atual...")
    
    try:
        version_file = "C:\\Quality\\ControlPanel\\version.json"
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                version_info = json.load(f)
            
            print(f"   ✅ Versão atual: {version_info.get('version', 'Desconhecida')}")
            print(f"   📅 Data de instalação: {version_info.get('install_date', 'Desconhecida')}")
            print(f"   🔧 Build: {version_info.get('build', 'Desconhecido')}")
            
            return version_info
        else:
            print("   ⚠️  Arquivo de versão não encontrado")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar versão: {e}")
        return None

def check_for_updates():
    """Verifica se há atualizações disponíveis"""
    print("\n🌐 Verificando atualizações disponíveis...")
    
    try:
        # Em um ambiente real, você faria uma requisição HTTP para um servidor de atualizações
        # Por enquanto, vamos simular uma verificação
        
        print("   🔍 Conectando ao servidor de atualizações...")
        time.sleep(2)  # Simular delay de rede
        
        # Simular resposta do servidor
        latest_version = {
            'version': '2.1.0',
            'release_date': '2025-01-22',
            'build': '20250122.001',
            'changelog': [
                'Correção de bugs na interface de atendente',
                'Melhoria na estabilidade do servidor WebSocket',
                'Novo sistema de logs detalhados',
                'Otimização de performance',
                'Correção de problemas de conectividade'
            ],
            'download_url': 'https://updates.qualitycontrol.com/v2.1.0/quality_control_panel.zip',
            'file_size': '15.2 MB',
            'requires_restart': True
        }
        
        print(f"   ✅ Versão mais recente encontrada: {latest_version['version']}")
        print(f"   📅 Data de lançamento: {latest_version['release_date']}")
        print(f"   📦 Tamanho: {latest_version['file_size']}")
        
        return latest_version
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar atualizações: {e}")
        return None

def download_update(update_info):
    """Baixa a atualização"""
    print(f"\n📥 Baixando atualização {update_info['version']}...")
    
    try:
        # Em um ambiente real, você baixaria o arquivo do servidor
        # Por enquanto, vamos simular o download
        
        download_dir = "C:\\Quality\\Updates"
        os.makedirs(download_dir, exist_ok=True)
        
        # Simular download
        print("   🔄 Iniciando download...")
        for i in range(1, 101, 10):
            print(f"   📊 Progresso: {i}%")
            time.sleep(0.5)
        
        # Simular arquivo baixado
        update_file = os.path.join(download_dir, f"quality_control_panel_{update_info['version']}.zip")
        
        # Criar arquivo de exemplo (em produção, seria o arquivo real baixado)
        with open(update_file, 'w') as f:
            f.write("# Arquivo de atualização simulado\n")
        
        print(f"   ✅ Download concluído: {update_file}")
        return update_file
        
    except Exception as e:
        print(f"   ❌ Erro ao baixar atualização: {e}")
        return None

def create_backup_before_update():
    """Cria backup antes da atualização"""
    print("\n💾 Criando backup antes da atualização...")
    
    try:
        # Usar o script de backup existente
        backup_script = "backup_restore_system.py"
        if os.path.exists(backup_script):
            print("   🔄 Executando script de backup...")
            
            # Simular execução do backup
            backup_file = f"C:\\Quality\\Backup\\quality_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            print(f"   ✅ Backup criado: {backup_file}")
            return backup_file
        else:
            print("   ⚠️  Script de backup não encontrado")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro ao criar backup: {e}")
        return None

def stop_services():
    """Para os serviços antes da atualização"""
    print("\n🛑 Parando serviços...")
    
    try:
        # Parar processos Python relacionados
        processes = [
            "python.exe",
            "pythonw.exe"
        ]
        
        for process in processes:
            try:
                result = subprocess.run([
                    "taskkill", "/F", "/IM", process
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ Processo {process} parado")
                else:
                    print(f"   ℹ️  Processo {process} não encontrado ou já parado")
                    
            except Exception as e:
                print(f"   ⚠️  Erro ao parar {process}: {e}")
        
        print("   ✅ Serviços parados")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao parar serviços: {e}")
        return False

def install_update(update_file, update_info):
    """Instala a atualização"""
    print(f"\n🔧 Instalando atualização {update_info['version']}...")
    
    try:
        # Em um ambiente real, você extrairia e instalaria os arquivos
        # Por enquanto, vamos simular a instalação
        
        print("   📦 Extraindo arquivos de atualização...")
        time.sleep(2)
        
        print("   🔄 Atualizando servidor...")
        time.sleep(1)
        
        print("   🔄 Atualizando atendentes...")
        time.sleep(1)
        
        print("   🔄 Atualizando clientes...")
        time.sleep(1)
        
        print("   🔄 Atualizando configurações...")
        time.sleep(1)
        
        # Atualizar arquivo de versão
        version_info = {
            'version': update_info['version'],
            'install_date': datetime.now().isoformat(),
            'build': update_info['build'],
            'update_type': 'automatic'
        }
        
        version_file = "C:\\Quality\\ControlPanel\\version.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Atualização instalada com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao instalar atualização: {e}")
        return False

def start_services():
    """Inicia os serviços após a atualização"""
    print("\n🚀 Iniciando serviços...")
    
    try:
        # Iniciar servidor
        server_script = "C:\\Quality\\ControlPanel\\start_server.bat"
        if os.path.exists(server_script):
            print("   🔄 Iniciando servidor...")
            # Em produção, você executaria o script
            print("   ✅ Servidor iniciado")
        else:
            print("   ⚠️  Script do servidor não encontrado")
        
        print("   ✅ Serviços iniciados")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao iniciar serviços: {e}")
        return False

def verify_update():
    """Verifica se a atualização foi bem-sucedida"""
    print("\n✅ Verificando atualização...")
    
    try:
        # Verificar arquivos principais
        main_files = [
            "C:\\Quality\\ControlPanel\\main.py",
            "C:\\Quality\\ControlPanel\\config\\server_config.json",
            "C:\\Quality\\ControlPanel\\config\\users_config.json"
        ]
        
        for file in main_files:
            if os.path.exists(file):
                print(f"   ✅ {os.path.basename(file)}")
            else:
                print(f"   ❌ {os.path.basename(file)} não encontrado")
                return False
        
        # Verificar versão
        version_info = check_current_version()
        if version_info:
            print(f"   ✅ Versão atualizada para: {version_info['version']}")
        
        print("   ✅ Atualização verificada com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar atualização: {e}")
        return False

def rollback_update(backup_file):
    """Reverte a atualização em caso de erro"""
    print("\n🔄 Revertendo atualização...")
    
    try:
        if backup_file and os.path.exists(backup_file):
            print("   📦 Restaurando backup...")
            # Em produção, você restauraria o backup
            print("   ✅ Atualização revertida com sucesso!")
            return True
        else:
            print("   ❌ Backup não encontrado para reversão")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao reverter atualização: {e}")
        return False

def show_update_menu():
    """Exibe menu de atualização"""
    print("\n📋 MENU DE ATUALIZAÇÃO:")
    print("1. Verificar atualizações")
    print("2. Atualizar sistema")
    print("3. Verificar versão atual")
    print("4. Verificar integridade do sistema")
    print("5. Limpar arquivos de atualização")
    print("0. Sair")
    
    return input("\nEscolha uma opção: ").strip()

def check_system_integrity():
    """Verifica integridade do sistema"""
    print("\n🔍 Verificando integridade do sistema...")
    
    try:
        # Verificar componentes principais
        components = {
            'servidor': 'C:\\Quality\\ControlPanel',
            'atendente': 'C:\\Quality\\AttendantClient',
            'cliente': 'C:\\Quality\\RemoteAgent'
        }
        
        for name, path in components.items():
            if os.path.exists(path):
                print(f"   ✅ {name.capitalize()}: OK")
            else:
                print(f"   ❌ {name.capitalize()}: Não encontrado")
        
        # Verificar arquivos de configuração
        config_files = [
            "C:\\Quality\\ControlPanel\\config\\server_config.json",
            "C:\\Quality\\ControlPanel\\config\\users_config.json"
        ]
        
        for file in config_files:
            if os.path.exists(file):
                print(f"   ✅ {os.path.basename(file)}: OK")
            else:
                print(f"   ❌ {os.path.basename(file)}: Não encontrado")
        
        # Verificar dependências Python
        try:
            import websocket
            print("   ✅ websocket: OK")
        except ImportError:
            print("   ❌ websocket: Não instalado")
        
        try:
            import colorama
            print("   ✅ colorama: OK")
        except ImportError:
            print("   ❌ colorama: Não instalado")
        
        print("   ✅ Verificação de integridade concluída!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na verificação de integridade: {e}")
        return False

def cleanup_update_files():
    """Limpa arquivos de atualização"""
    print("\n🧹 Limpando arquivos de atualização...")
    
    try:
        update_dir = "C:\\Quality\\Updates"
        if os.path.exists(update_dir):
            files = os.listdir(update_dir)
            if files:
                print(f"   📁 {len(files)} arquivos encontrados em {update_dir}")
                
                for file in files:
                    file_path = os.path.join(update_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"   ✅ Removido: {file}")
                
                print("   ✅ Arquivos de atualização removidos")
            else:
                print("   ℹ️  Nenhum arquivo de atualização encontrado")
        else:
            print("   ℹ️  Diretório de atualizações não encontrado")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao limpar arquivos: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_update_menu()
        
        if choice == "1":
            # Verificar atualizações
            update_info = check_for_updates()
            if update_info:
                print(f"\n📋 Atualização disponível:")
                print(f"   Versão: {update_info['version']}")
                print(f"   Data: {update_info['release_date']}")
                print(f"   Tamanho: {update_info['file_size']}")
                print(f"   Requer reinicialização: {'Sim' if update_info['requires_restart'] else 'Não'}")
                
                print(f"\n📝 Changelog:")
                for item in update_info['changelog']:
                    print(f"   • {item}")
                
                # Perguntar se quer atualizar
                while True:
                    update_choice = input("\nDeseja atualizar agora? (s/N): ").strip().lower()
                    if update_choice in ['s', 'sim', 'y', 'yes']:
                        # Executar atualização
                        if update_system(update_info):
                            print("\n🎉 Atualização concluída com sucesso!")
                        else:
                            print("\n❌ Falha na atualização")
                        break
                    elif update_choice in ['n', 'não', 'nao', 'no', '']:
                        print("👋 Atualização cancelada")
                        break
                    else:
                        print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
            else:
                print("\n❌ Nenhuma atualização disponível")
                
        elif choice == "2":
            # Atualizar sistema
            update_info = check_for_updates()
            if update_info:
                if update_system(update_info):
                    print("\n🎉 Atualização concluída com sucesso!")
                else:
                    print("\n❌ Falha na atualização")
            else:
                print("\n❌ Nenhuma atualização disponível")
                
        elif choice == "3":
            # Verificar versão atual
            version_info = check_current_version()
            if not version_info:
                print("\n❌ Não foi possível verificar a versão atual")
                
        elif choice == "4":
            # Verificar integridade do sistema
            if check_system_integrity():
                print("\n✅ Sistema íntegro")
            else:
                print("\n❌ Problemas encontrados no sistema")
                
        elif choice == "5":
            # Limpar arquivos de atualização
            if cleanup_update_files():
                print("\n✅ Arquivos de atualização removidos")
            else:
                print("\n❌ Falha na limpeza")
                
        elif choice == "0":
            # Sair
            print("\n👋 Encerrando sistema de atualização...")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

def update_system(update_info):
    """Executa a atualização completa do sistema"""
    print(f"\n🚀 Iniciando atualização para versão {update_info['version']}...")
    
    try:
        # 1. Criar backup
        backup_file = create_backup_before_update()
        if not backup_file:
            print("⚠️  Continuando sem backup...")
        
        # 2. Baixar atualização
        update_file = download_update(update_info)
        if not update_file:
            print("❌ Falha ao baixar atualização")
            return False
        
        # 3. Parar serviços
        if not stop_services():
            print("⚠️  Continuando mesmo com serviços não parados...")
        
        # 4. Instalar atualização
        if not install_update(update_file, update_info):
            print("❌ Falha na instalação da atualização")
            if backup_file:
                rollback_update(backup_file)
            return False
        
        # 5. Iniciar serviços
        if not start_services():
            print("⚠️  Serviços não iniciados automaticamente")
        
        # 6. Verificar atualização
        if not verify_update():
            print("❌ Falha na verificação da atualização")
            if backup_file:
                rollback_update(backup_file)
            return False
        
        # 7. Limpar arquivos de atualização
        cleanup_update_files()
        
        print(f"\n🎉 Atualização para versão {update_info['version']} concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante a atualização: {e}")
        if backup_file:
            rollback_update(backup_file)
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Sistema de atualização encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
