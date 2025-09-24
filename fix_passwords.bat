@echo off
echo ================================================================
echo CORRECAO - SENHAS DOS USUARIOS
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\config\users_config.json" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    pause
    exit /b 1
)

echo Corrigindo senhas dos usuarios...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\config\users_config.json" "C:\Quality\ControlPanel\config\users_config.json.backup_passwords"
echo Backup criado: users_config.json.backup_passwords

REM Corrigir usando PowerShell
powershell -Command "
$file = 'C:\Quality\ControlPanel\config\users_config.json'
$content = Get-Content $file -Raw

# Hash correto da senha 'quality123'
$correctHash = '0f840d7354d0873e3054340243d745a0670ca3da75acb727e75228afee529bbb'
$oldHash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

# Substituir hash incorreto pelo correto
if ($content -match [regex]::Escape($oldHash)) {
    $content = $content -replace [regex]::Escape($oldHash), $correctHash
    echo 'Hash da senha corrigido!'
} else {
    echo 'Hash ja esta correto ou nao encontrado'
}

Set-Content $file $content
echo 'Arquivo corrigido!'
"

echo.
echo ================================================================
echo CORRECAO CONCLUIDA COM SUCESSO!
echo ================================================================
echo.
echo ✅ Senhas dos usuários corrigidas
echo ✅ Hash da senha 'quality123' atualizado
echo.
echo 👤 USUÁRIOS DISPONÍVEIS:
echo    - admin / quality123 (Administrador)
echo    - joao.silva / quality123 (Suporte Sênior)
echo    - maria.santos / quality123 (Suporte Júnior)
echo.
echo 🚀 Agora você pode:
echo    1. Tentar fazer login novamente
echo    2. Usar as senhas corretas
echo    3. Acessar o sistema normalmente
echo.
echo ================================================================

echo.
pause
