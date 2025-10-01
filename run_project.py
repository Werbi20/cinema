#!/usr/bin/env python3
"""
Script para executar o projeto Cinema ERP completo
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    
    # Verificar Node.js
    node_result = run_command("node --version")
    if not node_result:
        print("❌ Node.js não encontrado")
        return False
    
    # Verificar npm
    npm_result = run_command("npm --version")
    if not npm_result:
        print("❌ npm não encontrado")
        return False
    
    print("✅ Dependências verificadas com sucesso")
    return True

def setup_backend():
    """Configura e executa o backend"""
    print("\n🚀 Configurando backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Diretório backend não encontrado")
        return False
    
    # Verificar se virtual environment existe
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("📦 Criando virtual environment...")
        run_command("python -m venv venv", cwd=backend_dir)
    
    # Ativar virtual environment e instalar dependências
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    print("📦 Instalando dependências do backend...")
    run_command(activate_cmd, cwd=backend_dir)
    
    # Verificar se arquivo .env existe
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚙️ Criando arquivo .env...")
        env_example = backend_dir / "env.example"
        if env_example.exists():
            run_command(f"copy env.example .env" if os.name == 'nt' else "cp env.example .env", cwd=backend_dir)
        else:
            print("⚠️ Arquivo env.example não encontrado. Configure manualmente as variáveis de ambiente.")
    
    print("✅ Backend configurado com sucesso")
    return True

def setup_frontend():
    """Configura e executa o frontend"""
    print("\n🎨 Configurando frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Diretório frontend não encontrado")
        return False
    
    # Instalar dependências
    print("📦 Instalando dependências do frontend...")
    run_command("npm install", cwd=frontend_dir)
    
    print("✅ Frontend configurado com sucesso")
    return True

def start_backend():
    """Inicia o backend em background"""
    print("\n🚀 Iniciando backend...")
    
    backend_dir = Path("backend")
    
    # Comando para ativar venv e executar
    if os.name == 'nt':  # Windows
        cmd = "venv\\Scripts\\activate && python run_app.py"
    else:  # Linux/Mac
        cmd = "source venv/bin/activate && python run_app.py"
    
    # Executar em background
    if os.name == 'nt':
        subprocess.Popen(cmd, cwd=backend_dir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(cmd, cwd=backend_dir, shell=True)
    
    print("✅ Backend iniciado em background")
    return True

def start_frontend():
    """Inicia o frontend em background"""
    print("\n🎨 Iniciando frontend...")
    
    frontend_dir = Path("frontend")
    
    # Executar em background
    if os.name == 'nt':
        subprocess.Popen("npm run dev", cwd=frontend_dir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen("npm run dev", cwd=frontend_dir, shell=True)
    
    print("✅ Frontend iniciado em background")
    return True

def wait_for_services():
    """Aguarda os serviços ficarem disponíveis"""
    print("\n⏳ Aguardando serviços ficarem disponíveis...")
    
    import requests
    
    # Aguardar backend
    backend_ready = False
    for i in range(30):  # 30 tentativas
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                backend_ready = True
                print("✅ Backend está rodando")
                break
        except:
            pass
        time.sleep(2)
    
    if not backend_ready:
        print("⚠️ Backend não respondeu em tempo hábil")
    
    # Aguardar frontend
    frontend_ready = False
    for i in range(30):  # 30 tentativas
        try:
            response = requests.get("http://localhost:5173", timeout=2)
            if response.status_code == 200:
                frontend_ready = True
                print("✅ Frontend está rodando")
                break
        except:
            pass
        time.sleep(2)
    
    if not frontend_ready:
        print("⚠️ Frontend não respondeu em tempo hábil")
    
    return backend_ready and frontend_ready

def open_browser():
    """Abre o navegador com as aplicações"""
    print("\n🌐 Abrindo navegador...")
    
    # Aguardar um pouco para os serviços inicializarem
    time.sleep(5)
    
    try:
        # Abrir frontend
        webbrowser.open("http://localhost:5173")
        print("✅ Frontend aberto no navegador")
        
        # Abrir documentação da API
        webbrowser.open("http://localhost:8000/docs")
        print("✅ Documentação da API aberta no navegador")
        
    except Exception as e:
        print(f"⚠️ Erro ao abrir navegador: {e}")

def main():
    """Função principal"""
    print("🎬 Cinema ERP - Sistema de Gestão de Locações")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        print("❌ Dependências não atendidas. Instale Python 3.8+ e Node.js 16+")
        return
    
    # Configurar backend
    if not setup_backend():
        print("❌ Falha ao configurar backend")
        return
    
    # Configurar frontend
    if not setup_frontend():
        print("❌ Falha ao configurar frontend")
        return
    
    # Iniciar serviços
    if not start_backend():
        print("❌ Falha ao iniciar backend")
        return
    
    if not start_frontend():
        print("❌ Falha ao iniciar frontend")
        return
    
    # Aguardar serviços
    if wait_for_services():
        print("\n🎉 Projeto iniciado com sucesso!")
        print("\n📱 Frontend: http://localhost:5173")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        
        # Abrir navegador
        open_browser()
        
        print("\n💡 Para parar os serviços, feche as janelas dos terminais")
        print("🔄 Para reiniciar, execute este script novamente")
        
    else:
        print("\n⚠️ Alguns serviços podem não estar funcionando corretamente")
        print("Verifique os logs nos terminais abertos")

if __name__ == "__main__":
    main()
