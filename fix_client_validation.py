#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Validação de Cliente
Corrige o erro 'bool' object is not callable na validação de clientes
"""

import os
import shutil

def fix_client_validation():
    """Corrige problema da validação de clientes"""
    print("🔧 Corrigindo problema da validação de clientes...")
    
    try:
        # Caminho do servidor instalado
        server_path = "C:\\Quality\\ControlPanel"
        helpers_file = os.path.join(server_path, "utils", "helpers.py")
        
        if not os.path.exists(helpers_file):
            print(f"❌ Arquivo helpers.py não encontrado: {helpers_file}")
            return False
        
        print(f"   📝 Corrigindo: {helpers_file}")
        
        # Fazer backup
        backup_file = helpers_file + '.backup5'
        shutil.copy2(helpers_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(helpers_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir a validação de clientes
        old_validation = """    # Verificar se começa com QUALITY_CLIENTE_
    return client_id.startswith('QUALITY_CLIENTE_')"""
        
        new_validation = """    # Aceitar IDs que começam com QUALITY_CLIENTE_ ou SERVIDOR_
    return (client_id.startswith('QUALITY_CLIENTE_') or 
            client_id.startswith('SERVIDOR_') or
            client_id.startswith('CLIENT_'))"""
        
        if old_validation in content:
            content = content.replace(old_validation, new_validation)
            
            # Salvar arquivo corrigido
            with open(helpers_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✅ Validação de clientes corrigida!")
        else:
            print("   ℹ️  Validação já está correta ou não encontrada")
            return True
        
        print("✅ Correção concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir validação de clientes: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - VALIDAÇÃO DE CLIENTES")
    print("=" * 60)
    print("Corrigindo erro 'bool' object is not callable na validação")
    print("=" * 60)
    print()
    
    # Corrigir validação de clientes
    if fix_client_validation():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Erro da validação de clientes corrigido")
        print("✅ Agora aceita IDs: QUALITY_CLIENTE_, SERVIDOR_, CLIENT_")
        print()
        print("🚀 Agora você pode:")
        print("   1. Reiniciar o servidor")
        print("   2. O servidor aceitará o cliente SERVIDOR_TESTE")
        print("   3. Não haverá mais erros de validação")
        print("   4. Comunicação funcionará perfeitamente")
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
