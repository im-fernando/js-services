@echo off
echo ================================================================
echo DEBUG - ERRO DO SERVIDOR
echo ================================================================
echo.

REM Verificar se o servidor existe
if not exist "C:\Quality\ControlPanel\core\server.py" (
    echo Erro: Servidor nao encontrado em C:\Quality\ControlPanel
    echo Execute primeiro: python install_multi_attendant_system.py
    pause
    exit /b 1
)

echo Adicionando codigo de debug ao servidor...
echo.

REM Fazer backup
copy "C:\Quality\ControlPanel\core\server.py" "C:\Quality\ControlPanel\core\server.py.backup_debug"
echo Backup criado: server.py.backup_debug

REM Adicionar debug usando PowerShell
powershell -Command "
$content = Get-Content 'C:\Quality\ControlPanel\core\server.py' -Raw

# Adicionar import do traceback
if ($content -notmatch 'import traceback') {
    $content = $content -replace 'import threading', 'import threading\nimport traceback'
    echo 'Import traceback adicionado'
}

# Adicionar debug no _process_message
$oldProcess = '        except Exception as e:\n            self.logger.error\(f\"❌ Erro ao processar mensagem de \{client_id\}: \{e\}\"\)'
$newProcess = '        except Exception as e:\n            # Debug detalhado do erro\n            error_traceback = traceback.format_exc()\n            self.logger.error\(f\"❌ Erro ao processar mensagem de \{client_id\}: \{e\}\"\)\n            self.logger.error\(f\"📋 Traceback completo:\\n\{error_traceback\}\"\)\n            print\(f\"DEBUG - Erro detalhado: \{e\}\"\)\n            print\(f\"DEBUG - Traceback:\\n\{error_traceback\}\")'

if ($content -match [regex]::Escape($oldProcess)) {
    $content = $content -replace [regex]::Escape($oldProcess), $newProcess
    echo 'Debug adicionado ao _process_message'
}

# Adicionar debug no message_received
$oldReceived = '        except Exception as e:\n            self.logger.error\(f\"❌ Erro ao processar mensagem: \{e\}\"\)'
$newReceived = '        except Exception as e:\n            # Debug detalhado do erro\n            error_traceback = traceback.format_exc()\n            self.logger.error\(f\"❌ Erro ao processar mensagem: \{e\}\"\)\n            self.logger.error\(f\"📋 Traceback completo:\\n\{error_traceback\}\"\)\n            print\(f\"DEBUG - Erro detalhado: \{e\}\"\)\n            print\(f\"DEBUG - Traceback:\\n\{error_traceback\}\")'

if ($content -match [regex]::Escape($oldReceived)) {
    $content = $content -replace [regex]::Escape($oldReceived), $newReceived
    echo 'Debug adicionado ao message_received'
}

Set-Content 'C:\Quality\ControlPanel\core\server.py' $content
"

echo Codigo de debug adicionado!
echo.

echo ================================================================
echo DEBUG ADICIONADO COM SUCESSO!
echo ================================================================
echo.
echo ✅ Código de debug adicionado ao servidor
echo ✅ Agora mostrará traceback completo dos erros
echo.
echo 🚀 Próximos passos:
echo    1. Reinicie o servidor
echo    2. Conecte o cliente
echo    3. Observe o traceback detalhado
echo    4. Identifique exatamente onde está o erro
echo.
echo ================================================================

echo.
pause
