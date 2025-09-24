#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção Rápida - Logger Debug
Corrige diretamente o arquivo instalado
"""

import os
import shutil

def fix_logger_quick():
    """Corrige rapidamente o problema do logger"""
    print("🔧 Corrigindo rapidamente o problema do logger...")
    
    try:
        # Caminho do servidor instalado
        logger_file = "C:\\Quality\\ControlPanel\\utils\\logger.py"
        
        if not os.path.exists(logger_file):
            print(f"❌ Arquivo não encontrado: {logger_file}")
            return False
        
        print(f"   📝 Corrigindo: {logger_file}")
        
        # Fazer backup
        backup_file = logger_file + '.backup_quick'
        shutil.copy2(logger_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(logger_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Corrigir linha por linha
        fixed_lines = []
        for i, line in enumerate(lines):
            # Corrigir self.debug = debug
            if "self.debug = debug" in line:
                fixed_lines.append(line.replace("self.debug = debug", "self.debug_mode = debug"))
                print(f"   ✅ Linha {i+1}: self.debug = debug → self.debug_mode = debug")
            # Corrigir self.debug em logger.setLevel
            elif "self.debug" in line and "logger.setLevel" in line:
                fixed_lines.append(line.replace("self.debug", "self.debug_mode"))
                print(f"   ✅ Linha {i+1}: self.debug → self.debug_mode")
            else:
                fixed_lines.append(line)
        
        # Salvar arquivo corrigido
        with open(logger_file, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("✅ Correção rápida concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na correção rápida: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO RÁPIDA - LOGGER DEBUG")
    print("=" * 60)
    print("Corrigindo diretamente o arquivo instalado")
    print("=" * 60)
    print()
    
    if fix_logger_quick():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO RÁPIDA CONCLUÍDA!")
        print("=" * 60)
        print("✅ Problema do logger corrigido")
        print("✅ Arquivo instalado atualizado")
        print()
        print("🚀 Agora:")
        print("   1. Pare o servidor (Ctrl+C)")
        print("   2. Reinicie o servidor")
        print("   3. O erro não ocorrerá mais")
        print("=" * 60)
    else:
        print("\n❌ Falha na correção rápida")
    
    input("\nPressione Enter para finalizar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Correção cancelada")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        input("\nPressione Enter para sair...")
