#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface CLI Administrativa
Interface para administradores gerenciarem o sistema
"""

import sys
import os
import time
import getpass
from typing import Dict, Any, List, Optional
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(str(os.path.dirname(os.path.dirname(__file__))))

from utils.auth import QualityAuthManager
from utils.helpers import format_timestamp

class AdminCLI:
    """Interface CLI administrativa"""
    
    def __init__(self):
        self.auth_manager = QualityAuthManager()
        self.current_admin = None
        
    def print_banner(self):
        """Exibe banner administrativo"""
        print("=" * 70)
        print("🔧 QUALITY CONTROL PANEL - ADMINISTRAÇÃO")
        print("=" * 70)
        print("Interface administrativa do sistema")
        print("=" * 70)
        print()
    
    def admin_login(self) -> bool:
        """Realiza login administrativo"""
        self.print_banner()
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                print(f"Tentativa {attempts + 1} de {max_attempts}")
                print("-" * 40)
                
                username = input("Usuário Administrativo: ").strip()
                if not username:
                    print("❌ Usuário não pode estar vazio")
                    attempts += 1
                    continue
                
                password = getpass.getpass("Senha: ")
                if not password:
                    print("❌ Senha não pode estar vazia")
                    attempts += 1
                    continue
                
                # Autenticar
                success, user_data, message = self.auth_manager.authenticate_user(username, password)
                
                if success and user_data.get('role') == 'administrator':
                    self.current_admin = user_data
                    print(f"\n🟢 {message}")
                    print(f"Bem-vindo, {user_data['display_name']} (Administrador)")
                    return True
                else:
                    if success:
                        print(f"\n❌ Acesso negado: Usuário não é administrador")
                    else:
                        print(f"\n❌ {message}")
                    attempts += 1
                    
            except KeyboardInterrupt:
                print("\n👋 Login cancelado pelo usuário")
                return False
            except Exception as e:
                print(f"\n❌ Erro no login: {e}")
                attempts += 1
        
        print(f"\n❌ Máximo de tentativas excedido. Acesso negado.")
        return False
    
    def show_admin_dashboard(self):
        """Exibe dashboard administrativo"""
        print("\n" + "=" * 70)
        print("🔧 PAINEL ADMINISTRATIVO")
        print("=" * 70)
        print(f"🕐 {datetime.now().strftime('%H:%M:%S')} | Admin: {self.current_admin['display_name']}")
        print()
        
        # Estatísticas do sistema (simuladas)
        print("📊 ESTATÍSTICAS DO SISTEMA:")
        print("   Total de Atendentes: 5")
        print("   Sessões Ativas: 3")
        print("   Comandos Executados Hoje: 47")
        print("   Clientes Atendidos: 12")
        print("   Uptime do Servidor: 99.8%")
        print()
        
        # Alertas críticos
        print("🚨 ALERTAS CRÍTICOS:")
        print("   ⚠️  Cliente DEF offline há 2 horas")
        print("   ⚠️  Muitos reinicializações no Posto GHI (5x hoje)")
        print("   ⚠️  ServicoFiscal instável em 3 postos")
        print()
        
        # Atendentes ativos
        print("👥 ATENDENTES ATIVOS:")
        print("   João Silva (14:35) → Posto ABC [Reiniciando serviços]")
        print("   Maria Santos (13:20) → Dashboard [Monitorando]")
        print("   Pedro Costa (15:10) → Posto XYZ [Visualizando logs]")
        print()
    
    def show_admin_menu(self):
        """Exibe menu administrativo"""
        print("=== MENU ADMINISTRATIVO ===")
        print("1. 👥 Gerenciar Atendentes")
        print("2. 🔐 Gerenciar Permissões")
        print("3. 📊 Relatórios e Estatísticas")
        print("4. 🔧 Configurações do Sistema")
        print("5. 📋 Logs do Sistema")
        print("6. 🚨 Monitoramento de Alertas")
        print("7. 💾 Backup e Restauração")
        print("8. 🔄 Manutenção do Sistema")
        print("0. Logout")
        print()
    
    def show_attendants_management(self):
        """Exibe gerenciamento de atendentes"""
        print("\n=== GERENCIAMENTO DE ATENDENTES ===")
        print()
        print("👥 ATENDENTES CADASTRADOS:")
        print("1. João Silva (joao.silva) - Suporte Sênior - Ativo")
        print("2. Maria Santos (maria.santos) - Suporte Júnior - Ativo")
        print("3. Pedro Costa (pedro.costa) - Suporte Sênior - Ativo")
        print("4. Ana Lima (ana.lima) - Administrador - Ativo")
        print("5. Carlos Silva (carlos.silva) - Suporte Júnior - Inativo")
        print()
        print("Ações:")
        print("A. Adicionar Novo Atendente")
        print("E. Editar Atendente")
        print("D. Desativar/Ativar Atendente")
        print("R. Redefinir Senha")
        print("V. Ver Detalhes")
        print("0. Voltar")
        print()
    
    def show_permissions_management(self):
        """Exibe gerenciamento de permissões"""
        print("\n=== GERENCIAMENTO DE PERMISSÕES ===")
        print()
        print("🔐 PAPÉIS DISPONÍVEIS:")
        print("1. Administrador - Acesso total ao sistema")
        print("2. Suporte Sênior - Acesso amplo com algumas restrições")
        print("3. Suporte Júnior - Acesso limitado")
        print()
        print("📋 PERMISSÕES POR PAPEL:")
        print("   Administrador:")
        print("   ✅ Reiniciar serviços")
        print("   ✅ Finalizar processos")
        print("   ✅ Visualizar logs")
        print("   ✅ Gerenciar todos os clientes")
        print("   ✅ Ações críticas")
        print("   ✅ Gerenciar atendentes")
        print("   ✅ Ver todas as sessões")
        print()
        print("   Suporte Sênior:")
        print("   ✅ Reiniciar serviços")
        print("   ✅ Finalizar processos")
        print("   ✅ Visualizar logs")
        print("   ✅ Gerenciar todos os clientes")
        print("   ✅ Ações críticas")
        print("   ❌ Gerenciar atendentes")
        print("   ❌ Ver todas as sessões")
        print()
        print("   Suporte Júnior:")
        print("   ✅ Reiniciar serviços")
        print("   ❌ Finalizar processos")
        print("   ✅ Visualizar logs")
        print("   ❌ Gerenciar todos os clientes")
        print("   ❌ Ações críticas")
        print("   ❌ Gerenciar atendentes")
        print("   ❌ Ver todas as sessões")
        print()
        print("Ações:")
        print("E. Editar Papel")
        print("C. Criar Novo Papel")
        print("D. Deletar Papel")
        print("0. Voltar")
        print()
    
    def show_reports_and_statistics(self):
        """Exibe relatórios e estatísticas"""
        print("\n=== RELATÓRIOS E ESTATÍSTICAS ===")
        print()
        print("📊 RELATÓRIOS DISPONÍVEIS:")
        print("1. 📈 Relatório de Atividade Diária")
        print("2. 👥 Relatório de Atendentes")
        print("3. 🖥️  Relatório de Clientes")
        print("4. ⚡ Relatório de Comandos")
        print("5. 🚨 Relatório de Alertas")
        print("6. 📋 Relatório de Logs")
        print()
        print("📅 PERÍODOS:")
        print("H. Hoje")
        print("S. Esta Semana")
        print("M. Este Mês")
        print("A. Ano Atual")
        print("C. Personalizado")
        print()
        print("0. Voltar")
        print()
    
    def show_system_settings(self):
        """Exibe configurações do sistema"""
        print("\n=== CONFIGURAÇÕES DO SISTEMA ===")
        print()
        print("⚙️  CONFIGURAÇÕES GERAIS:")
        print("   Servidor:")
        print("   - Host: 0.0.0.0")
        print("   - Porta: 8765")
        print("   - Timeout de Sessão: 3600s")
        print("   - Timeout de Cliente: 300s")
        print()
        print("   Qualidade:")
        print("   - Serviços Monitorados: 5")
        print("   - Intervalo de Heartbeat: 30s")
        print("   - Intervalo de Logs: 1s")
        print()
        print("   Segurança:")
        print("   - Autenticação: Obrigatória")
        print("   - Criptografia: SHA-256")
        print("   - Log de Auditoria: Ativo")
        print()
        print("Ações:")
        print("E. Editar Configurações")
        print("R. Restaurar Padrões")
        print("T. Testar Configurações")
        print("0. Voltar")
        print()
    
    def show_system_logs(self):
        """Exibe logs do sistema"""
        print("\n=== LOGS DO SISTEMA ===")
        print()
        print("📋 LOGS RECENTES:")
        print("   [14:35:22] INFO - João Silva logou no sistema")
        print("   [14:35:23] INFO - Maria Santos conectou ao Posto ABC")
        print("   [14:35:24] WARNING - Cliente DEF não responde há 2 horas")
        print("   [14:35:25] ERROR - Falha na conexão com Posto GHI")
        print("   [14:35:26] INFO - Pedro Costa executou comando restart_service")
        print("   [14:35:27] INFO - Ana Lima acessou painel administrativo")
        print("   [14:35:28] WARNING - Muitos reinicializações no Posto GHI")
        print("   [14:35:29] INFO - Sistema de backup executado com sucesso")
        print()
        print("🔍 FILTROS:")
        print("L. Por Nível (INFO, WARNING, ERROR)")
        print("U. Por Usuário")
        print("T. Por Período")
        print("S. Por Serviço")
        print("E. Exportar Logs")
        print("0. Voltar")
        print()
    
    def show_alerts_monitoring(self):
        """Exibe monitoramento de alertas"""
        print("\n=== MONITORAMENTO DE ALERTAS ===")
        print()
        print("🚨 ALERTAS ATIVOS:")
        print("   🔴 CRÍTICO - Cliente DEF offline há 2 horas")
        print("      Cliente: Posto Quality DEF")
        print("      Última atividade: 12:30:15")
        print("      Ação sugerida: Verificar conectividade")
        print()
        print("   🟡 MÉDIO - Muitos reinicializações no Posto GHI")
        print("      Cliente: Posto Quality GHI")
        print("      Reinicializações hoje: 5")
        print("      Ação sugerida: Investigar causa raiz")
        print()
        print("   🟡 MÉDIO - ServicoFiscal instável")
        print("      Clientes afetados: 3")
        print("      Última ocorrência: 14:20:30")
        print("      Ação sugerida: Atualizar serviço")
        print()
        print("📊 ESTATÍSTICAS DE ALERTAS:")
        print("   Total hoje: 8")
        print("   Críticos: 1")
        print("   Médios: 5")
        print("   Baixos: 2")
        print("   Resolvidos: 3")
        print()
        print("Ações:")
        print("R. Resolver Alerta")
        print("A. Ajustar Configurações")
        print("N. Criar Notificação")
        print("0. Voltar")
        print()
    
    def show_backup_restore(self):
        """Exibe backup e restauração"""
        print("\n=== BACKUP E RESTAURAÇÃO ===")
        print()
        print("💾 BACKUPS DISPONÍVEIS:")
        print("1. backup_20250122_143000.tar.gz - 2.5 MB - Hoje 14:30")
        print("2. backup_20250121_143000.tar.gz - 2.4 MB - Ontem 14:30")
        print("3. backup_20250120_143000.tar.gz - 2.3 MB - 2 dias atrás")
        print("4. backup_20250119_143000.tar.gz - 2.2 MB - 3 dias atrás")
        print()
        print("📊 ESTATÍSTICAS:")
        print("   Último backup: Hoje 14:30")
        print("   Próximo backup: Hoje 20:00")
        print("   Tamanho médio: 2.4 MB")
        print("   Retenção: 30 dias")
        print()
        print("Ações:")
        print("C. Criar Backup Agora")
        print("R. Restaurar Backup")
        print("D. Download Backup")
        print("S. Configurar Agendamento")
        print("0. Voltar")
        print()
    
    def show_system_maintenance(self):
        """Exibe manutenção do sistema"""
        print("\n=== MANUTENÇÃO DO SISTEMA ===")
        print()
        print("🔧 OPERAÇÕES DE MANUTENÇÃO:")
        print("1. 🧹 Limpeza de Logs Antigos")
        print("2. 🔄 Reinicialização do Servidor")
        print("3. 📊 Otimização do Banco de Dados")
        print("4. 🔍 Verificação de Integridade")
        print("5. 📈 Análise de Performance")
        print("6. 🛡️  Verificação de Segurança")
        print()
        print("⚠️  OPERAÇÕES CRÍTICAS:")
        print("R. Reiniciar Todos os Serviços")
        print("S. Parar Sistema")
        print("U. Atualizar Sistema")
        print("F. Verificação Completa")
        print()
        print("📊 STATUS DO SISTEMA:")
        print("   Uptime: 15 dias, 8 horas")
        print("   Uso de CPU: 12%")
        print("   Uso de Memória: 45%")
        print("   Espaço em Disco: 78%")
        print("   Conexões Ativas: 8")
        print()
        print("0. Voltar")
        print()
    
    def create_new_attendant(self):
        """Cria novo atendente"""
        print("\n=== CRIAR NOVO ATENDENTE ===")
        print()
        
        try:
            username = input("Nome de usuário: ").strip()
            if not username:
                print("❌ Nome de usuário é obrigatório")
                return
            
            display_name = input("Nome para exibição: ").strip()
            if not display_name:
                display_name = username
            
            print("\nPapéis disponíveis:")
            roles = self.auth_manager.get_roles()
            for role_id, role_info in roles.items():
                print(f"   {role_id}: {role_info['description']}")
            
            role = input("Papel: ").strip()
            if role not in roles:
                print("❌ Papel inválido")
                return
            
            # Simular criação
            print(f"\n✅ Atendente {username} criado com sucesso!")
            print(f"   Nome: {display_name}")
            print(f"   Papel: {role}")
            print(f"   Senha padrão: quality123")
            print("   ⚠️  Lembre-se de alterar a senha no primeiro login")
            
        except KeyboardInterrupt:
            print("\n❌ Operação cancelada")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    def run(self):
        """Executa a interface administrativa"""
        try:
            # Login administrativo
            if not self.admin_login():
                return
            
            # Loop principal
            while True:
                try:
                    self.show_admin_dashboard()
                    self.show_admin_menu()
                    
                    choice = input("Escolha uma opção: ").strip()
                    
                    if choice == "0":
                        print("\n👋 Logout administrativo realizado!")
                        break
                    elif choice == "1":
                        self.handle_attendants_management()
                    elif choice == "2":
                        self.show_permissions_management()
                        input("\nPressione Enter para continuar...")
                    elif choice == "3":
                        self.show_reports_and_statistics()
                        input("\nPressione Enter para continuar...")
                    elif choice == "4":
                        self.show_system_settings()
                        input("\nPressione Enter para continuar...")
                    elif choice == "5":
                        self.show_system_logs()
                        input("\nPressione Enter para continuar...")
                    elif choice == "6":
                        self.show_alerts_monitoring()
                        input("\nPressione Enter para continuar...")
                    elif choice == "7":
                        self.show_backup_restore()
                        input("\nPressione Enter para continuar...")
                    elif choice == "8":
                        self.show_system_maintenance()
                        input("\nPressione Enter para continuar...")
                    else:
                        print("❌ Opção inválida")
                        time.sleep(1)
                        
                except KeyboardInterrupt:
                    print("\n\n👋 Sessão administrativa interrompida")
                    break
                except Exception as e:
                    print(f"\n❌ Erro: {e}")
                    time.sleep(2)
                    
        except Exception as e:
            print(f"\n❌ Erro fatal: {e}")
    
    def handle_attendants_management(self):
        """Gerencia menu de atendentes"""
        while True:
            try:
                self.show_attendants_management()
                choice = input("Escolha uma opção: ").strip().upper()
                
                if choice == "0":
                    break
                elif choice == "A":
                    self.create_new_attendant()
                    input("\nPressione Enter para continuar...")
                elif choice == "E":
                    print("\n🔧 Editar atendente - Funcionalidade em desenvolvimento")
                    input("\nPressione Enter para continuar...")
                elif choice == "D":
                    print("\n🔄 Desativar/Ativar atendente - Funcionalidade em desenvolvimento")
                    input("\nPressione Enter para continuar...")
                elif choice == "R":
                    print("\n🔐 Redefinir senha - Funcionalidade em desenvolvimento")
                    input("\nPressione Enter para continuar...")
                elif choice == "V":
                    print("\n👁️  Ver detalhes - Funcionalidade em desenvolvimento")
                    input("\nPressione Enter para continuar...")
                else:
                    print("❌ Opção inválida")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(2)

def main():
    """Função principal"""
    try:
        admin_cli = AdminCLI()
        admin_cli.run()
    except KeyboardInterrupt:
        print("\n👋 Interface administrativa encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()
