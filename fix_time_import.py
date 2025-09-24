#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Import do Time
Corrige o erro 'name 'time' is not defined' no servidor
"""

import os
import shutil

def fix_time_import():
    """Corrige problema do import do time"""
    print("🔧 Corrigindo problema do import do time...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        main_file = os.path.join(server_path, "main.py")
        
        if not os.path.exists(main_file):
            print(f"❌ Arquivo main.py não encontrado: {main_file}")
            return False
        
        print(f"   📝 Corrigindo: {main_file}")
        
        # Fazer backup
        backup_file = main_file + '.backup4'
        shutil.copy2(main_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem o import
        if 'import time' in content:
            print("   ℹ️  Import do time já existe")
            return True
        
        # Adicionar import do time
        old_imports = """import sys
import os
import argparse
import signal
from pathlib import Path"""
        
        new_imports = """import sys
import os
import argparse
import signal
import time
from pathlib import Path"""
        
        if old_imports in content:
            content = content.replace(old_imports, new_imports)
            
            # Salvar arquivo corrigido
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Import do time adicionado!")
        else:
            print("   ℹ️  Estrutura de imports não encontrada")
            return False
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir import do time: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - IMPORT DO TIME")
    print("=" * 60)
    print("Corrigindo erro 'name 'time' is not defined' no servidor")
    print("=" * 60)
    print()
    
    # Corrigir import do time
    if fix_time_import():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Erro do import do time corrigido")
        print("✅ Servidor agora funcionará sem erros")
        print()
        print("🚀 Agora você pode:")
        print("   1. Reiniciar o servidor")
        print("   2. O servidor ficará rodando sem erros")
        print("   3. Testar a conectividade")
        print("   4. Conectar o cliente")
        print("=" * 60)
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
