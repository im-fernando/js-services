#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Backup e Restore - Sistema Quality Control Panel
Faz backup e restauração do sistema
"""

import os
import sys
import shutil
import json
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

def print_banner():
    """Exibe banner de backup/restore"""
    print("=" * 70)
    print("💾 QUALITY CONTROL PANEL - BACKUP E RESTORE")
    print("=" * 70)
    print("Sistema de backup e restauração do Quality Control Panel")
    print("=" * 70)
    print()

def create_backup():
    """Cria backup do sistema"""
    print("📦 Criando backup do sistema...")
    
    try:
        # Diretório de backup
        backup_dir = "C:\\Quality\\Backup"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Timestamp para nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"quality_backup_{timestamp}.zip")
        
        # Componentes para backup
        components = {
            'servidor': 'C:\\Quality\\ControlPanel',
            'atendente': 'C:\\Quality\\AttendantClient',
            'cliente': 'C:\\Quality\\RemoteAgent',
            'documentacao': 'C:\\Quality\\Documentation',
            'logs': 'C:\\Quality\\Logs'
        }
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for name, path in components.items():
                if os.path.exists(path):
                    print(f"   📁 Adicionando {name}: {path}")
                    
                    # Adicionar arquivos ao zip
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, path)
                            zipf.write(file_path, f"{name}/{arcname}")
                else:
                    print(f"   ⚠️  {name} não encontrado: {path}")
        
        # Criar arquivo de metadados
        metadata = {
            'timestamp': timestamp,
            'backup_file': backup_file,
            'components': components,
            'system_info': {
                'computer_name': os.environ.get('COMPUTERNAME', 'Desconhecido'),
                'username': os.environ.get('USERNAME', 'Desconhecido'),
                'python_version': sys.version
            }
        }
        
        metadata_file = os.path.join(backup_dir, f"backup_metadata_{timestamp}.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Backup criado: {backup_file}")
        print(f"   ✅ Metadados salvos: {metadata_file}")
        
        return backup_file
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def restore_backup():
    """Restaura backup do sistema"""
    print("🔄 Restaurando backup do sistema...")
    
    try:
        # Listar backups disponíveis
        backup_dir = "C:\\Quality\\Backup"
        if not os.path.exists(backup_dir):
            print("❌ Diretório de backup não encontrado")
            return False
        
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('quality_backup_') and f.endswith('.zip')]
        
        if not backup_files:
            print("❌ Nenhum backup encontrado")
            return False
        
        print("\n📋 Backups disponíveis:")
        for i, file in enumerate(backup_files, 1):
            file_path = os.path.join(backup_dir, file)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"   {i}. {file} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M')})")
        
        # Selecionar backup
        while True:
            try:
                choice = int(input("\nEscolha o backup para restaurar (número): ")) - 1
                if 0 <= choice < len(backup_files):
                    selected_backup = backup_files[choice]
                    break
                else:
                    print("❌ Opção inválida")
            except ValueError:
                print("❌ Digite um número válido")
        
        backup_file = os.path.join(backup_dir, selected_backup)
        
        # Confirmar restauração
        print(f"\n⚠️  ATENÇÃO: Esta operação irá substituir os arquivos atuais!")
        print(f"   Backup selecionado: {selected_backup}")
        
        while True:
            confirm = input("Deseja continuar? (s/N): ").strip().lower()
            if confirm in ['s', 'sim', 'y', 'yes']:
                break
            elif confirm in ['n', 'não', 'nao', 'no', '']:
                print("👋 Restauração cancelada")
                return False
            else:
                print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
        
        # Extrair backup
        print(f"\n📦 Extraindo backup: {selected_backup}")
        
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            # Listar arquivos no backup
            file_list = zipf.namelist()
            
            # Extrair por componente
            components = ['servidor', 'atendente', 'cliente', 'documentacao', 'logs']
            
            for component in components:
                component_files = [f for f in file_list if f.startswith(f"{component}/")]
                
                if component_files:
                    print(f"   📁 Restaurando {component}...")
                    
                    # Criar diretório de destino
                    dest_dir = f"C:\\Quality\\{component.capitalize()}"
                    if component == 'servidor':
                        dest_dir = "C:\\Quality\\ControlPanel"
                    elif component == 'atendente':
                        dest_dir = "C:\\Quality\\AttendantClient"
                    elif component == 'cliente':
                        dest_dir = "C:\\Quality\\RemoteAgent"
                    elif component == 'documentacao':
                        dest_dir = "C:\\Quality\\Documentation"
                    elif component == 'logs':
                        dest_dir = "C:\\Quality\\Logs"
                    
                    # Extrair arquivos
                    for file in component_files:
                        zipf.extract(file, "C:\\Quality\\")
                        print(f"      ✅ {file}")
                else:
                    print(f"   ⚠️  {component} não encontrado no backup")
        
        print("✅ Backup restaurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup: {e}")
        return False

def list_backups():
    """Lista backups disponíveis"""
    print("📋 Listando backups disponíveis...")
    
    try:
        backup_dir = "C:\\Quality\\Backup"
        if not os.path.exists(backup_dir):
            print("❌ Diretório de backup não encontrado")
            return
        
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('quality_backup_') and f.endswith('.zip')]
        
        if not backup_files:
            print("❌ Nenhum backup encontrado")
            return
        
        print(f"\n📦 {len(backup_files)} backups encontrados:")
        print("-" * 50)
        
        for i, file in enumerate(backup_files, 1):
            file_path = os.path.join(backup_dir, file)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            print(f"{i:2d}. {file}")
            print(f"    Tamanho: {size:,} bytes")
            print(f"    Data: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        # Mostrar metadados se disponível
        metadata_files = [f for f in os.listdir(backup_dir) if f.startswith('backup_metadata_') and f.endswith('.json')]
        
        if metadata_files:
            print("📄 Metadados disponíveis:")
            for metadata_file in metadata_files:
                metadata_path = os.path.join(backup_dir, metadata_file)
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    print(f"   📄 {metadata_file}")
                    print(f"      Computador: {metadata['system_info']['computer_name']}")
                    print(f"      Usuário: {metadata['system_info']['username']}")
                    print(f"      Python: {metadata['system_info']['python_version'].split()[0]}")
                    print()
                    
                except Exception as e:
                    print(f"   ❌ Erro ao ler {metadata_file}: {e}")
        
    except Exception as e:
        print(f"❌ Erro ao listar backups: {e}")

def delete_backup():
    """Remove backup específico"""
    print("🗑️  Removendo backup...")
    
    try:
        backup_dir = "C:\\Quality\\Backup"
        if not os.path.exists(backup_dir):
            print("❌ Diretório de backup não encontrado")
            return False
        
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('quality_backup_') and f.endswith('.zip')]
        
        if not backup_files:
            print("❌ Nenhum backup encontrado")
            return False
        
        print("\n📋 Backups disponíveis:")
        for i, file in enumerate(backup_files, 1):
            file_path = os.path.join(backup_dir, file)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"   {i}. {file} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M')})")
        
        # Selecionar backup para remover
        while True:
            try:
                choice = int(input("\nEscolha o backup para remover (número): ")) - 1
                if 0 <= choice < len(backup_files):
                    selected_backup = backup_files[choice]
                    break
                else:
                    print("❌ Opção inválida")
            except ValueError:
                print("❌ Digite um número válido")
        
        backup_file = os.path.join(backup_dir, selected_backup)
        
        # Confirmar remoção
        print(f"\n⚠️  ATENÇÃO: Esta operação irá remover permanentemente o backup!")
        print(f"   Backup selecionado: {selected_backup}")
        
        while True:
            confirm = input("Deseja continuar? (s/N): ").strip().lower()
            if confirm in ['s', 'sim', 'y', 'yes']:
                break
            elif confirm in ['n', 'não', 'nao', 'no', '']:
                print("👋 Remoção cancelada")
                return False
            else:
                print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
        
        # Remover arquivo
        os.remove(backup_file)
        print(f"✅ Backup removido: {selected_backup}")
        
        # Remover metadados se existir
        metadata_file = os.path.join(backup_dir, f"backup_metadata_{selected_backup.replace('quality_backup_', '').replace('.zip', '')}.json")
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
            print(f"✅ Metadados removidos: {os.path.basename(metadata_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao remover backup: {e}")
        return False

def cleanup_old_backups():
    """Remove backups antigos"""
    print("🧹 Limpando backups antigos...")
    
    try:
        backup_dir = "C:\\Quality\\Backup"
        if not os.path.exists(backup_dir):
            print("❌ Diretório de backup não encontrado")
            return False
        
        # Obter dias para manter
        while True:
            try:
                days = int(input("Manter backups dos últimos quantos dias? (padrão: 30): ").strip() or "30")
                if days > 0:
                    break
                else:
                    print("❌ Digite um número positivo")
            except ValueError:
                print("❌ Digite um número válido")
        
        # Calcular data limite
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Encontrar backups antigos
        backup_files = [f for f in os.listdir(backup_dir) if f.startswith('quality_backup_') and f.endswith('.zip')]
        old_backups = []
        
        for file in backup_files:
            file_path = os.path.join(backup_dir, file)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if modified < cutoff_date:
                old_backups.append(file)
        
        if not old_backups:
            print(f"✅ Nenhum backup antigo encontrado (mais de {days} dias)")
            return True
        
        print(f"\n📋 {len(old_backups)} backups antigos encontrados:")
        for file in old_backups:
            file_path = os.path.join(backup_dir, file)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"   📄 {file} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M')})")
        
        # Confirmar limpeza
        print(f"\n⚠️  ATENÇÃO: Esta operação irá remover {len(old_backups)} backups antigos!")
        
        while True:
            confirm = input("Deseja continuar? (s/N): ").strip().lower()
            if confirm in ['s', 'sim', 'y', 'yes']:
                break
            elif confirm in ['n', 'não', 'nao', 'no', '']:
                print("👋 Limpeza cancelada")
                return False
            else:
                print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")
        
        # Remover backups antigos
        removed_count = 0
        for file in old_backups:
            try:
                file_path = os.path.join(backup_dir, file)
                os.remove(file_path)
                print(f"   ✅ Removido: {file}")
                removed_count += 1
                
                # Remover metadados se existir
                metadata_file = os.path.join(backup_dir, f"backup_metadata_{file.replace('quality_backup_', '').replace('.zip', '')}.json")
                if os.path.exists(metadata_file):
                    os.remove(metadata_file)
                    print(f"   ✅ Metadados removidos: {os.path.basename(metadata_file)}")
                    
            except Exception as e:
                print(f"   ❌ Erro ao remover {file}: {e}")
        
        print(f"\n✅ {removed_count} backups antigos removidos")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar backups antigos: {e}")
        return False

def show_menu():
    """Exibe menu de opções"""
    print("\n📋 MENU DE BACKUP E RESTORE:")
    print("1. Criar backup")
    print("2. Restaurar backup")
    print("3. Listar backups")
    print("4. Remover backup")
    print("5. Limpar backups antigos")
    print("6. Verificar espaço em disco")
    print("0. Sair")
    
    return input("\nEscolha uma opção: ").strip()

def check_disk_space():
    """Verifica espaço em disco"""
    print("💾 Verificando espaço em disco...")
    
    try:
        import shutil
        
        # Verificar espaço no disco C:
        total, used, free = shutil.disk_usage("C:")
        
        total_gb = total // (1024**3)
        used_gb = used // (1024**3)
        free_gb = free // (1024**3)
        used_percent = (used / total) * 100
        
        print(f"\n📊 Disco C:")
        print(f"   Total: {total_gb:,} GB")
        print(f"   Usado: {used_gb:,} GB ({used_percent:.1f}%)")
        print(f"   Livre: {free_gb:,} GB")
        
        # Verificar espaço no diretório de backup
        backup_dir = "C:\\Quality\\Backup"
        if os.path.exists(backup_dir):
            backup_size = 0
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    backup_size += os.path.getsize(file_path)
            
            backup_size_gb = backup_size // (1024**3)
            print(f"\n📦 Backups:")
            print(f"   Tamanho total: {backup_size_gb:,} GB")
            print(f"   Arquivos: {len([f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))])}")
        
        # Avisos
        if free_gb < 5:
            print("\n⚠️  AVISO: Pouco espaço livre no disco!")
            print("   Considere limpar backups antigos ou liberar espaço")
        elif free_gb < 10:
            print("\n⚠️  AVISO: Espaço livre limitado")
            print("   Monitore o uso do disco")
        else:
            print("\n✅ Espaço em disco adequado")
        
    except Exception as e:
        print(f"❌ Erro ao verificar espaço em disco: {e}")

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Criar backup
            backup_file = create_backup()
            if backup_file:
                print(f"\n🎉 Backup criado com sucesso: {backup_file}")
            else:
                print("\n❌ Falha ao criar backup")
                
        elif choice == "2":
            # Restaurar backup
            if restore_backup():
                print("\n🎉 Backup restaurado com sucesso!")
            else:
                print("\n❌ Falha ao restaurar backup")
                
        elif choice == "3":
            # Listar backups
            list_backups()
            
        elif choice == "4":
            # Remover backup
            if delete_backup():
                print("\n🎉 Backup removido com sucesso!")
            else:
                print("\n❌ Falha ao remover backup")
                
        elif choice == "5":
            # Limpar backups antigos
            if cleanup_old_backups():
                print("\n🎉 Limpeza concluída com sucesso!")
            else:
                print("\n❌ Falha na limpeza")
                
        elif choice == "6":
            # Verificar espaço em disco
            check_disk_space()
            
        elif choice == "0":
            # Sair
            print("\n👋 Encerrando sistema de backup...")
            break
            
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Sistema de backup encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
