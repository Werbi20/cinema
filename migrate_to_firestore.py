#!/usr/bin/env python3
"""
Script para migrar dados do SQLite para Firestore
"""

import sqlite3
import json
import asyncio
from datetime import datetime
import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.firestore_adapter import firestore_adapter


class SQLiteToFirestoreMigration:
    """Classe para migrar dados do SQLite para Firestore"""

    def __init__(self, sqlite_path: str = 'cinema_erp.db'):
        self.sqlite_path = sqlite_path
        self.firestore = firestore_adapter

        # Mapeamento de tabelas SQLite para coleções Firestore
        self.table_mapping = {
            'users': 'users',
            'projects': 'projects',
            'locations': 'locations',
            'suppliers': 'suppliers',
            'contracts': 'contracts',
            'notifications': 'notifications',
            'presentations': 'presentations',
            'tags': 'tags',
            'project_stages': 'project_stages',
            'project_tasks': 'project_tasks',
            'location_photos': 'location_photos',
            'visits': 'visits',
            'financial_movements': 'financial_movements',
            'audit_log': 'audit_log',
            'agenda_events': 'agenda_events'
        }

    def get_sqlite_data(self, table_name: str) -> list:
        """Obter dados de uma tabela SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Converter para lista de dicionários
            data = []
            for row in rows:
                row_dict = dict(row)
                data.append(row_dict)

            return data

        except sqlite3.Error as e:
            print(f"❌ Erro ao ler tabela {table_name}: {e}")
            return []
        finally:
            conn.close()

    def prepare_data_for_firestore(self, data: dict, table_name: str) -> dict:
        """Preparar dados para Firestore"""
        # Converter campos JSON se existirem
        json_fields = [
            'preferences_json', 'address_json', 'settings_json',
            'variables_json', 'criteria_json', 'accessibility_features',
            'availability_json', 'exif_json', 'custom_data', 'tags',
            'attachments', 'special_requirements', 'equipment_needed',
            'metadata_json', 'before_json', 'after_json'
        ]

        for field in json_fields:
            if field in data and data[field]:
                try:
                    if isinstance(data[field], str):
                        data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    print(f"⚠️ Erro ao converter JSON do campo {field}: {data[field]}")
                    data[field] = {}

        # Converter timestamps
        timestamp_fields = [
            'created_at', 'updated_at', 'token_expires_at', 'read_at',
            'approved_at', 'generated_at', 'sent_at', 'signed_at', 'expires_at',
            'completed_at', 'start_datetime', 'end_datetime', 'movement_date'
        ]

        for field in timestamp_fields:
            if field in data and data[field]:
                try:
                    if isinstance(data[field], str):
                        # Tentar parsing ISO format
                        data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                except ValueError:
                    print(f"⚠️ Erro ao converter timestamp {field}: {data[field]}")

        # Converter campos específicos por tabela
        if table_name == 'users':
            # Remover password_hash por segurança (será refeito com Firebase Auth)
            if 'password_hash' in data:
                del data['password_hash']

        elif table_name == 'locations':
            # Converter photos de string para array se necessário
            if 'photos' in data and isinstance(data['photos'], str):
                try:
                    data['photos'] = json.loads(data['photos'])
                except:
                    data['photos'] = []

        # Usar ID existente como documento ID
        doc_id = None
        if 'id' in data:
            doc_id = str(data['id'])
            del data['id']  # Remover ID dos dados (será usado como doc ID)

        return data, doc_id

    async def migrate_table(self, table_name: str) -> bool:
        """Migrar uma tabela específica"""
        print(f"\n📊 Migrando tabela: {table_name}")

        if table_name not in self.table_mapping:
            print(f"⚠️ Tabela {table_name} não mapeada para Firestore")
            return False

        collection_name = self.table_mapping[table_name]

        # Obter dados do SQLite
        sqlite_data = self.get_sqlite_data(table_name)

        if not sqlite_data:
            print(f"   📭 Nenhum dado encontrado na tabela {table_name}")
            return True

        print(f"   📦 Encontrados {len(sqlite_data)} registros")

        # Migrar cada registro
        migrated_count = 0
        errors = 0

        for row_data in sqlite_data:
            try:
                # Preparar dados
                firestore_data, doc_id = self.prepare_data_for_firestore(row_data, table_name)

                # Criar documento no Firestore
                created_id = await self.firestore.create_document(
                    collection_name,
                    firestore_data,
                    doc_id
                )

                migrated_count += 1
                print(f"   ✅ Migrado: {doc_id or created_id}")

            except Exception as e:
                errors += 1
                print(f"   ❌ Erro ao migrar registro: {e}")

        print(f"   📊 Resultado: {migrated_count} sucessos, {errors} erros")
        return errors == 0

    async def migrate_all(self) -> dict:
        """Migrar todas as tabelas"""
        print("🚀 Iniciando migração completa SQLite → Firestore")
        print("=" * 60)

        results = {}

        # Ordem de migração (respeitar dependências)
        migration_order = [
            'users',
            'suppliers',
            'tags',
            'projects',
            'locations',
            'project_stages',
            'project_tasks',
            'contracts',
            'location_photos',
            'visits',
            'notifications',
            'presentations',
            'financial_movements',
            'audit_log',
            'agenda_events'
        ]

        for table_name in migration_order:
            if table_name in self.table_mapping:
                success = await self.migrate_table(table_name)
                results[table_name] = success

        print("\n" + "=" * 60)
        print("📊 Resumo da Migração:")

        successful = sum(1 for success in results.values() if success)
        total = len(results)

        for table, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {table}")

        print(f"\n🎯 Total: {successful}/{total} tabelas migradas com sucesso")

        if successful == total:
            print("🎉 Migração concluída com sucesso!")
        else:
            print("⚠️ Migração concluída com alguns erros")

        return results

    async def verify_migration(self) -> dict:
        """Verificar se a migração foi bem-sucedida"""
        print("\n🔍 Verificando migração...")

        verification = {}

        for table_name, collection_name in self.table_mapping.items():
            try:
                # Contar registros no SQLite
                sqlite_count = len(self.get_sqlite_data(table_name))

                # Contar documentos no Firestore
                firestore_count = await self.firestore.count_documents(collection_name)

                verification[table_name] = {
                    'sqlite_count': sqlite_count,
                    'firestore_count': firestore_count,
                    'match': sqlite_count == firestore_count
                }

                status = "✅" if sqlite_count == firestore_count else "❌"
                print(f"   {status} {table_name}: SQLite={sqlite_count}, Firestore={firestore_count}")

            except Exception as e:
                print(f"   ❌ Erro ao verificar {table_name}: {e}")
                verification[table_name] = {'error': str(e)}

        return verification


async def main():
    """Função principal"""
    migration = SQLiteToFirestoreMigration()

    print("🔥 Migração de Dados: SQLite → Firebase Firestore")
    print("=" * 60)

    try:
        # Executar migração
        results = await migration.migrate_all()

        # Verificar migração
        verification = await migration.verify_migration()

        # Salvar relatório
        report = {
            'migration_results': results,
            'verification': verification,
            'timestamp': datetime.now().isoformat()
        }

        with open('migration_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n📄 Relatório salvo em: migration_report.json")

    except Exception as e:
        print(f"❌ Erro durante migração: {e}")


if __name__ == "__main__":
    asyncio.run(main())
