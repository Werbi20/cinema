@echo off
echo ========================================
echo 🚀 Iniciando Backend para Teste de Fotos
echo ========================================

cd backend

echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 🔧 Verificando dependências...
pip install -q -r requirements.txt

echo 🌐 Iniciando servidor na porta 8020...
echo 💡 O servidor ficará rodando até você pressionar Ctrl+C
echo 💡 Para testar, abra outro terminal e execute: python test_photo_upload_fixed.py
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8020 --reload







