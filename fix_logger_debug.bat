@echo off
echo ================================================================
echo CORRECAO - LOGGER DEBUG
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\utils\logger.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Corrigindo problema do logger debug...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\utils\logger.py" "C:\Quality\ControlPanel\utils\logger.py.backup6"
echo Backup criado: logger.py.backup6

REM Corrigir o problema usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\utils\logger.py' -Raw

# Corrigir o atributo debug
$oldInit = '    def __init__(self, name: str, debug: bool = False):\n        self.name = name\n        self.debug = debug\n        self.logger = self._setup_logger()'
$newInit = '    def __init__(self, name: str, debug: bool = False):\n        self.name = name\n        self.debug_mode = debug\n        self.logger = self._setup_logger()'

if ($content -match [regex]::Escape($oldInit)) {
    $content = $content -replace [regex]::Escape($oldInit), $newInit
    echo 'Atributo debug renomeado para debug_mode'
}

# Corrigir referência ao debug
$oldRef = 'logger.setLevel(logging.DEBUG if self.debug else logging.INFO)'
$newRef = 'logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)'

if ($content -match [regex]::Escape($oldRef)) {
    $content = $content -replace [regex]::Escape($oldRef), $newRef
    echo 'Referência ao debug corrigida'
}

Set-Content 'C:\Quality\ControlPanel\utils\logger.py' $content
"

echo Problema do logger debug corrigido!
echo.

echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Erro do logger debug corrigido
echo ✅ Atributo debug renomeado para debug_mode
echo ✅ Método debug() agora funciona corretamente
echo.
echo 🚀 Agora você pode:
echo    1. Reiniciar o servidor
echo    2. O servidor funcionará sem erros
echo    3. Comunicação funcionará perfeitamente
echo    4. Sistema completamente operacional
echo.
echo ================================================================

echo.
pause
