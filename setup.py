#!/usr/bin/env python3
"""
Script de setup para o Cinema ERP
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Imprime cabeçalho do setup"""
    print("🎬" * 50)
    print("🎬  CINEMA ERP - SISTEMA DE GESTÃO DE LOCAÇÕES  🎬")
    print("🎬" * 50)
    print()

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_node():
    """Verifica se Node.js está instalado"""
    print("📦 Verificando Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} - OK")
            return True
        else:
            print("❌ Node.js não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Node.js não encontrado")
        return False

def install_backend_dependencies():
    """Instala dependências do backend"""
    print("\n🔧 Instalando dependências do backend...")
    
    if not os.path.exists("backend"):
        print("❌ Diretório backend não encontrado")
        return False
    
    os.chdir("backend")
    
    try:
        # Criar ambiente virtual se não existir
        if not os.path.exists("venv"):
            print("   Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Ativar ambiente virtual
        if platform.system() == "Windows":
            activate_script = "venv\\Scripts\\activate"
        else:
            activate_script = "venv/bin/activate"
        
        # Instalar dependências
        print("   Instalando dependências Python...")
        if platform.system() == "Windows":
            subprocess.run(["venv\\Scripts\\pip", "install", "-r", "requirements.txt"], check=True)
        else:
            subprocess.run(["venv/bin/pip", "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependências do backend instaladas com sucesso!")
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        os.chdir("..")
        return False

def install_frontend_dependencies():
    """Instala dependências do frontend"""
    print("\n🔧 Instalando dependências do frontend...")
    
    if not os.path.exists("frontend"):
        print("❌ Diretório frontend não encontrado")
        return False
    
    os.chdir("frontend")
    
    try:
        print("   Instalando dependências Node.js...")
        subprocess.run(["npm", "install"], check=True)
        print("✅ Dependências do frontend instaladas com sucesso!")
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        os.chdir("..")
        return False

def create_env_file():
    """Cria arquivo .env se não existir"""
    print("\n📝 Criando arquivo de configuração...")
    
    env_content = """# Configurações do Cinema ERP
DATABASE_URL=sqlite:///./cinema_erp.db
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
"""
    
    if not os.path.exists("backend/.env"):
        with open("backend/.env", "w") as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
    else:
        print("ℹ️  Arquivo .env já existe")

def print_next_steps():
    """Imprime próximos passos"""
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("=" * 50)
    
    print("\n1️⃣  INICIAR BACKEND:")
    print("   cd backend")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("   source venv/bin/activate")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    print("\n2️⃣  POPULAR BANCO COM DADOS DE EXEMPLO:")
    print("   cd backend")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\python scripts/seed_data.py")
    else:
        print("   venv/bin/python scripts/seed_data.py")
    
    print("\n3️⃣  INICIAR FRONTEND:")
    print("   cd frontend")
    print("   npm run dev")
    
    print("\n4️⃣  ACESSAR APLICAÇÃO:")
    print("   Backend API: http://localhost:8000")
    print("   Documentação: http://localhost:8000/docs")
    print("   Frontend: http://localhost:5173")
    
    print("\n" + "=" * 50)

def main():
    """Função principal"""
    print_header()
    
    # Verificações
    if not check_python_version():
        sys.exit(1)
    
    if not check_node():
        print("\n⚠️  Node.js não encontrado. Instale em: https://nodejs.org/")
        print("   Continuando apenas com o backend...")
    
    # Instalação
    if not install_backend_dependencies():
        print("\n❌ Falha na instalação do backend")
        sys.exit(1)
    
    if check_node() and not install_frontend_dependencies():
        print("\n❌ Falha na instalação do frontend")
        sys.exit(1)
    
    # Configuração
    create_env_file()
    
    # Próximos passos
    print_next_steps()
    
    print("\n🎉 SETUP CONCLUÍDO COM SUCESSO!")
    print("   Siga os próximos passos acima para executar a aplicação.")

if __name__ == "__main__":
    main()

