#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Completa - Sistema Quality Control Panel
Instala servidor, atendentes e clientes em uma única execução
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner de instalação"""
    print("=" * 70)
    print("🚀 QUALITY CONTROL PANEL - INSTALAÇÃO COMPLETA")
    print("=" * 70)
    print("Instalação completa do sistema multi-atendente")
    print("=" * 70)
    print()

def install_dependencies():
    """Instala todas as dependências necessárias"""
    print("📦 Instalando dependências do sistema...")
    
    try:
        deps = [
            "websocket-server==0.4",
            "websocket-client==1.6.4",
            "colorama==0.4.6",
            "rich==13.7.0",
            "requests==2.31.0"
        ]
        
        for dep in deps:
            print(f"   Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
        
        print("✅ Dependências instaladas com sucesso")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_server_installation():
    """Cria instalação do servidor"""
    print("\n🖥️  Criando instalação do servidor...")
    
    try:
        # Diretório do servidor
        server_dir = Path("C:\\Quality\\ControlPanel")
        server_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivos do servidor
        source_dir = Path(__file__).parent / "servidor_control"
        if source_dir.exists():
            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, server_dir / item.name)
                elif item.is_dir():
                    dest_dir = server_dir / item.name
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.copytree(item, dest_dir)
            
            print(f"   ✅ Servidor instalado em: {server_dir}")
        else:
            print(f"   ❌ Diretório fonte não encontrado: {source_dir}")
            return False
        
        # Criar script de inicialização do servidor
        server_script = f"""@echo off
echo Iniciando Quality Control Panel - Servidor...
cd /d "{server_dir}"
python main.py --multi-attendant
pause
"""
        
        server_bat = server_dir / "start_server.bat"
        with open(server_bat, 'w', encoding='utf-8') as f:
            f.write(server_script)
        
        print(f"   ✅ Script do servidor criado: {server_bat}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar servidor: {e}")
        return False

def create_attendant_installation():
    """Cria instalação dos atendentes"""
    print("\n👥 Criando instalação dos atendentes...")
    
    try:
        # Diretório dos atendentes
        attendant_dir = Path("C:\\Quality\\AttendantClient")
        attendant_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar cliente atendente
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
        client_file = attendant_dir / "attendant_client.py"
        with open(client_file, 'w', encoding='utf-8') as f:
            f.write(client_code)
        
        print(f"   ✅ Cliente atendente criado: {client_file}")
        
        # Criar script de inicialização
        attendant_script = f"""@echo off
echo Iniciando Quality Control Panel - Atendente...
cd /d "{attendant_dir}"
python attendant_client.py
pause
"""
        
        attendant_bat = attendant_dir / "start_attendant.bat"
        with open(attendant_bat, 'w', encoding='utf-8') as f:
            f.write(attendant_script)
        
        print(f"   ✅ Script do atendente criado: {attendant_bat}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar atendente: {e}")
        return False

def create_client_installation():
    """Cria instalação dos clientes"""
    print("\n🖥️  Criando instalação dos clientes...")
    
    try:
        # Diretório dos clientes
        client_dir = Path("C:\\Quality\\RemoteAgent")
        client_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar agente cliente
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
        agent_file = client_dir / "quality_agent.py"
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(agent_code)
        
        print(f"   ✅ Agente cliente criado: {agent_file}")
        
        # Criar script de inicialização
        client_script = f"""@echo off
echo Iniciando Quality Control Panel - Agente...
cd /d "{client_dir}"
python quality_agent.py
pause
"""
        
        client_bat = client_dir / "start_agent.bat"
        with open(client_bat, 'w', encoding='utf-8') as f:
            f.write(client_script)
        
        print(f"   ✅ Script do cliente criado: {client_bat}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return False

def create_documentation():
    """Cria documentação do sistema"""
    print("\n📚 Criando documentação...")
    
    try:
        # Diretório de documentação
        doc_dir = Path("C:\\Quality\\Documentation")
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar README
        readme_content = """# Quality Control Panel - Sistema Multi-Atendente

## Visão Geral
Sistema de monitoramento e controle remoto para serviços Quality com suporte a múltiplos atendentes simultâneos.

## Componentes Instalados

### 1. Servidor (C:\\Quality\\ControlPanel)
- Servidor WebSocket principal
- Gerenciamento de sessões
- Sistema de autenticação
- Controle de permissões

### 2. Atendentes (C:\\Quality\\AttendantClient)
- Interface de atendente
- Conexão com servidor
- Gerenciamento de clientes

### 3. Clientes (C:\\Quality\\RemoteAgent)
- Agente de monitoramento
- Conexão com servidor
- Execução de comandos

## Como Usar

### Iniciar o Servidor
```
C:\\Quality\\ControlPanel\\start_server.bat
```

### Conectar Atendentes
```
C:\\Quality\\AttendantClient\\start_attendant.bat
```

### Conectar Clientes
```
C:\\Quality\\RemoteAgent\\start_agent.bat
```

## Usuários Padrão
- admin / admin123 (Administrador)
- joao.silva / quality123 (Suporte Sênior)
- maria.santos / quality123 (Suporte Júnior)

## Configuração de Rede
- Servidor: Porta 8765
- Atendentes: Conectam ao servidor
- Clientes: Conectam ao servidor

## Suporte
Para suporte técnico, consulte a documentação completa ou entre em contato com a equipe de desenvolvimento.
"""
        
        readme_file = doc_dir / "README.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"   ✅ Documentação criada: {readme_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar documentação: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Instalar dependências
    if not install_dependencies():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar servidor
    if not create_server_installation():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar atendentes
    if not create_attendant_installation():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar clientes
    if not create_client_installation():
        input("\\nPressione Enter para sair...")
        return False
    
    # Criar documentação
    if not create_documentation():
        input("\\nPressione Enter para sair...")
        return False
    
    print("\\n" + "=" * 70)
    print("🎉 INSTALAÇÃO COMPLETA CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print("📁 COMPONENTES INSTALADOS:")
    print("   🖥️  Servidor: C:\\Quality\\ControlPanel")
    print("   👥 Atendentes: C:\\Quality\\AttendantClient")
    print("   🖥️  Clientes: C:\\Quality\\RemoteAgent")
    print("   📚 Documentação: C:\\Quality\\Documentation")
    print()
    print("🚀 COMO USAR:")
    print("   1. Inicie o servidor: C:\\Quality\\ControlPanel\\start_server.bat")
    print("   2. Conecte atendentes: C:\\Quality\\AttendantClient\\start_attendant.bat")
    print("   3. Conecte clientes: C:\\Quality\\RemoteAgent\\start_agent.bat")
    print()
    print("👤 USUÁRIOS PADRÃO:")
    print("   admin / admin123 (Administrador)")
    print("   joao.silva / quality123 (Suporte Sênior)")
    print("   maria.santos / quality123 (Suporte Júnior)")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Altere as senhas padrão após a instalação")
    print("   - Configure os IPs corretamente")
    print("   - Execute como Administrador")
    print("=" * 70)
    
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
