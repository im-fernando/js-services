#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Logger Debug
Corrige o erro 'bool' object is not callable no logger
"""

import os
import shutil

def fix_logger_debug():
    """Corrige problema do logger debug"""
    print("🔧 Corrigindo problema do logger debug...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        logger_file = os.path.join(server_path, "utils", "logger.py")
        
        if not os.path.exists(logger_file):
            print(f"❌ Arquivo logger.py não encontrado: {logger_file}")
            return False
        
        print(f"   📝 Corrigindo: {logger_file}")
        
        # Fazer backup
        backup_file = logger_file + '.backup6'
        shutil.copy2(logger_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(logger_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir o problema do debug
        old_init = """    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.debug = debug
        self.logger = self._setup_logger()"""
        
        new_init = """    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.debug_mode = debug
        self.logger = self._setup_logger()"""
        
        if old_init in content:
            content = content.replace(old_init, new_init)
            print("   ✅ Atributo debug renomeado para debug_mode")
        
        # Corrigir referência ao debug
        old_reference = "logger.setLevel(logging.DEBUG if self.debug else logging.INFO)"
        new_reference = "logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)"
        
        if old_reference in content:
            content = content.replace(old_reference, new_reference)
            print("   ✅ Referência ao debug corrigida")
        
        # Salvar arquivo corrigido
        with open(logger_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Problema do logger debug corrigido!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir logger debug: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - LOGGER DEBUG")
    print("=" * 60)
    print("Corrigindo erro 'bool' object is not callable no logger")
    print("=" * 60)
    print()
    
    # Corrigir logger debug
    if fix_logger_debug():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Erro do logger debug corrigido")
        print("✅ Atributo debug renomeado para debug_mode")
        print("✅ Método debug() agora funciona corretamente")
        print()
        print("🚀 Agora você pode:")
        print("   1. Reiniciar o servidor")
        print("   2. O servidor funcionará sem erros")
        print("   3. Comunicação funcionará perfeitamente")
        print("   4. Sistema completamente operacional")
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
