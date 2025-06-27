@echo off
echo Определение IP-адреса...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r /c:"IPv4"') do (
    set IP=%%a
    goto :found
)

:found
echo.
echo Используйте следующий IP-адрес вместо localhost:
echo %IP%
echo.
echo Фронтенд: http:%IP%:8080
echo Бэкенд API: http:%IP%:8000
echo API документация: http:%IP%:8000/docs
echo Ollama API: http:%IP%:11434
echo.
pause 