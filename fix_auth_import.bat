@echo off
echo Corrigindo import no arquivo auth.py...

REM Verificar se o arquivo existe
if not exist "C:\Quality\ControlPanel\utils\auth.py" (
    echo Erro: Arquivo auth.py nao encontrado
    pause
    exit /b 1
)

REM Fazer backup do arquivo original
copy "C:\Quality\ControlPanel\utils\auth.py" "C:\Quality\ControlPanel\utils\auth.py.backup"

REM Corrigir o import usando PowerShell
powershell -Command "(Get-Content 'C:\Quality\ControlPanel\utils\auth.py') -replace 'from typing import Dict, Any, Optional, Tuple', 'from typing import Dict, Any, Optional, Tuple, List' | Set-Content 'C:\Quality\ControlPanel\utils\auth.py'"

echo Import corrigido com sucesso!
echo.
echo Testando servidor...
cd /d "C:\Quality\ControlPanel"
python -c "from utils.auth import QualityAuthManager; print('Import funcionando!')"

if %errorlevel% equ 0 (
    echo.
    echo ✅ CORREÇÃO CONCLUÍDA COM SUCESSO!
    echo O servidor agora deve funcionar corretamente.
    echo.
    echo Execute: C:\Quality\ControlPanel\start_server.bat
) else (
    echo.
    echo ❌ Ainda há problemas com o import.
    echo Verifique o arquivo auth.py manualmente.
)

pause
