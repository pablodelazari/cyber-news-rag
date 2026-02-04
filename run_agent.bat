@echo off
title Cyber News RAG Agent
color 0A
cls

echo ==================================================
echo       CYBER NEWS RAG - AGENTIC INTERFACE
echo ==================================================
echo.
echo initializing system...
echo.

:loop
color 0A
set /p query="Digite sua pergunta (ou 'sair' para fechar): "

if "%query%"=="sair" goto end
if "%query%"=="" goto loop

echo.
echo [AGENT] Analisando sua pergunta...
echo.
python main.py "%query%"
echo.
echo ==================================================
echo.
goto loop

:end
echo Bye!
pause
