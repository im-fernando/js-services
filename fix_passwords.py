#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção - Senhas dos Usuários
Corrige os hashes das senhas no arquivo de configuração
"""

import os
import shutil

def fix_passwords():
    """Corrige as senhas dos usuários"""
    print("🔧 Corrigindo senhas dos usuários...")
    
    try:
        # Caminho do servidor instalado
        users_file = "C:\\Quality\\ControlPanel\\config\\users_config.json"
        
        if not os.path.exists(users_file):
            print(f"❌ Arquivo não encontrado: {users_file}")
            return False
        
        print(f"   📝 Corrigindo: {users_file}")
        
        # Fazer backup
        backup_file = users_file + '.backup_passwords'
        shutil.copy2(users_file, backup_file)
        print(f"   💾 Backup criado: {backup_file}")
        
        # Ler arquivo
        with open(users_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hash correto da senha "quality123"
        correct_hash = "0f840d7354d0873e3054340243d745a0670ca3da75acb727e75228afee529bbb"
        old_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        
        # Substituir hash incorreto pelo correto
        if old_hash in content:
            content = content.replace(old_hash, correct_hash)
            print(f"   ✅ Hash da senha corrigido: {old_hash} → {correct_hash}")
        else:
            print("   ℹ️  Hash já está correto ou não encontrado")
            return True
        
        # Salvar arquivo corrigido
        with open(users_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Senhas dos usuários corrigidas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir senhas: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 CORREÇÃO - SENHAS DOS USUÁRIOS")
    print("=" * 60)
    print("Corrigindo hashes das senhas no arquivo de configuração")
    print("=" * 60)
    print()
    
    if fix_passwords():
        print("\n" + "=" * 60)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("✅ Senhas dos usuários corrigidas")
        print("✅ Hash da senha 'quality123' atualizado")
        print()
        print("👤 USUÁRIOS DISPONÍVEIS:")
        print("   - admin / quality123 (Administrador)")
        print("   - joao.silva / quality123 (Suporte Sênior)")
        print("   - maria.santos / quality123 (Suporte Júnior)")
        print()
        print("🚀 Agora você pode:")
        print("   1. Tentar fazer login novamente")
        print("   2. Usar as senhas corretas")
        print("   3. Acessar o sistema normalmente")
        print("=" * 60)
    else:
        print("\n❌ Falha na correção das senhas")
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
