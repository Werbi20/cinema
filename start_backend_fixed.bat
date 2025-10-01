@echo off
echo ========================================
echo 🚀 Iniciando Backend Cinema ERP
echo ========================================

cd backend
echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 🌐 Iniciando servidor...
echo 💡 Servidor rodará em http://localhost:8020
echo 💡 Documentação da API: http://localhost:8020/docs
echo 💡 Para parar, pressione Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8020 --reload







