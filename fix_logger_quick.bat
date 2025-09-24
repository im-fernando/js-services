@echo off
echo ================================================================
echo CORRECAO RAPIDA - LOGGER DEBUG
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\utils\logger.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    pause
    exit /b 1
)

echo Corrigindo rapidamente o problema do logger...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\utils\logger.py" "C:\Quality\ControlPanel\utils\logger.py.backup_quick"
echo Backup criado: logger.py.backup_quick

REM Corrigir usando PowerShell
powershell -Command "
$file = 'C:\Quality\ControlPanel\utils\logger.py'
$content = Get-Content $file -Raw

# Corrigir self.debug = debug
$content = $content -replace 'self\.debug = debug', 'self.debug_mode = debug'
echo 'Corrigido: self.debug = debug'

# Corrigir self.debug em logger.setLevel
$content = $content -replace 'self\.debug(?!_mode)', 'self.debug_mode'
echo 'Corrigido: self.debug em logger.setLevel'

Set-Content $file $content
echo 'Arquivo corrigido!'
"

echo.
echo ================================================================
echo CORRECAO RAPIDA CONCLUIDA!
echo ================================================================
echo.
echo ✅ Problema do logger corrigido
echo ✅ Arquivo instalado atualizado
echo.
echo 🚀 Agora:
echo    1. Pare o servidor (Ctrl+C)
echo    2. Reinicie o servidor
echo    3. O erro não ocorrerá mais
echo.
echo ================================================================

echo.
pause
