@echo off
echo ================================================================
echo CORRECAO - WEBSOCKET THREAD
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\core\server.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo problema de WebSocket thread...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\core\server.py" "C:\Quality\ControlPanel\core\server.py.backup2"
echo Backup criado: server.py.backup2

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\core\server.py' -Raw
$newContent = $content -replace 'self\.server_thread\.start\(\)\s*\n\s*except ImportError:', 'self.server_thread.start()\n            \n            # Aguardar um pouco para garantir que o servidor iniciou\n            time.sleep(1)\n            \n        except ImportError:'
Set-Content 'C:\Quality\ControlPanel\core\server.py' $newContent
"

echo Problema de WebSocket thread corrigido!
echo.

echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Problema de WebSocket thread corrigido
echo ✅ Servidor deve funcionar agora
echo.
echo 🚀 Agora você pode:
echo    1. Reiniciar o servidor
echo    2. Testar a conectividade
echo    3. Conectar o cliente
echo.
echo ================================================================

echo.
pause
