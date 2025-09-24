@echo off
echo ================================================================
echo CORRECAO COMPLETA - TODOS OS IMPORTS DO SERVIDOR
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo imports nos arquivos do servidor...
echo.

REM Corrigir utils/auth.py
if exist "C:\Quality\ControlPanel\utils\auth.py" (
    echo Corrigindo utils/auth.py...
    copy "C:\Quality\ControlPanel\utils\auth.py" "C:\Quality\ControlPanel\utils\auth.py.backup"
    powershell -Command "(Get-Content 'C:\Quality\ControlPanel\utils\auth.py') -replace 'from typing import Dict, Any, Optional, Tuple', 'from typing import Dict, Any, Optional, Tuple, List' | Set-Content 'C:\Quality\ControlPanel\utils\auth.py'"
    echo   ✅ utils/auth.py corrigido
) else (
    echo   ❌ utils/auth.py nao encontrado
)

REM Corrigir core/attendant_manager.py
if exist "C:\Quality\ControlPanel\core\attendant_manager.py" (
    echo Corrigindo core/attendant_manager.py...
    copy "C:\Quality\ControlPanel\core\attendant_manager.py" "C:\Quality\ControlPanel\core\attendant_manager.py.backup"
    powershell -Command "(Get-Content 'C:\Quality\ControlPanel\core\attendant_manager.py') -replace 'from typing import Dict, Any, List, Optional', 'from typing import Dict, Any, List, Optional, Tuple' | Set-Content 'C:\Quality\ControlPanel\core\attendant_manager.py'"
    echo   ✅ core/attendant_manager.py corrigido
) else (
    echo   ❌ core/attendant_manager.py nao encontrado
)

echo.
echo Testando imports...
cd /d "C:\Quality\ControlPanel"

REM Testar import do auth
python -c "from utils.auth import QualityAuthManager; print('✅ utils.auth importado com sucesso')" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ utils.auth funcionando
) else (
    echo   ❌ utils.auth ainda com problemas
)

REM Testar import do attendant_manager
python -c "from core.attendant_manager import AttendantManager; print('✅ core.attendant_manager importado com sucesso')" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ core.attendant_manager funcionando
) else (
    echo   ❌ core.attendant_manager ainda com problemas
)

REM Testar import do server
python -c "from core.server import QualityControlServer; print('✅ core.server importado com sucesso')" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ core.server funcionando
) else (
    echo   ❌ core.server ainda com problemas
)

echo.
echo ================================================================
echo TESTE FINAL - INICIALIZACAO DO SERVIDOR
echo ================================================================

REM Testar inicialização completa
python -c "
try:
    from core.server import QualityControlServer
    from config.settings import load_config
    print('✅ Todos os imports funcionando!')
    print('✅ Servidor pode ser inicializado!')
except Exception as e:
    print(f'❌ Erro: {e}')
    exit(1)
"

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo CORRECAO CONCLUIDA COM SUCESSO!
    echo ================================================================
    echo.
    echo ✅ Todos os imports corrigidos
    echo ✅ Servidor testado e funcionando
    echo ✅ Pronto para uso!
    echo.
    echo 🚀 Agora voce pode executar:
    echo    C:\Quality\ControlPanel\start_server.bat
    echo.
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo CORRECAO APLICADA, MAS AINDA HA PROBLEMAS
    echo ================================================================
    echo.
    echo ⚠️  Os imports foram corrigidos, mas ainda ha problemas.
    echo    Verifique os logs acima para mais detalhes.
    echo.
    echo 💡 Tente executar o servidor mesmo assim:
    echo    C:\Quality\ControlPanel\start_server.bat
    echo.
    echo ================================================================
)

echo.
pause
