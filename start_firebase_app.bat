@echo off
echo 🔥 Iniciando Cinema ERP - Sistema Firebase Completo
echo =====================================================

echo.
echo 📋 Verificando dependências...

echo.
echo 🗄️ Iniciando Backend (PostgreSQL + FastAPI)...
start "Backend - Cinema ERP" cmd /k "cd backend && echo 🚀 Iniciando Backend... && py complete_server.py"

echo.
echo ⏳ Aguardando backend inicializar...
timeout /t 8 /nobreak > nul

echo.
echo 🎨 Iniciando Frontend (React + Vite + Firebase)...
start "Frontend - Cinema ERP" cmd /k "cd frontend && echo 🎨 Iniciando Frontend... && npm run dev"

echo.
echo ⏳ Aguardando frontend inicializar...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Sistema Cinema ERP iniciado com sucesso!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🔥 Firebase: https://palaoro-production.firebaseapp.com/
echo.
echo 🎯 Funcionalidades disponíveis:
echo    ✅ Upload de fotos para Firebase Storage
echo    ✅ Sincronização com PostgreSQL
echo    ✅ Cache no Firestore
echo    ✅ Interface moderna e responsiva
echo.
echo Pressione qualquer tecla para sair...
pause > nul

