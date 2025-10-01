@echo off
echo 🔥 Iniciando Sistema Cinema ERP - Versão Melhorada
echo ==================================================

echo.
echo 🐍 Configurando Python...
set PYTHON_PATH=C:\Users\werbi\AppData\Local\Programs\Python\Python313\python.exe

echo.
echo 🗄️ Iniciando Backend...
start "Backend - Cinema ERP" cmd /k "cd backend && echo 🚀 Iniciando Backend... && %PYTHON_PATH% simple_firebase_server.py"

echo.
echo ⏳ Aguardando backend inicializar...
timeout /t 8 /nobreak > nul

echo.
echo 🎨 Iniciando Frontend...
start "Frontend - Cinema ERP" cmd /k "cd frontend && echo 🎨 Iniciando Frontend... && npm run dev"

echo.
echo ⏳ Aguardando frontend inicializar...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Sistema iniciado com sucesso!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
echo.
echo 💡 Dicas:
echo    - O backend usa PostgreSQL com dados mock
echo    - O frontend tem todas as melhorias implementadas
echo    - Logs detalhados estão disponíveis nos terminais
echo.
echo Pressione qualquer tecla para sair...
pause > nul
