#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Argumentos do Servidor
Corrige o argumento --multi-attendant no main.py
"""

import os
import shutil

def fix_server_args():
    """Corrige argumentos no servidor instalado"""
    print("🔧 Corrigindo argumentos do servidor...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        main_file = os.path.join(server_path, "main.py")
        
        if not os.path.exists(main_file):
            print(f"❌ Arquivo main.py não encontrado: {main_file}")
            return False
        
        print(f"   📝 Corrigindo: {main_file}")
        
        # Fazer backup
        backup_file = main_file + '.backup'
        shutil.copy2(main_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem o argumento
        if '--multi-attendant' in content:
            print("   ℹ️  Argumento --multi-attendant já existe")
            return True
        
        # Adicionar o argumento
        old_line = "    parser.add_argument('--quality-mode', action='store_true',\n                       help='Modo específico para serviços Quality')"
        new_line = "    parser.add_argument('--quality-mode', action='store_true',\n                       help='Modo específico para serviços Quality')\n    parser.add_argument('--multi-attendant', action='store_true',\n                       help='Modo multi-atendente (padrão)')"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # Salvar arquivo corrigido
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Argumento --multi-attendant adicionado!")
        else:
            print("   ⚠️  Não foi possível encontrar a linha para substituir")
            return False
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir argumentos: {e}")
        return False

def test_server_start():
    """Testa se o servidor inicia corretamente"""
    print("\n🧪 Testando inicialização do servidor...")
    
    try:
        import subprocess
        import sys
        
        server_path = "C:\\Quality\\ControlPanel"
        
        if os.path.exists(server_path):
            # Testar comando de inicialização
            cmd = [sys.executable, "main.py", "--multi-attendant", "--help"]
            
            result = subprocess.run(cmd, cwd=server_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Argumento --multi-attendant reconhecido!")
                print("   ✅ Servidor pode ser inicializado!")
                return True
            else:
                print(f"   ❌ Erro: {result.stderr}")
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
    print("🔧 CORREÇÃO - ARGUMENTOS DO SERVIDOR")
    print("=" * 60)
    print("Corrigindo argumento --multi-attendant no main.py")
    print("=" * 60)
    print()
    
    # Corrigir argumentos
    if fix_server_args():
        # Testar servidor
        if test_server_start():
            print("\n" + "=" * 60)
            print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("✅ Argumento --multi-attendant adicionado")
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
