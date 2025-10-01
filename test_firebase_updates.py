#!/usr/bin/env python3
"""
Script de teste para os novos endpoints Firebase do Cinema ERP
"""

import requests
import json
from datetime import datetime, timedelta

# Configuração base
BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key-here"  # Substitua pela sua API key

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def test_firebase_project_stages():
    """Testa os endpoints de Firebase Project Stages"""
    print("🧪 Testando Firebase Project Stages...")

    # Dados de teste
    project_id = 1
    location_id = 1

    # 1. Criar etapas padrão
    print("\n1. Criando etapas padrão...")
    response = requests.post(
        f"{BASE_URL}/project-stages/firebase/{project_id}/location/{location_id}/default",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Criadas {data['total_created']} etapas padrão")
    else:
        print(f"❌ Erro: {response.text}")

    # 2. Obter resumo das etapas
    print("\n2. Obtendo resumo das etapas...")
    response = requests.get(
        f"{BASE_URL}/project-stages/firebase/{project_id}/summary",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total de etapas: {data.get('total_stages', 0)}")
        print(f"✅ Concluídas: {data.get('completed_stages', 0)}")
        print(f"✅ Em andamento: {data.get('in_progress_stages', 0)}")
    else:
        print(f"❌ Erro: {response.text}")

    # 3. Obter todas as etapas do projeto
    print("\n3. Obtendo todas as etapas do projeto...")
    response = requests.get(
        f"{BASE_URL}/project-stages/firebase/{project_id}",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total de etapas: {data['total_stages']}")
        stages = data.get('stages', [])
        if stages:
            first_stage = stages[0]
            stage_id = first_stage['id']

            # 4. Atualizar status de uma etapa
            print(f"\n4. Atualizando status da etapa {stage_id}...")
            update_data = {
                "status": "in_progress",
                "progress_percentage": 25,
                "notes": "Iniciado via teste automatizado"
            }
            response = requests.put(
                f"{BASE_URL}/project-stages/{stage_id}/firebase",
                headers=headers,
                json=update_data
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Status atualizado com sucesso")
            else:
                print(f"❌ Erro: {response.text}")
    else:
        print(f"❌ Erro: {response.text}")

    # 5. Sincronizar com Firebase
    print("\n5. Sincronizando com Firebase...")
    response = requests.post(
        f"{BASE_URL}/project-stages/firebase/sync",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sincronização concluída")
        print(f"   Total processado: {data['results']['total_stages']}")
        print(f"   Sincronizados: {data['results']['synced_stages']}")
    else:
        print(f"❌ Erro: {response.text}")

def test_firebase_locations_stages():
    """Testa os endpoints de etapas de locação Firebase"""
    print("\n🧪 Testando Firebase Locations Stages...")

    location_id = 1
    project_id = 1

    # 1. Obter etapas de uma locação
    print("\n1. Obtendo etapas da locação...")
    response = requests.get(
        f"{BASE_URL}/locations/{location_id}/firebase-project-stages?project_id={project_id}",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total de etapas: {data['total_stages']}")
        stages = data.get('stages', [])
        if stages:
            stage_id = stages[0]['id']

            # 2. Atualizar status via endpoint de locação
            print(f"\n2. Atualizando status da etapa {stage_id} via locação...")
            update_data = {
                "status": "completed",
                "progress_percentage": 100,
                "notes": "Concluído via teste de locação"
            }
            response = requests.put(
                f"{BASE_URL}/locations/{location_id}/firebase-project-stages/{stage_id}/status",
                headers=headers,
                json=update_data
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Status atualizado com sucesso")
            else:
                print(f"❌ Erro: {response.text}")
    else:
        print(f"❌ Erro: {response.text}")

def test_health_checks():
    """Testa os endpoints de saúde"""
    print("\n🧪 Testando Health Checks...")

    # 1. Health geral
    print("\n1. Health check geral...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Aplicação saudável")
    else:
        print(f"❌ Problemas na aplicação: {response.text}")

    # 2. Health Firebase
    print("\n2. Health check Firebase...")
    response = requests.get(f"{BASE_URL}/../health/firebase")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Firebase disponível: {data.get('available')}")
        print(f"   Firestore: {data.get('firestore')}")
        print(f"   Storage: {data.get('storage')}")
    else:
        print(f"❌ Problemas no Firebase: {response.text}")

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes dos endpoints Firebase atualizados...")
    print(f"Base URL: {BASE_URL}")

    try:
        test_health_checks()
        test_firebase_project_stages()
        test_firebase_locations_stages()

        print("\n🎉 Testes concluídos!")

    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
