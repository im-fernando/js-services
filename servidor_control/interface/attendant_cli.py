#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface CLI para Atendentes
Interface específica para cada atendente conectado
"""

import sys
import os
import time
import getpass
from typing import Dict, Any, List, Optional
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(str(os.path.dirname(os.path.dirname(__file__))))

from utils.helpers import format_timestamp, get_status_emoji, get_critical_emoji, truncate_string
from utils.auth import QualityAuthManager

class AttendantCLI:
    """Interface CLI para atendentes"""
    
    def __init__(self, server_host: str = "localhost", server_port: int = 8765):
        self.server_host = server_host
        self.server_port = server_port
        self.auth_manager = QualityAuthManager()
        
        # Estado da sessão
        self.current_attendant = None
        self.session_id = None
        self.current_client = None
        self.connected = False
        
        # Dados em cache
        self.clients_cache = []
        self.services_cache = {}
        
    def print_banner(self):
        """Exibe banner de login"""
        print("=" * 70)
        print("🎯 QUALITY REMOTE CONTROL PANEL")
        print("=== LOGIN DE ATENDENTE ===")
        print("=" * 70)
        print()
    
    def login(self) -> bool:
        """Realiza login do atendente"""
        self.print_banner()
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                print(f"Tentativa {attempts + 1} de {max_attempts}")
                print("-" * 40)
                
                username = input("Usuário: ").strip()
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
                
                if success:
                    self.current_attendant = user_data
                    print(f"\n🟢 {message}")
                    print(f"Bem-vindo, {user_data['display_name']} ({user_data['role']})")
                    return True
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
    
    def show_dashboard(self):
        """Exibe dashboard do atendente"""
        if not self.current_attendant:
            return
        
        print("\n" + "=" * 70)
        print(f"📊 DASHBOARD - {self.current_attendant['display_name']}")
        print("=" * 70)
        print(f"🕐 {datetime.now().strftime('%H:%M:%S')} | Sessão: {self.session_id or 'N/A'}")
        print()
        
        # Informações do atendente
        print("👤 INFORMAÇÕES DO ATENDENTE:")
        print(f"   Nome: {self.current_attendant['display_name']}")
        print(f"   Papel: {self.current_attendant['role']}")
        print(f"   Clientes designados: {len(self.current_attendant.get('assigned_clients', []))}")
        print()
        
        # Estatísticas (simuladas)
        print("📊 ESTATÍSTICAS DA SESSÃO:")
        print("   Comandos executados: 0")
        print("   Clientes atendidos: 0")
        print("   Tempo de sessão: 0 min")
        print()
        
        # Clientes disponíveis (simulados)
        print("🖥️  CLIENTES DISPONÍVEIS:")
        print("   ✅ Posto Quality Matriz      [🟢 Online] [Livre]")
        print("   ✅ Posto Quality Filial 01   [🟢 Online] [Livre]")
        print("   ✅ Posto Quality Filial 02   [🟡 Instável] [Livre]")
        print("   🔒 Posto Quality ABC         [🟢 Online] [Maria Santos - Logs]")
        print("   🔒 Posto Quality XYZ         [🟢 Online] [Pedro Costa - Serviços]")
        print()
    
    def show_main_menu(self):
        """Exibe menu principal"""
        print("=== MENU PRINCIPAL ===")
        print("1. 🖥️  Gerenciar Clientes Disponíveis")
        print("2. 👥 Ver Atividade de Outros Atendentes")
        print("3. 📊 Dashboard Consolidado")
        print("4. ⚙️  Configurações da Sessão")
        print("5. 📋 Histórico de Atividades")
        print("6. 💬 Chat Interno")
        print("0. Logout")
        print()
    
    def show_clients_menu(self):
        """Exibe menu de clientes"""
        print("\n=== CLIENTES QUALITY DISPONÍVEIS ===")
        print()
        print("✅ DISPONÍVEIS:")
        print("1. 🏪 Posto Quality Matriz      [🟢 Online] [Livre]")
        print("2. 🏪 Posto Quality Filial 01   [🟢 Online] [Livre]")
        print("3. 🏪 Posto Quality Filial 02   [🟡 Instável] [Livre]")
        print("4. 🏪 Posto Quality Filial 03   [🟢 Online] [Livre]")
        print()
        print("🔒 EM USO POR OUTROS ATENDENTES:")
        print("5. 🏪 Posto Quality ABC         [🟢 Online] [Maria Santos - Logs]")
        print("6. 🏪 Posto Quality XYZ         [🟢 Online] [Pedro Costa - Serviços]")
        print()
        print("❌ OFFLINE:")
        print("7. 🏪 Posto Quality DEF         [🔴 Offline] [Última atividade: 12:30]")
        print("8. 🏪 Posto Quality GHI         [🔴 Offline] [Última atividade: Ontem]")
        print()
        print("Selecione um cliente disponível (1-4) ou 0 para voltar:")
    
    def show_client_management_menu(self, client_name: str):
        """Exibe menu de gerenciamento de cliente"""
        print(f"\n=== CLIENTE: {client_name} ===")
        print("Status: 🟢 Conectado | Última atividade: 14:30:52")
        print()
        print("1. 🔧 Gerenciar Serviços Quality")
        print("2. 📊 Monitorar Processos")
        print("3. 📋 Visualizar Logs")
        print("4. ⚡ Ações Rápidas")
        print("5. 📈 Status Consolidado")
        print("0. Voltar ao Menu Principal")
        print()
    
    def show_services_menu(self, client_name: str):
        """Exibe menu de serviços"""
        print(f"\n=== SERVIÇOS QUALITY - {client_name} ===")
        print()
        print("1. 🌐 IntegraWebService          [🟢 Executando]")
        print("2. 💰 webPostoFiscalService      [🟢 Executando]")
        print("3. 🤖 webPostoLeituraAutomacao   [🔴 Parado]")
        print("4. 💳 webPostoPayServer          [🟢 Executando]")
        print("5. ⚡ QualityPulserWeb           [🟡 Instável]")
        print()
        print("Ações:")
        print("R. Reiniciar Todos os Serviços")
        print("S. Parar Todos os Serviços")
        print("I. Iniciar Todos os Serviços")
        print("0. Voltar")
        print()
    
    def show_logs_menu(self, client_name: str):
        """Exibe menu de logs"""
        print(f"\n=== VISUALIZAÇÃO DE LOGS - {client_name} ===")
        print("Selecione o serviço para monitorar logs:")
        print()
        print("1. 📋 Integra (IntegraWebService)")
        print("2. 📋 Fiscal (webPostoFiscalService)")
        print("3. 📋 Automação (webPostoLeituraAutomacao)")
        print("4. 📋 Pagamento (webPostoPayServer)")
        print("5. 📋 Pulser (QualityPulserWeb)")
        print()
        print("Opções:")
        print("T. Monitorar Todos (Multiplexado)")
        print("F. Filtrar por Palavra-chave")
        print("L. Últimas 100 linhas")
        print("0. Voltar")
        print()
    
    def show_other_attendants_activity(self):
        """Exibe atividade de outros atendentes"""
        print("\n=== ATIVIDADE DE OUTROS ATENDENTES ===")
        print()
        print("👥 ATENDENTES ATIVOS:")
        print("   Maria Santos (Suporte Júnior) - 13:20")
        print("     → Posto ABC [Visualizando logs do ServicoFiscal]")
        print("     → Comandos executados: 3")
        print()
        print("   Pedro Costa (Suporte Sênior) - 15:10")
        print("     → Posto XYZ [Reiniciando serviços]")
        print("     → Comandos executados: 7")
        print()
        print("   Ana Lima (Administrador) - 16:45")
        print("     → Dashboard [Monitorando sistema]")
        print("     → Comandos executados: 12")
        print()
        print("📊 ESTATÍSTICAS GERAIS:")
        print("   Total de atendentes: 4")
        print("   Sessões ativas: 4")
        print("   Comandos executados hoje: 47")
        print("   Clientes atendidos: 12")
        print()
    
    def show_consolidated_dashboard(self):
        """Exibe dashboard consolidado"""
        print("\n=== DASHBOARD CONSOLIDADO ===")
        print()
        print("📊 VISÃO GERAL DO SISTEMA:")
        print("   Clientes Conectados: 8/12")
        print("   Atendentes Ativos: 4")
        print("   Serviços Críticos: 3/5 com problemas")
        print("   Uptime Médio: 98.5%")
        print()
        print("🚨 ALERTAS CRÍTICOS:")
        print("   ⚠️  Posto DEF offline há 2 horas")
        print("   ⚠️  Muitos reinicializações no Posto GHI (5x hoje)")
        print("   ⚠️  ServicoFiscal instável em 3 postos")
        print()
        print("📈 MÉTRICAS DE HOJE:")
        print("   Comandos executados: 127")
        print("   Reinicializações: 23")
        print("   Tempo médio de atendimento: 8.5 min")
        print("   Satisfação: 4.8/5.0")
        print()
    
    def show_session_settings(self):
        """Exibe configurações da sessão"""
        print("\n=== CONFIGURAÇÕES DA SESSÃO ===")
        print()
        print("👤 INFORMAÇÕES PESSOAIS:")
        print(f"   Nome: {self.current_attendant['display_name']}")
        print(f"   Usuário: {self.current_attendant['username']}")
        print(f"   Papel: {self.current_attendant['role']}")
        print(f"   Sessão: {self.session_id or 'N/A'}")
        print()
        print("🔐 PERMISSÕES:")
        permissions = self.current_attendant.get('permissions', {})
        for perm, value in permissions.items():
            status = "✅" if value else "❌"
            perm_name = perm.replace('can_', '').replace('_', ' ').title()
            print(f"   {status} {perm_name}")
        print()
        print("⚙️  OPÇÕES:")
        print("1. Alterar Senha")
        print("2. Ver Histórico de Sessões")
        print("3. Configurar Notificações")
        print("0. Voltar")
        print()
    
    def show_activity_history(self):
        """Exibe histórico de atividades"""
        print("\n=== HISTÓRICO DE ATIVIDADES ===")
        print()
        print("📋 ATIVIDADES RECENTES:")
        print("   14:35 - Reiniciou ServicoFiscal no Posto ABC")
        print("   14:30 - Visualizou logs do IntegraWebService")
        print("   14:25 - Conectou ao Posto ABC")
        print("   14:20 - Login realizado")
        print()
        print("📊 ESTATÍSTICAS DA SESSÃO:")
        print("   Comandos executados: 3")
        print("   Clientes atendidos: 1")
        print("   Tempo de sessão: 15 min")
        print("   Ações mais frequentes: Visualizar logs (2x)")
        print()
    
    def show_chat_interface(self):
        """Exibe interface de chat interno"""
        print("\n=== CHAT INTERNO ===")
        print()
        print("💬 MENSAGENS RECENTES:")
        print("   [14:35] João Silva: Alguém sabe se o Posto ABC teve problemas hoje?")
        print("   [14:36] Maria Santos: Sim, reiniciei o ServicoFiscal há 10 min")
        print("   [14:37] Pedro Costa: Tudo funcionando normal agora")
        print("   [14:38] Ana Lima: Vou verificar os logs do sistema")
        print()
        print("Digite sua mensagem (ou 'sair' para voltar):")
    
    def simulate_log_monitoring(self, service_name: str):
        """Simula monitoramento de logs"""
        print(f"\n📋 MONITORAMENTO DE LOGS - {service_name}")
        print("=" * 50)
        print("Simulando streaming de logs em tempo real...")
        print("Pressione Ctrl+C para parar")
        print()
        
        log_entries = [
            f"[14:35:22] {service_name}: INFO - Conexão estabelecida com servidor",
            f"[14:35:23] {service_name}: DEBUG - Processando requisição de integração",
            f"[14:35:24] {service_name}: INFO - Dados sincronizados com sucesso",
            f"[14:35:25] {service_name}: WARNING - Timeout na conexão com banco",
            f"[14:35:26] {service_name}: ERROR - Falha ao processar transação"
        ]
        
        try:
            for i, entry in enumerate(log_entries):
                print(entry)
                time.sleep(1)
                
                if i >= 4:  # Limitar para demonstração
                    break
                    
        except KeyboardInterrupt:
            print("\n\n📋 Monitoramento de logs interrompido")
    
    def run(self):
        """Executa a interface principal"""
        try:
            # Login
            if not self.login():
                return
            
            # Simular criação de sessão
            self.session_id = f"SES_{self.current_attendant['id']}_{int(time.time())}"
            
            # Loop principal
            while True:
                try:
                    self.show_dashboard()
                    self.show_main_menu()
                    
                    choice = input("Escolha uma opção: ").strip()
                    
                    if choice == "0":
                        print("\n👋 Logout realizado com sucesso!")
                        break
                    elif choice == "1":
                        self.handle_clients_menu()
                    elif choice == "2":
                        self.show_other_attendants_activity()
                        input("\nPressione Enter para continuar...")
                    elif choice == "3":
                        self.show_consolidated_dashboard()
                        input("\nPressione Enter para continuar...")
                    elif choice == "4":
                        self.show_session_settings()
                        input("\nPressione Enter para continuar...")
                    elif choice == "5":
                        self.show_activity_history()
                        input("\nPressione Enter para continuar...")
                    elif choice == "6":
                        self.show_chat_interface()
                        input("\nPressione Enter para continuar...")
                    else:
                        print("❌ Opção inválida")
                        time.sleep(1)
                        
                except KeyboardInterrupt:
                    print("\n\n👋 Sessão interrompida pelo usuário")
                    break
                except Exception as e:
                    print(f"\n❌ Erro: {e}")
                    time.sleep(2)
                    
        except Exception as e:
            print(f"\n❌ Erro fatal: {e}")
    
    def handle_clients_menu(self):
        """Gerencia menu de clientes"""
        while True:
            try:
                self.show_clients_menu()
                choice = input("Escolha uma opção: ").strip()
                
                if choice == "0":
                    break
                elif choice in ["1", "2", "3", "4"]:
                    client_names = {
                        "1": "Posto Quality Matriz",
                        "2": "Posto Quality Filial 01", 
                        "3": "Posto Quality Filial 02",
                        "4": "Posto Quality Filial 03"
                    }
                    
                    client_name = client_names[choice]
                    self.current_client = client_name
                    self.handle_client_management(client_name)
                else:
                    print("❌ Opção inválida")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(2)
    
    def handle_client_management(self, client_name: str):
        """Gerencia menu de cliente específico"""
        while True:
            try:
                self.show_client_management_menu(client_name)
                choice = input("Escolha uma opção: ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    self.handle_services_menu(client_name)
                elif choice == "2":
                    print(f"\n📊 Processos do {client_name}:")
                    print("   IntegraWebService.exe (PID: 1234) - 45.2 MB")
                    print("   webPostoFiscalServer.exe (PID: 5678) - 32.1 MB")
                    input("\nPressione Enter para continuar...")
                elif choice == "3":
                    self.handle_logs_menu(client_name)
                elif choice == "4":
                    print(f"\n⚡ Ações rápidas para {client_name}:")
                    print("   ✅ Reiniciar todos os serviços")
                    print("   ✅ Verificar status")
                    print("   ✅ Limpar logs antigos")
                    input("\nPressione Enter para continuar...")
                elif choice == "5":
                    print(f"\n📈 Status consolidado do {client_name}:")
                    print("   🟢 4/5 serviços funcionando")
                    print("   📊 Uptime: 98.5%")
                    print("   💾 Memória: 2.1 GB")
                    input("\nPressione Enter para continuar...")
                else:
                    print("❌ Opção inválida")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(2)
    
    def handle_services_menu(self, client_name: str):
        """Gerencia menu de serviços"""
        while True:
            try:
                self.show_services_menu(client_name)
                choice = input("Escolha uma opção: ").strip().upper()
                
                if choice == "0":
                    break
                elif choice in ["1", "2", "3", "4", "5"]:
                    service_names = {
                        "1": "IntegraWebService",
                        "2": "webPostoFiscalService",
                        "3": "webPostoLeituraAutomacao", 
                        "4": "webPostoPayServer",
                        "5": "QualityPulserWeb"
                    }
                    
                    service_name = service_names[choice]
                    print(f"\n🔧 Gerenciando {service_name}...")
                    print("   ✅ Serviço reiniciado com sucesso")
                    input("\nPressione Enter para continuar...")
                elif choice == "R":
                    print(f"\n🔄 Reiniciando todos os serviços do {client_name}...")
                    print("   ✅ Todos os serviços reiniciados com sucesso")
                    input("\nPressione Enter para continuar...")
                elif choice == "S":
                    print(f"\n🛑 Parando todos os serviços do {client_name}...")
                    print("   ✅ Todos os serviços parados com sucesso")
                    input("\nPressione Enter para continuar...")
                elif choice == "I":
                    print(f"\n🚀 Iniciando todos os serviços do {client_name}...")
                    print("   ✅ Todos os serviços iniciados com sucesso")
                    input("\nPressione Enter para continuar...")
                else:
                    print("❌ Opção inválida")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(2)
    
    def handle_logs_menu(self, client_name: str):
        """Gerencia menu de logs"""
        while True:
            try:
                self.show_logs_menu(client_name)
                choice = input("Escolha uma opção: ").strip().upper()
                
                if choice == "0":
                    break
                elif choice in ["1", "2", "3", "4", "5"]:
                    service_names = {
                        "1": "IntegraWebService",
                        "2": "webPostoFiscalService",
                        "3": "webPostoLeituraAutomacao",
                        "4": "webPostoPayServer", 
                        "5": "QualityPulserWeb"
                    }
                    
                    service_name = service_names[choice]
                    self.simulate_log_monitoring(service_name)
                elif choice == "T":
                    print(f"\n📋 Monitorando todos os logs do {client_name}...")
                    self.simulate_log_monitoring("Todos os Serviços")
                elif choice == "F":
                    keyword = input("Digite a palavra-chave para filtrar: ").strip()
                    print(f"\n🔍 Filtrando logs por: '{keyword}'")
                    self.simulate_log_monitoring(f"Filtrado por '{keyword}'")
                elif choice == "L":
                    print(f"\n📋 Últimas 100 linhas de logs do {client_name}:")
                    self.simulate_log_monitoring("Últimas 100 linhas")
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
    import argparse
    
    parser = argparse.ArgumentParser(description='Quality Control Panel - Interface de Atendente')
    parser.add_argument('--server', default='localhost:8765',
                       help='Servidor (host:port)')
    parser.add_argument('--host', default='localhost',
                       help='Host do servidor')
    parser.add_argument('--port', type=int, default=8765,
                       help='Porta do servidor')
    
    args = parser.parse_args()
    
    # Extrair host e porta
    if ':' in args.server:
        host, port = args.server.split(':')
        port = int(port)
    else:
        host = args.host
        port = args.port
    
    try:
        cli = AttendantCLI(host, port)
        cli.run()
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()
