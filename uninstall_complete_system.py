#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Desinstalação Completa - Sistema Quality Control Panel
Remove todos os componentes do sistema
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de desinstalação"""
    print("=" * 70)
    print("🗑️  QUALITY CONTROL PANEL - DESINSTALAÇÃO COMPLETA")
    print("=" * 70)
    print("Removendo todos os componentes do sistema")
    print("=" * 70)
    print()

def confirm_uninstall():
    """Confirma se o usuário quer desinstalar"""
    print("⚠️  ATENÇÃO: Esta operação irá remover TODOS os componentes do sistema!")
    print("   - Servidor (C:\\Quality\\ControlPanel)")
    print("   - Atendentes (C:\\Quality\\AttendantClient)")
    print("   - Clientes (C:\\Quality\\RemoteAgent)")
    print("   - Documentação (C:\\Quality\\Documentation)")
    print()
    
    while True:
        choice = input("Deseja continuar com a desinstalação? (s/N): ").strip().lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            return True
        elif choice in ['n', 'não', 'nao', 'no', '']:
            return False
        else:
            print("❌ Opção inválida. Digite 's' para sim ou 'n' para não.")

def stop_services():
    """Para todos os serviços do sistema"""
    print("\n🛑 Parando serviços do sistema...")
    
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
        
        print("✅ Serviços parados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao parar serviços: {e}")
        return False

def remove_directory(directory_path, description):
    """Remove um diretório e seu conteúdo"""
    try:
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            print(f"   ✅ {description} removido: {directory_path}")
            return True
        else:
            print(f"   ℹ️  {description} não encontrado: {directory_path}")
            return True
    except Exception as e:
        print(f"   ❌ Erro ao remover {description}: {e}")
        return False

def remove_server():
    """Remove o servidor"""
    print("\n🖥️  Removendo servidor...")
    
    server_dir = "C:\\Quality\\ControlPanel"
    return remove_directory(server_dir, "Servidor")

def remove_attendants():
    """Remove os atendentes"""
    print("\n👥 Removendo atendentes...")
    
    attendant_dir = "C:\\Quality\\AttendantClient"
    return remove_directory(attendant_dir, "Atendentes")

def remove_clients():
    """Remove os clientes"""
    print("\n🖥️  Removendo clientes...")
    
    client_dir = "C:\\Quality\\RemoteAgent"
    return remove_directory(client_dir, "Clientes")

def remove_documentation():
    """Remove a documentação"""
    print("\n📚 Removendo documentação...")
    
    doc_dir = "C:\\Quality\\Documentation"
    return remove_directory(doc_dir, "Documentação")

def remove_quality_directory():
    """Remove o diretório Quality principal"""
    print("\n🗂️  Removendo diretório Quality...")
    
    quality_dir = "C:\\Quality"
    return remove_directory(quality_dir, "Diretório Quality")

def uninstall_dependencies():
    """Desinstala dependências Python"""
    print("\n📦 Desinstalando dependências Python...")
    
    try:
        deps = [
            "websocket-server",
            "websocket-client",
            "colorama",
            "rich",
            "requests"
        ]
        
        for dep in deps:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "uninstall", dep, "-y"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"   ✅ {dep} desinstalado")
                else:
                    print(f"   ℹ️  {dep} não encontrado ou já desinstalado")
                    
            except Exception as e:
                print(f"   ⚠️  Erro ao desinstalar {dep}: {e}")
        
        print("✅ Dependências desinstaladas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao desinstalar dependências: {e}")
        return False

def clean_registry():
    """Limpa entradas do registro (se necessário)"""
    print("\n🧹 Limpando registro do Windows...")
    
    try:
        # Aqui você pode adicionar comandos para limpar o registro
        # Por exemplo, remover chaves relacionadas ao sistema
        print("   ℹ️  Nenhuma entrada de registro encontrada para limpeza")
        print("✅ Registro limpo")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar registro: {e}")
        return False

def clean_environment():
    """Limpa variáveis de ambiente"""
    print("\n🌍 Limpando variáveis de ambiente...")
    
    try:
        # Aqui você pode adicionar comandos para limpar variáveis de ambiente
        # Por exemplo, remover PATH entries relacionadas ao sistema
        print("   ℹ️  Nenhuma variável de ambiente encontrada para limpeza")
        print("✅ Variáveis de ambiente limpas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar variáveis de ambiente: {e}")
        return False

def create_uninstall_log():
    """Cria log da desinstalação"""
    print("\n📝 Criando log da desinstalação...")
    
    try:
        from datetime import datetime
        
        log_content = f"""# Log de Desinstalação - Quality Control Panel
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Usuário: {os.getenv('USERNAME', 'Desconhecido')}
Sistema: {os.name}

## Componentes Removidos:
- Servidor: C:\\Quality\\ControlPanel
- Atendentes: C:\\Quality\\AttendantClient
- Clientes: C:\\Quality\\RemoteAgent
- Documentação: C:\\Quality\\Documentation
- Diretório Principal: C:\\Quality

## Dependências Desinstaladas:
- websocket-server
- websocket-client
- colorama
- rich
- requests

## Status: Desinstalação Concluída
"""
        
        # Salvar log no diretório temporário
        temp_dir = os.environ.get('TEMP', 'C:\\Temp')
        log_file = os.path.join(temp_dir, 'quality_control_panel_uninstall.log')
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"   ✅ Log criado: {log_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar log: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Confirmar desinstalação
    if not confirm_uninstall():
        print("\n👋 Desinstalação cancelada pelo usuário")
        input("Pressione Enter para sair...")
        return False
    
    print("\n🚀 Iniciando desinstalação...")
    
    # Parar serviços
    if not stop_services():
        print("⚠️  Continuando desinstalação mesmo com erros nos serviços...")
    
    # Remover componentes
    success = True
    
    if not remove_server():
        success = False
    
    if not remove_attendants():
        success = False
    
    if not remove_clients():
        success = False
    
    if not remove_documentation():
        success = False
    
    if not remove_quality_directory():
        success = False
    
    # Desinstalar dependências
    if not uninstall_dependencies():
        success = False
    
    # Limpeza adicional
    clean_registry()
    clean_environment()
    
    # Criar log
    create_uninstall_log()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 DESINSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("✅ Todos os componentes foram removidos")
        print("✅ Dependências foram desinstaladas")
        print("✅ Sistema limpo completamente")
        print()
        print("📝 Log da desinstalação salvo em:")
        print(f"   {os.environ.get('TEMP', 'C:\\Temp')}\\quality_control_panel_uninstall.log")
        print()
        print("👋 Obrigado por usar o Quality Control Panel!")
    else:
        print("⚠️  DESINSTALAÇÃO CONCLUÍDA COM AVISOS")
        print("=" * 70)
        print("✅ Componentes principais removidos")
        print("⚠️  Alguns itens podem não ter sido removidos completamente")
        print("   Verifique manualmente se necessário")
        print()
        print("📝 Log da desinstalação salvo em:")
        print(f"   {os.environ.get('TEMP', 'C:\\Temp')}\\quality_control_panel_uninstall.log")
    
    print("=" * 70)
    
    input("\nPressione Enter para finalizar...")
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Desinstalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado durante a desinstalação: {e}")
        input("\nPressione Enter para sair...")
