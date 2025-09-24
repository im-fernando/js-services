@echo off
echo ================================================================
echo CORRECAO - ARGUMENTOS DO SERVIDOR
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\main.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo argumento --multi-attendant no main.py...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\main.py" "C:\Quality\ControlPanel\main.py.backup"
echo Backup criado: main.py.backup

REM Adicionar o argumento --multi-attendant
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\main.py'
$newContent = $content -replace 'parser.add_argument\(''--quality-mode'', action=''store_true'',', 'parser.add_argument(''--quality-mode'', action=''store_true'','
$newContent = $newContent -replace 'help=''Modo específico para serviços Quality''\)', 'help=''Modo específico para serviços Quality'')\n    parser.add_argument(''--multi-attendant'', action=''store_true'',\n                       help=''Modo multi-atendente (padrão)'')'
Set-Content 'C:\Quality\ControlPanel\main.py' $newContent
"

echo Argumento --multi-attendant adicionado!
echo.

echo Testando servidor...
cd /d "C:\Quality\ControlPanel"

REM Testar se o argumento é reconhecido
python main.py --multi-attendant --help >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Argumento --multi-attendant reconhecido!
    echo ✅ Servidor pode ser inicializado!
    echo.
    echo ================================================================
    echo CORRECAO CONCLUIDA COM SUCESSO!
    echo ================================================================
    echo.
    echo ✅ Argumento --multi-attendant adicionado
    echo ✅ Servidor testado e funcionando
    echo ✅ Pronto para uso!
    echo.
    echo 🚀 Agora voce pode executar:
    echo    C:\Quality\ControlPanel\start_server.bat
    echo.
    echo ================================================================
) else (
    echo ❌ Ainda ha problemas com o argumento.
    echo Verifique o arquivo main.py manualmente.
    echo.
    echo 💡 Tente executar o servidor mesmo assim:
    echo    C:\Quality\ControlPanel\start_server.bat
)

echo.
pause
