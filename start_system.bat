@echo off
echo 🚀 Iniciando Sistema Cinema ERP
echo =====================================

echo.
echo 📋 Iniciando Backend (PostgreSQL + FastAPI)...
start "Backend" cmd /k "cd backend && py simple_working_server.py"

echo.
echo ⏳ Aguardando backend inicializar...
timeout /t 5 /nobreak > nul

echo.
echo 🎨 Iniciando Frontend (React + Vite)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Sistema iniciado!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Pressione qualquer tecla para sair...
pause > nul

