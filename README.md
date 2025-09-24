# Quality Remote Control System

Sistema distribuído para monitoramento e controle remoto de serviços Quality, composto por um agente cliente e um painel de controle servidor.

## 🏗️ Arquitetura

### Componente Cliente (Agent)
- **Localização**: `cliente_agent/`
- **Função**: Aplicação que roda em segundo plano nos computadores dos clientes
- **Responsabilidades**:
  - Monitoramento dos 5 serviços Quality específicos
  - Gerenciamento de processos
  - Streaming de logs em tempo real
  - Comunicação com o servidor de controle

### Componente Servidor (Control Panel)
- **Localização**: `servidor_control/`
- **Função**: Interface para atendentes gerenciarem os clientes remotamente
- **Responsabilidades**:
  - Gerenciamento de clientes conectados
  - Interface CLI interativa
  - Execução de comandos remotos
  - Dashboard de status consolidado

## 🚀 Instalação

### 1. Instalação do Cliente (Agent)

Execute o script de instalação interativo:

```bash
python install_quality_agent.py
```

O script irá:
- ✅ Verificar a instalação do Python (3.7+)
- 🔍 Detectar serviços Quality instalados
- ⚙️ Configurar o cliente (ID, nome, servidor)
- 📦 Instalar dependências Python
- 📁 Criar estrutura de arquivos
- 🧪 Testar a instalação

### 2. Instalação do Servidor (Control Panel)

```bash
cd servidor_control
pip install -r requirements.txt
python main.py --quality-mode
```

## 🔧 Configuração

### Serviços Quality Monitorados

O sistema monitora os seguintes serviços:

1. **🌐 IntegraWebService** (`srvIntegraWeb`)
   - Caminho: `C:\Quality\web\IntegraWebService.exe`
   - Logs: `C:\Quality\LOG\Integra`

2. **💰 webPostoFiscalService** (`ServicoFiscal`)
   - Caminho: `C:\Quality\Services\webPostoPayServer\webPostoFiscalServer.exe`
   - Logs: `C:\Quality\LOG\webPostoFiscalServer`

3. **🤖 webPostoLeituraAutomacao** (`ServicoAutomacao`)
   - Caminho: `C:\Quality\Services\webPostoLeituraAutomacao\webPostoLeituraAutomacao.exe`
   - Logs: `C:\Quality\LOG\webPostoLeituraAutomacao`

4. **💳 webPostoPayServer** (`webPostoPayServer`)
   - Caminho: `C:\Quality\Services\webPostoPayServer\winSW\webPostoPaySW.exe`
   - Logs: `C:\Quality\LOG\QualityPDV_PAF`

5. **⚡ QualityPulserWeb** (`QualityPulser`)
   - Caminho: `C:\Quality\PulserWeb.exe`
   - Logs: `C:\Quality\LOG\WebPostoPulser`

### Dependências entre Serviços

```json
{
    "ServicoFiscal": ["srvIntegraWeb"],
    "ServicoAutomacao": ["srvIntegraWeb", "ServicoFiscal"],
    "webPostoPayServer": ["ServicoFiscal"],
    "QualityPulser": ["srvIntegraWeb"]
}
```

## 🎮 Uso

### Iniciar o Agente Cliente

```bash
# Windows
C:\Quality\RemoteAgent\start_agent.bat

# Ou diretamente
cd C:\Quality\RemoteAgent
python main.py
```

### Iniciar o Servidor de Controle

```bash
cd servidor_control
python main.py --quality-mode --port 8765
```

### Interface do Servidor

```
=== QUALITY REMOTE CONTROL PANEL ===
1. Listar Clientes Conectados
2. Selecionar Cliente para Gerenciar
3. Dashboard Consolidado
4. Histórico de Atividades
5. Configurações
0. Sair
```

## 📋 Funcionalidades

### Monitoramento de Serviços
- ✅ Status em tempo real dos 5 serviços Quality
- 🔄 Iniciar/parar/reiniciar serviços individuais
- 📊 Informações de uso de recursos (CPU, memória)
- ⏱️ Tempo de execução (uptime)
- 🚨 Detecção automática de falhas

### Gerenciamento de Processos
- 📋 Lista de processos Quality em execução
- 🛑 Finalização de processos por PID
- 📈 Monitoramento de recursos por processo
- 🔍 Processos órfãos (Quality não associados a serviços)

### Monitor de Logs Inteligente
- 🗂️ Navegação automática na estrutura de pastas aninhadas
- 📄 Identificação do arquivo de log mais recente
- 📺 Streaming de logs em tempo real (estilo BareTail)
- 🔍 Filtros por nível de log e palavras-chave
- 📊 Monitoramento multiplexado de múltiplos serviços

### Comunicação
- 🌐 Conexão WebSocket persistente
- 🔄 Reconexão automática em caso de falha
- 💓 Sistema de heartbeat para verificação de conectividade
- 🆔 Identificação única de clientes

## 🛠️ Comandos Disponíveis

### Comandos de Serviços
- `get_quality_services_status` - Status de todos os serviços
- `start_service` - Iniciar serviço específico
- `stop_service` - Parar serviço específico
- `restart_service` - Reiniciar serviço específico
- `restart_all_services` - Reiniciar todos os serviços

### Comandos de Processos
- `get_processes` - Listar processos Quality
- `kill_process` - Finalizar processo por PID

### Comandos de Logs
- `get_logs` - Obter logs de um serviço
- `start_log_monitoring` - Iniciar monitoramento em tempo real
- `stop_log_monitoring` - Parar monitoramento

### Comandos de Sistema
- `get_system_info` - Informações do sistema cliente

## 📁 Estrutura de Arquivos

```
js-services/
├── cliente_agent/                 # Agente Cliente
│   ├── main.py                   # Ponto de entrada
│   ├── config/
│   │   ├── settings.py           # Configurações
│   │   └── services_config.json  # Configuração dos serviços
│   ├── core/
│   │   ├── agent.py              # Classe principal do agente
│   │   ├── service_manager.py    # Gerenciamento de serviços
│   │   ├── process_manager.py    # Gerenciamento de processos
│   │   ├── log_monitor.py        # Monitor de logs
│   │   └── network_client.py     # Comunicação WebSocket
│   ├── utils/
│   │   ├── logger.py             # Sistema de logging
│   │   ├── log_finder.py         # Localização de logs
│   │   └── helpers.py            # Funções auxiliares
│   └── requirements.txt          # Dependências
├── servidor_control/              # Painel de Controle
│   ├── main.py                   # Ponto de entrada do servidor
│   ├── config/
│   │   ├── settings.py           # Configurações
│   │   └── server_config.json    # Configuração do servidor
│   ├── core/
│   │   ├── server.py             # Servidor principal
│   │   ├── client_manager.py     # Gerenciamento de clientes
│   │   └── command_handler.py    # Processamento de comandos
│   ├── utils/
│   │   ├── logger.py             # Sistema de logging
│   │   └── helpers.py            # Funções auxiliares
│   └── requirements.txt          # Dependências
├── install_quality_agent.py      # Script de instalação
└── README.md                     # Este arquivo
```

## 🔍 Algoritmo de Localização de Logs

O sistema implementa navegação automática na estrutura de logs aninhada:

```
C:\Quality\LOG\{service}\{pasta_num}\{pasta_num}\{pasta_num}\{arquivo.txt}
```

**Exemplo de caminho resultante:**
```
C:\Quality\LOG\Integra\2025\01\22\integra_20250122_143052.txt
```

**Algoritmo:**
1. Navegar 3 níveis de pastas numéricas
2. Selecionar a pasta com o número mais alto (mais recente)
3. Encontrar o arquivo .txt mais recente por timestamp
4. Retornar o caminho completo do arquivo

## 🚨 Alertas Críticos

- 🚨 **IntegraWebService parado**: Todos os outros serviços podem falhar
- ⚠️ **ServicoFiscal instável**: Problemas com emissão fiscal
- 🔄 **Reinicialização em cascata**: Respeitar ordem de dependências
- 📊 **Alto uso de CPU/Memória**: Alertar antes de falha

## 🔧 Desenvolvimento

### Executar em Modo Debug

```bash
# Cliente
python cliente_agent/main.py --debug

# Servidor
python servidor_control/main.py --debug --quality-mode
```

### Testes

```bash
# Testar localizador de logs
python cliente_agent/utils/log_finder.py

# Testar instalação
python install_quality_agent.py
```

## 📝 Logs

### Cliente
- Console: Logs em tempo real
- Arquivo: `logs/quality_agent_YYYYMMDD.log` (modo debug)

### Servidor
- Console: Logs em tempo real
- Arquivo: `logs/quality_control_server_YYYYMMDD.log`

## 🆘 Solução de Problemas

### Cliente não conecta ao servidor
1. Verificar se o servidor está rodando
2. Verificar IP e porta na configuração
3. Verificar firewall/antivírus
4. Verificar logs do cliente

### Serviços não são detectados
1. Verificar caminhos dos executáveis
2. Executar como administrador
3. Verificar permissões de acesso
4. Atualizar configuração manualmente

### Logs não são encontrados
1. Verificar estrutura de pastas
2. Verificar permissões de leitura
3. Verificar encoding dos arquivos
4. Testar localizador de logs

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, consulte:
- Logs detalhados em modo debug
- Documentação dos módulos
- Testes de funcionalidades específicas

---

**Quality Remote Control System v1.0.0**  
Sistema de monitoramento e controle remoto para serviços Quality
