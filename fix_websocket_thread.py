#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - WebSocket Thread
Corrige o problema de thread do WebSocket server
"""

import os
import shutil

def fix_websocket_thread():
    """Corrige problema de thread do WebSocket"""
    print("🔧 Corrigindo problema de WebSocket thread...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        server_file = os.path.join(server_path, "core", "server.py")
        
        if not os.path.exists(server_file):
            print(f"❌ Arquivo server.py não encontrado: {server_file}")
            return False
        
        print(f"   📝 Corrigindo: {server_file}")
        
        # Fazer backup
        backup_file = server_file + '.backup2'
        shutil.copy2(server_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir o problema
        old_code = """            self.server_thread.start()
            
        except ImportError:"""
        
        new_code = """            self.server_thread.start()
            
            # Aguardar um pouco para garantir que o servidor iniciou
            time.sleep(1)
            
        except ImportError:"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            
            # Salvar arquivo corrigido
            with open(server_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Problema de WebSocket thread corrigido!")
        else:
            print("   ℹ️  Código já está correto ou não encontrado")
            return True
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir WebSocket thread: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - WEBSOCKET THREAD")
    print("=" * 60)
    print("Corrigindo problema de thread do WebSocket server")
    print("=" * 60)
    print()
    
    # Corrigir WebSocket thread
    if fix_websocket_thread():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Problema de WebSocket thread corrigido")
        print("✅ Servidor deve funcionar agora")
        print()
        print("🚀 Agora você pode:")
        print("   1. Reiniciar o servidor")
        print("   2. Testar a conectividade")
        print("   3. Conectar o cliente")
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
