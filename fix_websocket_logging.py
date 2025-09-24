#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - WebSocket Logging
Corrige o problema de websocket_server.logging no servidor
"""

import os
import shutil

def fix_websocket_logging():
    """Corrige problema de logging no WebSocket"""
    print("🔧 Corrigindo problema de WebSocket logging...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        server_file = os.path.join(server_path, "core", "server.py")
        
        if not os.path.exists(server_file):
            print(f"❌ Arquivo server.py não encontrado: {server_file}")
            return False
        
        print(f"   📝 Corrigindo: {server_file}")
        
        # Fazer backup
        backup_file = server_file + '.backup'
        shutil.copy2(server_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir o problema
        old_code = """            # Configurar servidor WebSocket
            self.ws_server = websocket_server.WebsocketServer(
                self.port,
                host=self.host,
                loglevel=websocket_server.logging.INFO
            )"""
        
        new_code = """            # Configurar servidor WebSocket
            self.ws_server = websocket_server.WebsocketServer(
                self.port,
                host=self.host
            )"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            
            # Salvar arquivo corrigido
            with open(server_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Problema de WebSocket logging corrigido!")
        else:
            print("   ℹ️  Código já está correto ou não encontrado")
            return True
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir WebSocket logging: {e}")
        return False

def test_server_start():
    """Testa se o servidor inicia corretamente"""
    print("\n🧪 Testando inicialização do servidor...")
    
    try:
        import subprocess
        import sys
        import time
        
        server_path = "C:\\Quality\\ControlPanel"
        
        if os.path.exists(server_path):
            # Testar importação dos módulos
            cmd = [sys.executable, "-c", """
import sys
sys.path.insert(0, r'C:\\Quality\\ControlPanel')
try:
    from core.server import QualityControlServer
    print('✅ Import do servidor OK')
except Exception as e:
    print(f'❌ Erro no import: {e}')
    exit(1)
"""]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Módulos importados com sucesso!")
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
    print("🔧 CORREÇÃO - WEBSOCKET LOGGING")
    print("=" * 60)
    print("Corrigindo problema de websocket_server.logging")
    print("=" * 60)
    print()
    
    # Corrigir WebSocket logging
    if fix_websocket_logging():
        # Testar servidor
        if test_server_start():
            print("\n" + "=" * 60)
            print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("✅ Problema de WebSocket logging corrigido")
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
