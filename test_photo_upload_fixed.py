#!/usr/bin/env python3
"""
Script para testar o sistema de upload de fotos corrigido
Testa tanto o endpoint Firebase quanto o fallback local
"""
import requests
import os
import sys
from io import BytesIO
from PIL import Image

def create_test_image(filename, size=(800, 600), color='red'):
    """Cria uma imagem de teste"""
    img = Image.new('RGB', size, color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def test_photo_upload():
    """Testa o upload de fotos"""

    # Configuração do servidor
    base_url = "http://localhost:8020/api/v1"
    location_id = "teste"

    print("🧪 Testando sistema de upload de fotos corrigido...")
    print(f"📍 Servidor: {base_url}")
    print(f"📍 Locação: {location_id}")

    # 1. Verificar se o servidor está funcionando
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Servidor está online")
        else:
            print(f"⚠️ Servidor respondeu com status {health_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Servidor não está acessível: {e}")
        print("💡 Certifique-se de que o backend está rodando na porta 8020")
        return False

    # 2. Verificar status do Firebase
    try:
        firebase_health = requests.get(f"http://localhost:8020/health/firebase", timeout=5)
        if firebase_health.status_code == 200:
            firebase_status = firebase_health.json()
            print(f"🔥 Firebase disponível: {firebase_status.get('available', False)}")
            print(f"🪣 Bucket: {firebase_status.get('bucket', 'N/A')}")
            print(f"🗄️ Storage: {firebase_status.get('storage', 'N/A')}")
        else:
            print("⚠️ Não foi possível verificar status do Firebase")
    except:
        print("⚠️ Firebase health check falhou")

    # 3. Criar imagens de teste
    print("\n📸 Criando imagens de teste...")
    test_files = []

    # Imagem pequena (válida)
    small_img = create_test_image("test_small.jpg", (400, 300), 'blue')
    test_files.append(("photos", ("test_small.jpg", small_img, "image/jpeg")))

    # Imagem média (válida)
    medium_img = create_test_image("test_medium.jpg", (800, 600), 'green')
    test_files.append(("photos", ("test_medium.jpg", medium_img, "image/jpeg")))

    print(f"✅ Criadas {len(test_files)} imagens de teste")

    # 4. Fazer upload das fotos
    print("\n📤 Fazendo upload das fotos...")
    try:
        upload_response = requests.post(
            f"{base_url}/firebase-photos/upload/{location_id}",
            files=test_files,
            timeout=30,
            headers={
                "X-API-Key": "dev_local_api_key_change"  # API key do desenvolvimento
            }
        )

        if upload_response.status_code == 200:
            result = upload_response.json()
            print(f"✅ Upload realizado com sucesso!")
            print(f"📊 {result.get('message', 'N/A')}")
            print(f"📁 Total de fotos na locação: {result.get('total_photos', 0)}")

            # Mostrar detalhes das fotos enviadas
            uploaded_photos = result.get('uploaded_photos', [])
            for i, photo in enumerate(uploaded_photos):
                print(f"   📷 Foto {i+1}: {photo.get('filename', 'N/A')}")
                print(f"      💾 Tamanho: {photo.get('size', 0)} bytes")
                print(f"      🔗 URL: {photo.get('url', 'N/A')}")
                if photo.get('storage'):
                    print(f"      🪣 Storage: {photo['storage'].get('bucket', 'local')}")

        else:
            print(f"❌ Erro no upload: {upload_response.status_code}")
            try:
                error_detail = upload_response.json()
                print(f"📝 Detalhes: {error_detail.get('detail', 'Erro desconhecido')}")
            except:
                print(f"📝 Resposta: {upload_response.text[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição de upload: {e}")
        return False

    # 5. Listar fotos da locação
    print("\n📋 Listando fotos da locação...")
    try:
        list_response = requests.get(
            f"{base_url}/firebase-photos/{location_id}",
            timeout=10,
            headers={
                "X-API-Key": "dev_local_api_key_change"
            }
        )

        if list_response.status_code == 200:
            photos_list = list_response.json()
            print(f"✅ Lista obtida com sucesso!")
            print(f"📊 Total de fotos: {photos_list.get('total', 0)}")

            photos = photos_list.get('photos', [])
            for i, photo in enumerate(photos):
                exists = photo.get('exists', False)
                status = "✅" if exists else "❌"
                print(f"   {status} Foto {i+1}: {photo.get('filename', 'N/A')}")
                print(f"      🔗 URL: {photo.get('url', 'N/A')}")
        else:
            print(f"❌ Erro ao listar fotos: {list_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição de listagem: {e}")

    # 6. Testar acesso a uma foto via proxy
    if upload_response.status_code == 200:
        result = upload_response.json()
        uploaded_photos = result.get('uploaded_photos', [])

        if uploaded_photos:
            print("\n🖼️ Testando acesso às fotos via proxy...")
            first_photo = uploaded_photos[0]
            filename = first_photo.get('filename', '').split('/')[-1]  # Pegar só o nome do arquivo

            try:
                photo_url = f"{base_url}/firebase-photos/file/{location_id}/{filename}"
                photo_response = requests.get(photo_url, timeout=10)

                if photo_response.status_code == 200:
                    print(f"✅ Foto acessível via proxy!")
                    print(f"🔗 URL: {photo_url}")
                    print(f"📏 Tamanho da resposta: {len(photo_response.content)} bytes")
                    print(f"📋 Content-Type: {photo_response.headers.get('content-type', 'N/A')}")
                else:
                    print(f"❌ Erro ao acessar foto: {photo_response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"❌ Erro no acesso à foto: {e}")

    print("\n🎉 Teste concluído!")
    return True

def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE UPLOAD DE FOTOS CORRIGIDO")
    print("=" * 60)

    success = test_photo_upload()

    print("\n" + "=" * 60)
    if success:
        print("✅ TESTE CONCLUÍDO - Verifique os resultados acima")
    else:
        print("❌ TESTE FALHOU - Verifique se o servidor está rodando")
    print("=" * 60)

if __name__ == "__main__":
    main()







