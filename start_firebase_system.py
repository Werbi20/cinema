#!/usr/bin/env python3
"""
Script para iniciar o sistema após migração Firebase
Configura e inicia backend e frontend com Firebase
"""

import asyncio
import os
import subprocess
import time
import webbrowser
from datetime import datetime


class FirebaseSystemStarter:
    """Inicializador do sistema com Firebase"""

    def __init__(self):
        self.processes = []
        self.start_time = datetime.now()

    def log(self, message: str, level: str = "INFO"):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def start_process(self, command: str, description: str, cwd: str = None, wait: int = 3):
        """Iniciar processo em background"""
        self.log(f"🚀 Iniciando: {description}")

        try:
            # Iniciar processo
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.processes.append({
                'process': process,
                'description': description,
                'command': command
            })

            # Aguardar um pouco para o processo inicializar
            time.sleep(wait)

            # Verificar se ainda está rodando
            if process.poll() is None:
                self.log(f"✅ {description} - Iniciado (PID: {process.pid})")
                return True
            else:
                # Processo terminou, ler erro
                _, stderr = process.communicate()
                self.log(f"❌ {description} - Falhou: {stderr.decode()}", "ERROR")
                return False

        except Exception as e:
            self.log(f"❌ Erro ao iniciar {description}: {e}", "ERROR")
            return False

    def check_firebase_cli(self):
        """Verificar se Firebase CLI está instalado"""
        try:
            result = subprocess.run(
                "firebase --version",
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"✅ Firebase CLI encontrado: {version}")
                return True
            else:
                self.log("❌ Firebase CLI não encontrado", "ERROR")
                self.log("💡 Instale com: npm install -g firebase-tools", "INFO")
                return False

        except Exception as e:
            self.log(f"❌ Erro ao verificar Firebase CLI: {e}", "ERROR")
            return False

    def setup_environment(self):
        """Configurar ambiente"""
        self.log("🔧 Configurando ambiente...")

        # Verificar se estamos no diretório correto
        if not os.path.exists("backend") or not os.path.exists("frontend"):
            self.log("❌ Execute este script na raiz do projeto", "ERROR")
            return False

        # Verificar arquivos de configuração Firebase
        config_files = [
            "firebase.json",
            "backend/firebase_config.json",
            "frontend/src/config/firebase.ts"
        ]

        missing_files = []
        for file_path in config_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            self.log("⚠️ Arquivos de configuração ausentes:", "WARNING")
            for file_path in missing_files:
                self.log(f"   • {file_path}", "WARNING")
        else:
            self.log("✅ Arquivos de configuração encontrados")

        return True

    def start_firebase_emulators(self):
        """Iniciar emuladores Firebase (desenvolvimento)"""
        self.log("🔥 Iniciando emuladores Firebase...")

        # Verificar se firebase.json existe
        if not os.path.exists("firebase.json"):
            self.log("❌ firebase.json não encontrado", "ERROR")
            return False

        # Iniciar emuladores
        return self.start_process(
            "firebase emulators:start",
            "Firebase Emulators",
            wait=10
        )

    def start_backend_server(self):
        """Iniciar servidor backend"""
        self.log("🐍 Iniciando servidor backend...")

        # Verificar se virtual environment existe
        venv_paths = ["backend/venv", "venv", "backend/.venv", ".venv"]
        venv_path = None

        for path in venv_paths:
            if os.path.exists(path):
                venv_path = path
                break

        if venv_path:
            # Usar virtual environment
            if os.name == 'nt':  # Windows
                activate_cmd = f"{venv_path}\\Scripts\\activate"
                command = f"cmd /c \"{activate_cmd} && cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8021 --reload\""
            else:  # Linux/Mac
                activate_cmd = f"source {venv_path}/bin/activate"
                command = f"{activate_cmd} && cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8021 --reload"
        else:
            # Sem virtual environment
            command = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8021 --reload"

        return self.start_process(
            command,
            "Backend Server (FastAPI)",
            cwd="backend",
            wait=5
        )

    def start_frontend_server(self):
        """Iniciar servidor frontend"""
        self.log("⚛️ Iniciando servidor frontend...")

        # Verificar se node_modules existe
        if not os.path.exists("frontend/node_modules"):
            self.log("📦 Instalando dependências do frontend...")

            install_result = subprocess.run(
                "npm install",
                shell=True,
                cwd="frontend",
                capture_output=True,
                text=True
            )

            if install_result.returncode != 0:
                self.log("❌ Falha ao instalar dependências", "ERROR")
                return False
            else:
                self.log("✅ Dependências instaladas")

        # Iniciar servidor de desenvolvimento
        return self.start_process(
            "npm start",
            "Frontend Server (React)",
            cwd="frontend",
            wait=15
        )

    def wait_for_services(self):
        """Aguardar serviços ficarem disponíveis"""
        self.log("⏳ Aguardando serviços ficarem disponíveis...")

        import requests

        services = [
            ("Backend API", "http://localhost:8021/docs", 30),
            ("Frontend", "http://localhost:3000", 45),
        ]

        for service_name, url, timeout in services:
            self.log(f"🔍 Testando {service_name}: {url}")

            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        self.log(f"✅ {service_name} disponível")
                        break
                except:
                    pass

                time.sleep(2)
            else:
                self.log(f"⚠️ {service_name} não respondeu em {timeout}s", "WARNING")

    def open_browser(self):
        """Abrir navegador com aplicação"""
        self.log("🌐 Abrindo navegador...")

        urls_to_open = [
            "http://localhost:3000",  # Frontend
            "http://localhost:8021/docs",  # Backend API docs
        ]

        for url in urls_to_open:
            try:
                webbrowser.open(url)
                time.sleep(1)
            except Exception as e:
                self.log(f"⚠️ Erro ao abrir {url}: {e}", "WARNING")

    def show_status(self):
        """Mostrar status dos serviços"""
        self.log("📊 Status dos serviços:")

        for process_info in self.processes:
            process = process_info['process']
            description = process_info['description']

            if process.poll() is None:
                self.log(f"   ✅ {description} (PID: {process.pid})")
            else:
                self.log(f"   ❌ {description} (Parado)")

    def cleanup(self):
        """Parar todos os processos"""
        self.log("🛑 Parando serviços...")

        for process_info in self.processes:
            process = process_info['process']
            description = process_info['description']

            if process.poll() is None:
                self.log(f"⏹️ Parando {description}")
                process.terminate()

                # Aguardar um pouco
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Forçar parada se necessário
                    process.kill()

    async def start_system(self, use_emulators: bool = False):
        """Iniciar sistema completo"""
        self.log("🔥 INICIANDO SISTEMA FIREBASE")
        self.log("=" * 50)

        # Configurar ambiente
        if not self.setup_environment():
            return False

        success_count = 0
        total_services = 3 if use_emulators else 2

        # Iniciar emuladores Firebase (se solicitado)
        if use_emulators:
            if self.check_firebase_cli() and self.start_firebase_emulators():
                success_count += 1

        # Iniciar backend
        if self.start_backend_server():
            success_count += 1

        # Iniciar frontend
        if self.start_frontend_server():
            success_count += 1

        if success_count == total_services:
            self.log("✅ Todos os serviços iniciados com sucesso!")

            # Aguardar serviços ficarem disponíveis
            self.wait_for_services()

            # Abrir navegador
            self.open_browser()

            # Mostrar informações
            self.show_system_info()

            return True
        else:
            self.log(f"❌ Falha ao iniciar alguns serviços ({success_count}/{total_services})", "ERROR")
            return False

    def show_system_info(self):
        """Mostrar informações do sistema"""
        self.log("=" * 50)
        self.log("🎯 SISTEMA FIREBASE ATIVO")
        self.log("=" * 50)
        self.log("📱 Frontend: http://localhost:3000")
        self.log("🔧 Backend API: http://localhost:8021")
        self.log("📚 API Docs: http://localhost:8021/docs")
        self.log("=" * 50)
        self.log("💡 COMANDOS ÚTEIS:")
        self.log("   • Ctrl+C para parar todos os serviços")
        self.log("   • firebase emulators:start para emuladores")
        self.log("   • firebase deploy para produção")
        self.log("=" * 50)

        # Manter sistema rodando
        try:
            self.log("🔄 Sistema rodando... (Ctrl+C para parar)")
            while True:
                time.sleep(10)
                # Verificar se processos ainda estão rodando
                active_processes = sum(
                    1 for p in self.processes
                    if p['process'].poll() is None
                )

                if active_processes == 0:
                    self.log("⚠️ Todos os processos pararam", "WARNING")
                    break

        except KeyboardInterrupt:
            self.log("\n🛑 Parando sistema...")
        finally:
            self.cleanup()


async def main():
    """Função principal"""
    starter = FirebaseSystemStarter()

    try:
        # Perguntar sobre emuladores
        print("🔥 INICIALIZAÇÃO DO SISTEMA FIREBASE")
        print("=" * 40)
        print("Escolha o modo de execução:")
        print("1. Produção (usar Firebase real)")
        print("2. Desenvolvimento (usar emuladores)")
        print()

        choice = input("Digite sua escolha (1/2): ").strip()
        use_emulators = choice == "2"

        if use_emulators:
            print("🧪 Modo desenvolvimento - Emuladores Firebase")
        else:
            print("🚀 Modo produção - Firebase real")

        print()

        # Iniciar sistema
        success = await starter.start_system(use_emulators)

        if not success:
            print("\n❌ Falha ao iniciar sistema")

    except KeyboardInterrupt:
        print("\n⏹️ Inicialização cancelada")


if __name__ == "__main__":
    asyncio.run(main())
