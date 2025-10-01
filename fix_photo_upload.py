#!/usr/bin/env python3
"""
Script para corrigir problemas de upload de fotos no Firebase
"""

import requests
import json
from PIL import Image
import io
import base64

# Configurar endpoint
BASE_URL = "http://localhost:8020"

def test_backend_connection():
    """Testar se o backend está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Backend está rodando: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando ou não está acessível")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com backend: {e}")
        return False

def create_test_image():
    """Criar uma imagem de teste"""
    img = Image.new('RGB', (200, 200), color='blue')

    # Salvar em buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

def test_firebase_upload():
    """Testar upload para Firebase"""
    print("\n🔥 Testando upload para Firebase...")

    if not test_backend_connection():
        return False

    # Criar imagem de teste
    img_buffer = create_test_image()

    # Testar upload
    url = f"{BASE_URL}/api/v1/firebase-photos/upload/teste"

    try:
        files = {'photos': ('test_firebase.png', img_buffer, 'image/png')}
        response = requests.post(url, files=files, timeout=30)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Upload realizado com sucesso!")
            print(f"📝 Resposta: {json.dumps(result, indent=2)}")

            # Verificar se foi para Firebase ou local
            if result.get('uploaded_photos'):
                photo = result['uploaded_photos'][0]
                if 'firebase-photos' in photo.get('url', ''):
                    print("🔥 Foto foi salva no Firebase Storage!")
                else:
                    print("💾 Foto foi salva localmente (fallback)")

                # Testar se conseguimos acessar a foto
                photo_url = f"{BASE_URL}{photo['url']}"
                try:
                    photo_response = requests.get(photo_url)
                    if photo_response.status_code == 200:
                        print(f"✅ Foto acessível em: {photo_url}")
                    else:
                        print(f"❌ Erro ao acessar foto: {photo_response.status_code}")
                except Exception as e:
                    print(f"❌ Erro ao acessar foto: {e}")

            return True
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro durante upload: {e}")
        return False

def check_firebase_config():
    """Verificar configuração do Firebase"""
    print("\n🔧 Verificando configuração do Firebase...")

    try:
        # Ler arquivo de configuração
        with open('backend/firebase_config.json', 'r') as f:
            config = json.load(f)

        print("✅ Arquivo firebase_config.json encontrado")

        firebase_config = config.get('firebase', {})
        backend_config = config.get('backend', {})

        print(f"📝 Project ID: {firebase_config.get('projectId')}")
        print(f"📝 Storage Bucket: {firebase_config.get('storageBucket')}")
        print(f"📝 Backend Project ID: {backend_config.get('project_id')}")
        print(f"📝 Backend Storage Bucket: {backend_config.get('storage_bucket')}")

        # Verificar se os buckets são consistentes
        if firebase_config.get('storageBucket') != backend_config.get('storage_bucket'):
            print("⚠️  AVISO: Storage buckets diferentes entre configurações!")
            print(f"   Frontend: {firebase_config.get('storageBucket')}")
            print(f"   Backend: {backend_config.get('storage_bucket')}")

        return True

    except FileNotFoundError:
        print("❌ Arquivo firebase_config.json não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro ao ler configuração: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Testando sistema de upload de fotos...")
    print("="*50)

    # Verificar configuração
    check_firebase_config()

    # Testar upload
    success = test_firebase_upload()

    if success:
        print("\n✅ Sistema de upload está funcionando!")
        print("💡 Se as fotos estão sendo salvas localmente ao invés do Firebase,")
        print("   verifique as permissões do Firebase Storage e as regras de segurança.")
    else:
        print("\n❌ Sistema de upload apresentou problemas.")
        print("💡 Verifique se o backend está rodando e se a configuração do Firebase está correta.")

if __name__ == "__main__":
    main()
