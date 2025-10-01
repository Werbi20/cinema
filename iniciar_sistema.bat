@echo off
echo 🔥 Iniciando Sistema Cinema ERP - Firebase
echo ==========================================

echo.
echo 🗄️ Iniciando Backend...
start "Backend" cmd /k "cd backend && echo 🚀 Iniciando Backend... && py simple_firebase_server.py"

echo.
echo ⏳ Aguardando backend...
timeout /t 8 /nobreak > nul

echo.
echo 🎨 Iniciando Frontend...
start "Frontend" cmd /k "cd frontend && echo 🎨 Iniciando Frontend... && npm run dev"

echo.
echo ⏳ Aguardando frontend...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Sistema iniciado!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Pressione qualquer tecla para sair...
pause > nul
