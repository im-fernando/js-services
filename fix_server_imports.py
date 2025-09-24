#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção Rápida - Imports do Servidor
Corrige problemas de importação no servidor instalado
"""

import os
import shutil
from pathlib import Path

def fix_server_imports():
    """Corrige imports no servidor instalado"""
    print("🔧 Corrigindo imports do servidor...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        
        if not os.path.exists(server_path):
            print(f"❌ Servidor não encontrado em: {server_path}")
            return False
        
        # Caminho do arquivo com problema
        auth_file = os.path.join(server_path, "utils", "auth.py")
        
        if os.path.exists(auth_file):
            print(f"   📝 Corrigindo: {auth_file}")
            
            # Ler arquivo
            with open(auth_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Corrigir import
            old_import = "from typing import Dict, Any, Optional, Tuple"
            new_import = "from typing import Dict, Any, Optional, Tuple, List"
            
            if old_import in content:
                content = content.replace(old_import, new_import)
                
                # Salvar arquivo corrigido
                with open(auth_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("   ✅ Import corrigido com sucesso!")
            else:
                print("   ℹ️  Import já está correto")
        else:
            print(f"   ❌ Arquivo não encontrado: {auth_file}")
            return False
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir imports: {e}")
        return False

def test_server_start():
    """Testa se o servidor inicia corretamente"""
    print("\n🧪 Testando inicialização do servidor...")
    
    try:
        import sys
        server_path = "C:\\Quality\\ControlPanel"
        
        if os.path.exists(server_path):
            # Adicionar ao path
            sys.path.insert(0, server_path)
            
            # Testar imports
            try:
                from utils.auth import QualityAuthManager
                print("   ✅ utils.auth importado com sucesso")
                
                from core.server import QualityControlServer
                print("   ✅ core.server importado com sucesso")
                
                from core.session_manager import SessionManager
                print("   ✅ core.session_manager importado com sucesso")
                
                from core.attendant_manager import AttendantManager
                print("   ✅ core.attendant_manager importado com sucesso")
                
                print("✅ Todos os imports funcionando!")
                return True
                
            except Exception as e:
                print(f"   ❌ Erro ao importar: {e}")
                return False
        else:
            print(f"   ❌ Servidor não encontrado: {server_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO RÁPIDA - IMPORTS DO SERVIDOR")
    print("=" * 60)
    print("Corrigindo problemas de importação no servidor")
    print("=" * 60)
    print()
    
    # Corrigir imports
    if fix_server_imports():
        # Testar servidor
        if test_server_start():
            print("\n" + "=" * 60)
            print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("✅ Imports corrigidos")
            print("✅ Servidor testado")
            print("✅ Pronto para uso!")
            print()
            print("🚀 Agora você pode executar:")
            print("   C:\\Quality\\ControlPanel\\start_server.bat")
            print("=" * 60)
        else:
            print("\n⚠️  Correção aplicada, mas teste falhou")
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
