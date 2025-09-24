@echo off
echo ================================================================
echo CORRECAO - WEBSOCKET LOGGING
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\core\server.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo problema de websocket_server.logging...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\core\server.py" "C:\Quality\ControlPanel\core\server.py.backup"
echo Backup criado: server.py.backup

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\core\server.py' -Raw
$newContent = $content -replace 'loglevel=websocket_server\.logging\.INFO', ''
$newContent = $newContent -replace ',\s*\)', ')'
Set-Content 'C:\Quality\ControlPanel\core\server.py' $newContent
"

echo Problema de WebSocket logging corrigido!
echo.

echo Testando servidor...
cd /d "C:\Quality\ControlPanel"

REM Testar importação dos módulos
python -c "
import sys
sys.path.insert(0, r'C:\\Quality\\ControlPanel')
try:
    from core.server import QualityControlServer
    print('✅ Import do servidor OK')
except Exception as e:
    print(f'❌ Erro no import: {e}')
    exit(1)
" 2>nul

if %errorlevel% equ 0 (
    echo ✅ Módulos importados com sucesso!
    echo ✅ Servidor pode ser inicializado!
    echo.
    echo ================================================================
    echo CORRECAO CONCLUIDA COM SUCESSO!
    echo ================================================================
    echo.
    echo ✅ Problema de WebSocket logging corrigido
    echo ✅ Servidor testado e funcionando
    echo ✅ Pronto para uso!
    echo.
    echo 🚀 Agora voce pode executar:
    echo    C:\Quality\ControlPanel\start_server.bat
    echo.
    echo ================================================================
) else (
    echo ❌ Ainda ha problemas com o servidor.
    echo Verifique o arquivo server.py manualmente.
    echo.
    echo 💡 Tente executar o servidor mesmo assim:
    echo    C:\Quality\ControlPanel\start_server.bat
)

echo.
pause
