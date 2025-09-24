@echo off
echo ================================================================
echo CORRECAO - LOOP DO SERVIDOR
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\main.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo problema do loop do servidor...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\main.py" "C:\Quality\ControlPanel\main.py.backup3"
echo Backup criado: main.py.backup3

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\main.py' -Raw
$oldCode = '        server.start()\s*\n\s*except KeyboardInterrupt:'
$newCode = '        server.start()\n        \n        # Manter o servidor rodando\n        logger.info(\"🔄 Servidor rodando... Pressione Ctrl+C para parar\")\n        try:\n            while True:\n                time.sleep(1)\n        except KeyboardInterrupt:\n            logger.info(\"🛑 Parando servidor...\")\n            server.stop()\n            \n    except KeyboardInterrupt:'
$newContent = $content -replace $oldCode, $newCode
Set-Content 'C:\Quality\ControlPanel\main.py' $newContent
"

echo Problema do loop do servidor corrigido!
echo.

echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Problema do loop do servidor corrigido
echo ✅ Servidor agora ficará rodando continuamente
echo.
echo 🚀 Agora você pode:
echo    1. Reiniciar o servidor
echo    2. O servidor ficará rodando (não terminará)
echo    3. Testar a conectividade
echo    4. Conectar o cliente
echo.
echo ================================================================

echo.
pause
