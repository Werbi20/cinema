import requests
import os

# Criar uma imagem de teste simples
from PIL import Image
img = Image.new('RGB', (100, 100), color='red')
img.save('test_image.png')

# Testar upload
url = "http://localhost:8020/api/v1/firebase-photos/upload/teste"

try:
    with open('test_image.png', 'rb') as f:
        files = {'photos': ('test_image.png', f, 'image/png')}
        response = requests.post(url, files=files)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar ao backend na porta 8020")
    print("Verifique se o backend está rodando em http://localhost:8020")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

# Limpar arquivo de teste
if os.path.exists('test_image.png'):
    os.remove('test_image.png')
