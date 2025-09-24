#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Debug - Erro do Servidor
Identifica exatamente onde está ocorrendo o erro 'bool' object is not callable
"""

import os
import traceback
import sys

def add_debug_to_server():
    """Adiciona código de debug ao servidor"""
    print("🔍 Adicionando código de debug ao servidor...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        server_file = os.path.join(server_path, "core", "server.py")
        
        if not os.path.exists(server_file):
            print(f"❌ Arquivo server.py não encontrado: {server_file}")
            return False
        
        print(f"   📝 Adicionando debug: {server_file}")
        
        # Ler arquivo
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar import do traceback
        if "import traceback" not in content:
            content = content.replace("import threading", "import threading\nimport traceback")
        
        # Adicionar debug no método _process_message
        old_process = """        except Exception as e:
            self.logger.error(f"❌ Erro ao processar mensagem de {client_id}: {e}")"""
        
        new_process = """        except Exception as e:
            # Debug detalhado do erro
            error_traceback = traceback.format_exc()
            self.logger.error(f"❌ Erro ao processar mensagem de {client_id}: {e}")
            self.logger.error(f"📋 Traceback completo:\\n{error_traceback}")
            print(f"DEBUG - Erro detalhado: {e}")
            print(f"DEBUG - Traceback:\\n{error_traceback}")"""
        
        if old_process in content:
            content = content.replace(old_process, new_process)
            print("   ✅ Debug adicionado ao _process_message")
        
        # Adicionar debug no método message_received
        old_received = """        except Exception as e:
            self.logger.error(f"❌ Erro ao processar mensagem: {e}")"""
        
        new_received = """        except Exception as e:
            # Debug detalhado do erro
            error_traceback = traceback.format_exc()
            self.logger.error(f"❌ Erro ao processar mensagem: {e}")
            self.logger.error(f"📋 Traceback completo:\\n{error_traceback}")
            print(f"DEBUG - Erro detalhado: {e}")
            print(f"DEBUG - Traceback:\\n{error_traceback}")"""
        
        if old_received in content:
            content = content.replace(old_received, new_received)
            print("   ✅ Debug adicionado ao message_received")
        
        # Salvar arquivo com debug
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Código de debug adicionado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar debug: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔍 DEBUG - ERRO DO SERVIDOR")
    print("=" * 60)
    print("Adicionando código de debug para identificar erro específico")
    print("=" * 60)
    print()
    
    # Adicionar debug ao servidor
    if add_debug_to_server():
        print("\n" + "=" * 60)
        print("🎉 DEBUG ADICIONADO COM SUCESSO!")
        print("=" * 60)
        print("✅ Código de debug adicionado ao servidor")
        print("✅ Agora mostrará traceback completo dos erros")
        print()
        print("🚀 Próximos passos:")
        print("   1. Reinicie o servidor")
        print("   2. Conecte o cliente")
        print("   3. Observe o traceback detalhado")
        print("   4. Identifique exatamente onde está o erro")
        print("=" * 60)
    else:
        print("\n❌ Falha ao adicionar debug")
        print("   Verifique se o servidor está instalado corretamente")
    
    input("\nPressione Enter para finalizar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Debug cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
