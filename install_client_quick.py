#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Rápida - Cliente Quality
Instalação simplificada para computadores dos clientes
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de instalação"""
    print("=" * 60)
    print("🖥️  QUALITY CONTROL PANEL - INSTALAÇÃO RÁPIDA CLIENTE")
    print("=" * 60)
    print("Instalação simplificada do agente Quality")
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

def create_quality_agent():
    """Cria o agente Quality"""
    print("\n📋 Criando agente Quality...")
    
    try:
        # Diretório de instalação
        install_dir = Path("C:\\Quality\\RemoteAgent")
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar arquivo principal do agente
        agent_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente Quality - Quality Control Panel
Agente para monitoramento e controle remoto
"""

import sys
import os
import json
import time
import threading
import subprocess
from datetime import datetime

try:
    import websocket
    from colorama import init, Fore, Back, Style
    init()
except ImportError as e:
    print(f"❌ Dependência não encontrada: {e}")
    print("Execute: pip install websocket-client colorama")
    sys.exit(1)

class QualityAgent:
    def __init__(self, server_host="192.168.1.100", server_port=8765, client_id="QUALITY_CLIENTE_001"):
        self.server_host = server_host
        self.server_port = server_port
        self.client_id = client_id
        self.ws = None
        self.connected = False
        self.heartbeat_interval = 30  # segundos
        
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
        
        # Enviar identificação
        self.send_identification()
        
        # Iniciar heartbeat
        self.start_heartbeat()
    
    def on_message(self, ws, message):
        """Callback de mensagem recebida"""
        try:
            data = json.loads(message)
            print(f"📨 Mensagem recebida: {data}")
            
            # Processar comando
            if data.get("type") == "command":
                self.process_command(data)
                
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    def on_error(self, ws, error):
        """Callback de erro"""
        print(f"❌ Erro WebSocket: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Callback de conexão fechada"""
        print("🔌 Conexão fechada")
        self.connected = False
    
    def send_identification(self):
        """Envia identificação do cliente"""
        if not self.connected:
            return
        
        identification = {
            "type": "client_identification",
            "client_id": self.client_id,
            "client_name": f"Cliente {self.client_id}",
            "client_location": "Local",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(identification))
            print(f"🆔 Identificação enviada: {self.client_id}")
        except Exception as e:
            print(f"❌ Erro ao enviar identificação: {e}")
    
    def start_heartbeat(self):
        """Inicia heartbeat para manter conexão"""
        def heartbeat():
            while self.connected:
                time.sleep(self.heartbeat_interval)
                if self.connected:
                    self.send_heartbeat()
        
        heartbeat_thread = threading.Thread(target=heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
    
    def send_heartbeat(self):
        """Envia heartbeat"""
        if not self.connected:
            return
        
        heartbeat_data = {
            "type": "heartbeat",
            "client_id": self.client_id,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(heartbeat_data))
            print("💓 Heartbeat enviado")
        except Exception as e:
            print(f"❌ Erro ao enviar heartbeat: {e}")
    
    def process_command(self, command_data):
        """Processa comando recebido"""
        command = command_data.get("command", "")
        print(f"🔧 Processando comando: {command}")
        
        try:
            if command == "get_status":
                self.send_status()
            elif command == "restart_service":
                service_name = command_data.get("service_name", "")
                self.restart_service(service_name)
            elif command == "get_logs":
                self.send_logs()
            else:
                print(f"❌ Comando não reconhecido: {command}")
                
        except Exception as e:
            print(f"❌ Erro ao processar comando: {e}")
    
    def send_status(self):
        """Envia status do sistema"""
        if not self.connected:
            return
        
        status = {
            "type": "status_response",
            "client_id": self.client_id,
            "status": "online",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(status))
            print("📊 Status enviado")
        except Exception as e:
            print(f"❌ Erro ao enviar status: {e}")
    
    def restart_service(self, service_name):
        """Reinicia serviço"""
        if not service_name:
            print("❌ Nome do serviço não especificado")
            return
        
        try:
            # Comando para reiniciar serviço Windows
            result = subprocess.run([
                "net", "stop", service_name
            ], capture_output=True, text=True)
            
            time.sleep(2)
            
            result = subprocess.run([
                "net", "start", service_name
            ], capture_output=True, text=True)
            
            print(f"🔄 Serviço {service_name} reiniciado")
            
            # Enviar resposta
            response = {
                "type": "command_response",
                "client_id": self.client_id,
                "command": "restart_service",
                "service_name": service_name,
                "result": "success",
                "timestamp": datetime.now().isoformat()
            }
            
            if self.connected:
                self.ws.send(json.dumps(response))
                
        except Exception as e:
            print(f"❌ Erro ao reiniciar serviço: {e}")
    
    def send_logs(self):
        """Envia logs do sistema"""
        if not self.connected:
            return
        
        # Simular logs (em implementação real, ler arquivos de log)
        logs = {
            "type": "logs_response",
            "client_id": self.client_id,
            "logs": [
                f"[{datetime.now().strftime('%H:%M:%S')}] Sistema funcionando normalmente",
                f"[{datetime.now().strftime('%H:%M:%S')}] Agente conectado ao servidor"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.ws.send(json.dumps(logs))
            print("📋 Logs enviados")
        except Exception as e:
            print(f"❌ Erro ao enviar logs: {e}")

def main():
    """Função principal"""
    print("🖥️  QUALITY CONTROL PANEL - AGENTE QUALITY")
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
    
    # ID do cliente
    client_id = input("ID do Cliente (ex: QUALITY_CLIENTE_001): ").strip()
    if not client_id:
        client_id = "QUALITY_CLIENTE_001"
    
    # Criar agente
    agent = QualityAgent(server_host, server_port, client_id)
    
    # Conectar
    if not agent.connect():
        print("❌ Falha ao conectar ao servidor")
        input("Pressione Enter para sair...")
        return
    
    print("✅ Agente conectado e funcionando!")
    print("💡 Pressione Ctrl+C para encerrar")
    
    try:
        # Manter agente rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n👋 Agente encerrado pelo usuário")
    
    if agent.ws:
        agent.ws.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Agente encerrado pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
'''
        
        # Salvar arquivo do agente
        agent_file = install_dir / "quality_agent.py"
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(agent_code)
        
        print(f"   ✅ Agente criado: {agent_file}")
        
        # Criar script de inicialização
        batch_content = f"""@echo off
echo Iniciando Quality Control Panel - Agente...
cd /d "{install_dir}"
python quality_agent.py
pause
"""
        
        batch_file = install_dir / "start_agent.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"   ✅ Script criado: {batch_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Instalar dependências
    if not install_dependencies():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar agente
    if not create_quality_agent():
        input("\\nPressione Enter para sair...")
        return False
    
    print("\\n" + "=" * 60)
    print("🎉 INSTALAÇÃO RÁPIDA CONCLUÍDA!")
    print("=" * 60)
    print("📁 Diretório: C:\\Quality\\RemoteAgent")
    print("🚀 Para usar: C:\\Quality\\RemoteAgent\\start_agent.bat")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Configure o IP do servidor corretamente")
    print("   - Use um ID único para cada cliente")
    print("   - Execute como Administrador")
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
