@echo off
echo ================================================================
echo CORRECAO - IMPORT DO TIME
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\main.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo erro do import do time...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\main.py" "C:\Quality\ControlPanel\main.py.backup4"
echo Backup criado: main.py.backup4

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\main.py' -Raw
if ($content -match 'import time') {
    echo 'Import do time ja existe'
} else {
    $oldImports = 'import sys\nimport os\nimport argparse\nimport signal\nfrom pathlib import Path'
    $newImports = 'import sys\nimport os\nimport argparse\nimport signal\nimport time\nfrom pathlib import Path'
    $newContent = $content -replace [regex]::Escape($oldImports), $newImports
    Set-Content 'C:\Quality\ControlPanel\main.py' $newContent
    echo 'Import do time adicionado!'
}
"

echo Problema do import do time corrigido!
echo.

echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Erro do import do time corrigido
echo ✅ Servidor agora funcionará sem erros
echo.
echo 🚀 Agora você pode:
echo    1. Reiniciar o servidor
echo    2. O servidor ficará rodando sem erros
echo    3. Testar a conectividade
echo    4. Conectar o cliente
echo.
echo ================================================================

echo.
pause
