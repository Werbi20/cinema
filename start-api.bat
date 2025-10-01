@echo off
title Cinema ERP - API Server
color 0A

echo.
echo ========================================
echo    🚀 CINEMA ERP - API SERVER
echo ========================================
echo.

echo 🔍 Verificando dependências...
cd backend

echo.
echo 📦 Verificando se Python está instalado...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado!

echo.
echo 📦 Verificando dependências...
pip list | findstr fastapi >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dependências não encontradas. Instalando...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erro ao instalar dependências!
        pause
        exit /b 1
    )
    echo ✅ Dependências instaladas!
) else (
    echo ✅ Dependências já instaladas!
)

echo.
echo 🚀 Iniciando servidor da API...
echo.
echo 🌐 URL da API: http://127.0.0.1:8000
echo 📚 Documentação: http://127.0.0.1:8000/docs
echo 🔍 Health Check: http://127.0.0.1:8000/health
echo.
echo ⏹️  Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

python simple_server.py

echo.
echo 🛑 Servidor parado.
pause


