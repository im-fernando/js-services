#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Rápida - Cliente Atendente
Instalação simplificada para computadores dos atendentes
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de instalação"""
    print("=" * 60)
    print("👥 QUALITY CONTROL PANEL - INSTALAÇÃO RÁPIDA ATENDENTE")
    print("=" * 60)
    print("Instalação simplificada da interface de atendente")
    print("=" * 60)
    print()

def install_dependencies():
    """Instala dependências mínimas"""
    print("📦 Instalando dependências...")
    
    try:
        deps = [
            "websocket-client==1.6.4",
            "colorama==0.4.6"
        ]
        
        for dep in deps:
            print(f"   Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
        
        print("✅ Dependências instaladas")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_attendant_client():
    """Cria o cliente atendente"""
    print("\n📋 Criando cliente atendente...")
    
    try:
        # Diretório de instalação
        install_dir = Path("C:\\Quality\\AttendantClient")
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar arquivo principal do cliente
        client_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Atendente - Quality Control Panel
Interface simplificada para atendentes
"""

import sys
import os
import json
import time
import threading
from datetime import datetime

try:
    import websocket
    from colorama import init, Fore, Back, Style
    init()
except ImportError as e:
    print(f"❌ Dependência não encontrada: {e}")
    print("Execute: pip install websocket-client colorama")
    sys.exit(1)

class AttendantClient:
    def __init__(self, server_host="192.168.1.100", server_port=8765):
        self.server_host = server_host
        self.server_port = server_port
        self.ws = None
        self.connected = False
        self.session_id = None
        self.attendant_id = None
        
    def connect(self):
        """Conecta ao servidor"""
        try:
            url = f"ws://{self.server_host}:{self.server_port}"
            print(f"🔌 Conectando ao servidor: {url}")
            
            self.ws = websocket.WebSocketApp(
                url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Executar em thread separada
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
            # Aguardar conexão
            time.sleep(2)
            return self.connected
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def on_open(self, ws):
        """Callback de conexão aberta"""
        print("✅ Conectado ao servidor")
        self.connected = True
    
    def on_message(self, ws, message):
        """Callback de mensagem recebida"""
        try:
            data = json.loads(message)
            print(f"📨 Mensagem recebida: {data}")
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    def on_error(self, ws, error):
        """Callback de erro"""
        print(f"❌ Erro WebSocket: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Callback de conexão fechada"""
        print("🔌 Conexão fechada")
        self.connected = False
    
    def login(self, username, password):
        """Faz login no sistema"""
        if not self.connected:
            print("❌ Não conectado ao servidor")
            return False
        
        login_data = {
            "type": "login",
            "username": username,
            "password": password,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(login_data))
            print(f"🔐 Enviando login para: {username}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar login: {e}")
            return False
    
    def send_command(self, command, client_id=None):
        """Envia comando para o servidor"""
        if not self.connected:
            print("❌ Não conectado ao servidor")
            return False
        
        cmd_data = {
            "type": "command",
            "session_id": self.session_id,
            "attendant_id": self.attendant_id,
            "client_id": client_id,
            "command": command,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(cmd_data))
            print(f"📤 Comando enviado: {command}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar comando: {e}")
            return False

def main():
    """Função principal"""
    print("👥 QUALITY CONTROL PANEL - CLIENTE ATENDENTE")
    print("=" * 50)
    
    # Configuração do servidor
    server_host = input("IP do Servidor (padrão: 192.168.1.100): ").strip()
    if not server_host:
        server_host = "192.168.1.100"
    
    server_port = input("Porta do Servidor (padrão: 8765): ").strip()
    if not server_port:
        server_port = "8765"
    
    try:
        server_port = int(server_port)
    except ValueError:
        server_port = 8765
    
    # Criar cliente
    client = AttendantClient(server_host, server_port)
    
    # Conectar
    if not client.connect():
        print("❌ Falha ao conectar ao servidor")
        input("Pressione Enter para sair...")
        return
    
    # Login
    print("\\n🔐 LOGIN")
    username = input("Usuário: ").strip()
    password = input("Senha: ").strip()
    
    if not client.login(username, password):
        print("❌ Falha no login")
        input("Pressione Enter para sair...")
        return
    
    print("✅ Login realizado com sucesso!")
    
    # Menu principal
    while True:
        print("\\n📋 MENU PRINCIPAL")
        print("1. Listar clientes")
        print("2. Reiniciar serviço")
        print("3. Visualizar logs")
        print("4. Status do sistema")
        print("0. Sair")
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == "1":
            client.send_command("list_clients")
        elif choice == "2":
            client_id = input("ID do Cliente: ").strip()
            service = input("Nome do Serviço: ").strip()
            client.send_command(f"restart_service:{service}", client_id)
        elif choice == "3":
            client_id = input("ID do Cliente: ").strip()
            client.send_command("view_logs", client_id)
        elif choice == "4":
            client.send_command("system_status")
        elif choice == "0":
            break
        else:
            print("❌ Opção inválida")
    
    print("👋 Encerrando cliente...")
    if client.ws:
        client.ws.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Cliente encerrado pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
'''
        
        # Salvar arquivo do cliente
        client_file = install_dir / "attendant_client.py"
        with open(client_file, 'w', encoding='utf-8') as f:
            f.write(client_code)
        
        print(f"   ✅ Cliente criado: {client_file}")
        
        # Criar script de inicialização
        batch_content = f"""@echo off
echo Iniciando Quality Control Panel - Atendente...
cd /d "{install_dir}"
python attendant_client.py
pause
"""
        
        batch_file = install_dir / "start_attendant.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"   ✅ Script criado: {batch_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Instalar dependências
    if not install_dependencies():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar cliente
    if not create_attendant_client():
        input("\\nPressione Enter para sair...")
        return False
    
    print("\\n" + "=" * 60)
    print("🎉 INSTALAÇÃO RÁPIDA CONCLUÍDA!")
    print("=" * 60)
    print("📁 Diretório: C:\\Quality\\AttendantClient")
    print("🚀 Para usar: C:\\Quality\\AttendantClient\\start_attendant.bat")
    print()
    print("👤 USUÁRIOS PADRÃO:")
    print("   admin / admin123 (Administrador)")
    print("   joao.silva / quality123 (Suporte Sênior)")
    print("   maria.santos / quality123 (Suporte Júnior)")
    print("=" * 60)
    
    input("\\nPressione Enter para finalizar...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro inesperado: {e}")
        input("\\nPressione Enter para sair...")
