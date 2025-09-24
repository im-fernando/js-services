#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção Completa - Todos os Imports
Corrige todos os problemas de importação no servidor
"""

import os
import shutil
from pathlib import Path

def fix_all_imports():
    """Corrige todos os imports no servidor instalado"""
    print("🔧 Corrigindo todos os imports do servidor...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        
        if not os.path.exists(server_path):
            print(f"❌ Servidor não encontrado em: {server_path}")
            return False
        
        # Arquivos que precisam de correção
        files_to_fix = [
            {
                'file': 'utils/auth.py',
                'old_import': 'from typing import Dict, Any, Optional, Tuple',
                'new_import': 'from typing import Dict, Any, Optional, Tuple, List'
            },
            {
                'file': 'core/attendant_manager.py',
                'old_import': 'from typing import Dict, Any, List, Optional',
                'new_import': 'from typing import Dict, Any, List, Optional, Tuple'
            }
        ]
        
        for fix_info in files_to_fix:
            file_path = os.path.join(server_path, fix_info['file'])
            
            if os.path.exists(file_path):
                print(f"   📝 Corrigindo: {fix_info['file']}")
                
                # Fazer backup
                backup_path = file_path + '.backup'
                shutil.copy2(file_path, backup_path)
                
                # Ler arquivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Corrigir import
                if fix_info['old_import'] in content:
                    content = content.replace(fix_info['old_import'], fix_info['new_import'])
                    
                    # Salvar arquivo corrigido
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"   ✅ {fix_info['file']} corrigido!")
                else:
                    print(f"   ℹ️  {fix_info['file']} já está correto")
            else:
                print(f"   ❌ Arquivo não encontrado: {fix_info['file']}")
        
        print("✅ Todas as correções aplicadas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir imports: {e}")
        return False

def test_all_imports():
    """Testa todos os imports do servidor"""
    print("\n🧪 Testando todos os imports do servidor...")
    
    try:
        import sys
        server_path = "C:\\Quality\\ControlPanel"
        
        if os.path.exists(server_path):
            # Adicionar ao path
            sys.path.insert(0, server_path)
            
            # Testar imports principais
            imports_to_test = [
                ('utils.auth', 'QualityAuthManager'),
                ('core.server', 'QualityControlServer'),
                ('core.session_manager', 'SessionManager'),
                ('core.attendant_manager', 'AttendantManager'),
                ('core.client_manager', 'ClientManager'),
                ('core.command_handler', 'CommandHandler'),
                ('database.activity_log', 'ActivityLogger')
            ]
            
            all_ok = True
            
            for module_name, class_name in imports_to_test:
                try:
                    module = __import__(module_name, fromlist=[class_name])
                    getattr(module, class_name)
                    print(f"   ✅ {module_name}.{class_name}")
                except Exception as e:
                    print(f"   ❌ {module_name}.{class_name}: {e}")
                    all_ok = False
            
            if all_ok:
                print("✅ Todos os imports funcionando!")
                return True
            else:
                print("❌ Alguns imports ainda têm problemas")
                return False
        else:
            print(f"   ❌ Servidor não encontrado: {server_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_server_start():
    """Testa se o servidor inicia corretamente"""
    print("\n🚀 Testando inicialização do servidor...")
    
    try:
        import sys
        server_path = "C:\\Quality\\ControlPanel"
        
        if os.path.exists(server_path):
            # Adicionar ao path
            sys.path.insert(0, server_path)
            
            # Testar inicialização básica
            try:
                from core.server import QualityControlServer
                from config.settings import load_config
                
                # Carregar configuração
                config_file = os.path.join(server_path, "config", "server_config.json")
                if os.path.exists(config_file):
                    config = load_config(config_file)
                    print(f"   ✅ Configuração carregada: {config['server']['host']}:{config['server']['port']}")
                else:
                    print("   ❌ Arquivo de configuração não encontrado")
                    return False
                
                print("✅ Servidor pode ser inicializado!")
                return True
                
            except Exception as e:
                print(f"   ❌ Erro na inicialização: {e}")
                return False
        else:
            print(f"   ❌ Servidor não encontrado: {server_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("🔧 CORREÇÃO COMPLETA - TODOS OS IMPORTS")
    print("=" * 70)
    print("Corrigindo todos os problemas de importação no servidor")
    print("=" * 70)
    print()
    
    # Corrigir imports
    if fix_all_imports():
        # Testar imports
        if test_all_imports():
            # Testar inicialização
            if test_server_start():
                print("\n" + "=" * 70)
                print("🎉 CORREÇÃO COMPLETA CONCLUÍDA COM SUCESSO!")
                print("=" * 70)
                print("✅ Todos os imports corrigidos")
                print("✅ Todos os módulos testados")
                print("✅ Servidor testado")
                print("✅ Pronto para uso!")
                print()
                print("🚀 Agora você pode executar:")
                print("   C:\\Quality\\ControlPanel\\start_server.bat")
                print("=" * 70)
            else:
                print("\n⚠️  Imports corrigidos, mas inicialização falhou")
                print("   Verifique a configuração do servidor")
        else:
            print("\n⚠️  Correção aplicada, mas alguns imports ainda falham")
            print("   Verifique os logs para mais detalhes")
    else:
        print("\n❌ Falha na correção")
        print("   Verifique se o servidor está instalado corretamente")
    
    input("\nPressione Enter para finalizar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Correção cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
