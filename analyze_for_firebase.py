#!/usr/bin/env python3
"""
Script para analisar estrutura do banco SQLite e mapear para Firestore
"""

import sqlite3
import json

def analyze_sqlite_structure():
    """Analisar estrutura do banco SQLite"""
    conn = sqlite3.connect('cinema_erp.db')
    cursor = conn.cursor()

    # Obter todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("📊 Análise da Estrutura do Banco SQLite")
    print("=" * 50)

    structure = {}

    for table in tables:
        table_name = table[0]
        print(f"\n🗂️  Tabela: {table_name}")

        # Obter estrutura da tabela
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Obter quantidade de registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        table_structure = {
            'columns': [],
            'record_count': count
        }

        print(f"   📝 Colunas ({len(columns)}):")
        for col in columns:
            col_info = {
                'name': col[1],
                'type': col[2],
                'not_null': col[3],
                'default': col[4],
                'primary_key': col[5]
            }
            table_structure['columns'].append(col_info)
            pk_marker = " (PK)" if col[5] else ""
            null_marker = " NOT NULL" if col[3] else ""
            print(f"      - {col[1]}: {col[2]}{pk_marker}{null_marker}")

        print(f"   📊 Registros: {count}")

        # Exemplo de dados (se existirem)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            sample = cursor.fetchone()
            if sample:
                print(f"   🔍 Exemplo: {sample[:3]}...")  # Primeiros 3 campos

        structure[table_name] = table_structure

    conn.close()

    # Salvar estrutura em arquivo
    with open('sqlite_structure_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Análise salva em: sqlite_structure_analysis.json")

    return structure

def map_to_firestore_collections():
    """Mapear tabelas SQLite para coleções Firestore"""

    firestore_mapping = {
        'users': {
            'collection': 'users',
            'subcollections': ['preferences', 'notifications'],
            'indexes': ['email', 'role', 'active']
        },
        'projects': {
            'collection': 'projects',
            'subcollections': ['stages', 'tasks', 'locations'],
            'indexes': ['status', 'created_by', 'start_date', 'end_date']
        },
        'locations': {
            'collection': 'locations',
            'subcollections': ['photos', 'visits', 'contracts'],
            'indexes': ['status', 'type', 'city', 'state', 'availability']
        },
        'suppliers': {
            'collection': 'suppliers',
            'subcollections': ['contacts', 'contracts'],
            'indexes': ['type', 'status', 'city']
        },
        'contracts': {
            'collection': 'contracts',
            'subcollections': ['payments', 'documents'],
            'indexes': ['status', 'start_date', 'end_date', 'location_id', 'project_id']
        },
        'notifications': {
            'collection': 'notifications',
            'subcollections': [],
            'indexes': ['user_id', 'read', 'created_at', 'type']
        },
        'presentations': {
            'collection': 'presentations',
            'subcollections': ['items'],
            'indexes': ['project_id', 'created_at', 'status']
        }
    }

    print("\n🔥 Mapeamento para Firestore Collections")
    print("=" * 50)

    for table, mapping in firestore_mapping.items():
        print(f"\n📁 {table} → {mapping['collection']}")
        if mapping['subcollections']:
            print(f"   📂 Subcoleções: {', '.join(mapping['subcollections'])}")
        print(f"   🔍 Índices: {', '.join(mapping['indexes'])}")

    # Salvar mapeamento
    with open('firestore_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(firestore_mapping, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Mapeamento salvo em: firestore_mapping.json")

    return firestore_mapping

if __name__ == "__main__":
    print("Iniciando analise para migracao Firebase...")

    try:
        # Analisar estrutura SQLite
        structure = analyze_sqlite_structure()

        # Criar mapeamento Firestore
        mapping = map_to_firestore_collections()

        print("\nProximos passos:")
        print("1. Implementar adaptador Firestore")
        print("2. Migrar dados do SQLite para Firestore")
        print("3. Atualizar APIs para usar Firestore")
        print("4. Configurar regras de seguranca")
        print("5. Implementar Firebase Functions")

    except Exception as e:
        print(f"[ERRO] Erro durante analise: {e}")
