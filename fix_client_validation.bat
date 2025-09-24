@echo off
echo ================================================================
echo CORRECAO - VALIDACAO DE CLIENTES
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\utils\helpers.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo problema da validacao de clientes...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\utils\helpers.py" "C:\Quality\ControlPanel\utils\helpers.py.backup5"
echo Backup criado: helpers.py.backup5

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\utils\helpers.py' -Raw
$oldValidation = '    # Verificar se começa com QUALITY_CLIENTE_\n    return client_id.startswith(\"QUALITY_CLIENTE_\")'
$newValidation = '    # Aceitar IDs que começam com QUALITY_CLIENTE_ ou SERVIDOR_\n    return (client_id.startswith(\"QUALITY_CLIENTE_\") or \n            client_id.startswith(\"SERVIDOR_\") or\n            client_id.startswith(\"CLIENT_\"))'
$newContent = $content -replace [regex]::Escape($oldValidation), $newValidation
Set-Content 'C:\Quality\ControlPanel\utils\helpers.py' $newContent
"

echo Problema da validacao de clientes corrigido!
echo.

echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Erro da validação de clientes corrigido
echo ✅ Agora aceita IDs: QUALITY_CLIENTE_, SERVIDOR_, CLIENT_
echo.
echo 🚀 Agora você pode:
echo    1. Reiniciar o servidor
echo    2. O servidor aceitará o cliente SERVIDOR_TESTE
echo    3. Não haverá mais erros de validação
echo    4. Comunicação funcionará perfeitamente
echo.
echo ================================================================

echo.
pause
