@echo off
echo 🚀 Iniciando Cinema ERP - Desenvolvimento
echo.

echo 📦 Verificando dependências...
cd backend
if not exist "venv" (
    echo ❌ Ambiente virtual não encontrado. Execute: python -m venv venv
    pause
    exit /b 1
)

echo ✅ Ambiente virtual encontrado
echo.

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📋 Instalando dependências do backend...
pip install -r requirements.txt

echo.
echo 🗄️ Configurando banco de dados...
python setup_database.py

echo.
echo 🚀 Iniciando backend (porta 8000)...
start "Backend - Cinema ERP" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && py -m uvicorn app.main:app --reload --port 8000"

echo.
echo ⏳ Aguardando backend inicializar...
timeout /t 5 /nobreak > nul

echo.
echo 📦 Verificando dependências do frontend...
cd ..\frontend
if not exist "node_modules" (
    echo 📥 Instalando dependências do frontend...
    npm install
)

echo.
echo 🎨 Iniciando frontend (porta 5173)...
start "Frontend - Cinema ERP" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ✅ Serviços iniciados!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Pressione qualquer tecla para fechar...
pause > nul

