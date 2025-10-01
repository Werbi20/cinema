#!/bin/bash

echo "🚀 Iniciando Cinema ERP - Desenvolvimento"
echo

echo "📦 Verificando dependências..."
cd backend

if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute: python -m venv venv"
    exit 1
fi

echo "✅ Ambiente virtual encontrado"
echo

echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo "📋 Instalando dependências do backend..."
pip install -r requirements.txt

echo
echo "🗄️ Configurando banco de dados..."
python setup_database.py

echo
echo "🚀 Iniciando backend (porta 8000)..."
gnome-terminal --title="Backend - Cinema ERP" -- bash -c "cd $(pwd) && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000; exec bash"

echo
echo "⏳ Aguardando backend inicializar..."
sleep 5

echo
echo "📦 Verificando dependências do frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências do frontend..."
    npm install
fi

echo
echo "🎨 Iniciando frontend (porta 5173)..."
gnome-terminal --title="Frontend - Cinema ERP" -- bash -c "cd $(pwd) && npm run dev; exec bash"

echo
echo "✅ Serviços iniciados!"
echo
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo
echo "Pressione Enter para continuar..."
read

