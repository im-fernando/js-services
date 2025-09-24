#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Loop do Servidor
Corrige o problema do servidor que termina em vez de ficar rodando
"""

import os
import shutil

def fix_server_loop():
    """Corrige problema do loop do servidor"""
    print("🔧 Corrigindo problema do loop do servidor...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        main_file = os.path.join(server_path, "main.py")
        
        if not os.path.exists(main_file):
            print(f"❌ Arquivo main.py não encontrado: {main_file}")
            return False
        
        print(f"   📝 Corrigindo: {main_file}")
        
        # Fazer backup
        backup_file = main_file + '.backup3'
        shutil.copy2(main_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir o problema
        old_code = """        server.start()
            
    except KeyboardInterrupt:"""
        
        new_code = """        server.start()
        
        # Manter o servidor rodando
        logger.info("🔄 Servidor rodando... Pressione Ctrl+C para parar")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Parando servidor...")
            server.stop()
            
    except KeyboardInterrupt:"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            
            # Salvar arquivo corrigido
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Problema do loop do servidor corrigido!")
        else:
            print("   ℹ️  Código já está correto ou não encontrado")
            return True
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir loop do servidor: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - LOOP DO SERVIDOR")
    print("=" * 60)
    print("Corrigindo problema do servidor que termina em vez de ficar rodando")
    print("=" * 60)
    print()
    
    # Corrigir loop do servidor
    if fix_server_loop():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Problema do loop do servidor corrigido")
        print("✅ Servidor agora ficará rodando continuamente")
        print()
        print("🚀 Agora você pode:")
        print("   1. Reiniciar o servidor")
        print("   2. O servidor ficará rodando (não terminará)")
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
