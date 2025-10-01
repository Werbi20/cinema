#!/usr/bin/env python3
"""
Script para testar a criação de etapas para locações de projetos
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from app.core.database import SQLALCHEMY_DATABASE_URL
from app.models import *
from app.services.project_location_stage_service import ProjectLocationStageService
from app.schemas.project_location_stage import ProjectLocationStageCreate
from app.models.project_location_stage import ProjectLocationStageType, ProjectLocationStageStatus
from sqlalchemy.orm import sessionmaker

def test_stages_creation():
    """Testar criação de etapas"""
    print("🧪 Testando criação de etapas...")

    # Criar engine e sessão
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Verificar se existem projetos e locações
        projects = db.query(Project).all()
        locations = db.query(Location).all()
        project_locations = db.query(ProjectLocation).all()

        print(f"📊 Dados encontrados:")
        print(f"  - Projetos: {len(projects)}")
        print(f"  - Locações: {len(locations)}")
        print(f"  - Locações de Projetos: {len(project_locations)}")

        if not projects:
            print("❌ Nenhum projeto encontrado. Execute o setup_database.py primeiro.")
            return False

        if not locations:
            print("❌ Nenhuma locação encontrada. Execute o setup_database.py primeiro.")
            return False

        if not project_locations:
            print("❌ Nenhuma locação de projeto encontrada. Execute o create_project_locations.py primeiro.")
            return False

        # Usar o primeiro projeto e locação disponíveis
        project = projects[0]
        project_location = project_locations[0]

        print(f"\n🎯 Testando com:")
        print(f"  - Projeto: {project.name} (ID: {project.id})")
        print(f"  - Locação: {project_location.location_id}")

        # Criar serviço de etapas
        stage_service = ProjectLocationStageService(db)

        # Teste 1: Criar etapas padrão
        print(f"\n📋 Teste 1: Criando etapas padrão...")
        try:
            default_stages = stage_service.create_default_stages_for_location(
                project.id,
                project_location.location_id
            )
            print(f"✅ {len(default_stages)} etapas padrão criadas com sucesso!")

            for stage in default_stages:
                print(f"  - {stage.name} ({stage.stage_type}) - {stage.status}")

        except Exception as e:
            print(f"❌ Erro ao criar etapas padrão: {e}")
            return False

        # Teste 2: Criar etapa personalizada
        print(f"\n📋 Teste 2: Criando etapa personalizada...")
        try:
            custom_stage_data = ProjectLocationStageCreate(
                project_id=project.id,
                location_id=project_location.location_id,
                name="Etapa Personalizada de Teste",
                description="Etapa criada para teste do sistema",
                stage_type=ProjectLocationStageType.CUSTOM,
                status=ProjectLocationStageStatus.PENDING,
                order_index=10,
                is_mandatory=False,
                notes="Etapa de teste criada via script"
            )

            custom_stage = stage_service.create_stage(custom_stage_data)
            print(f"✅ Etapa personalizada criada: {custom_stage.name} (ID: {custom_stage.id})")

        except Exception as e:
            print(f"❌ Erro ao criar etapa personalizada: {e}")
            return False

        # Teste 3: Buscar etapas criadas
        print(f"\n📋 Teste 3: Buscando etapas criadas...")
        try:
            stages = stage_service.get_stages_by_project_and_location(
                project.id,
                project_location.location_id
            )
            print(f"✅ {len(stages)} etapas encontradas para o projeto e locação:")

            for stage in stages:
                print(f"  - {stage.name} ({stage.stage_type}) - {stage.status} - Progresso: {stage.progress_percentage}%")

        except Exception as e:
            print(f"❌ Erro ao buscar etapas: {e}")
            return False

        # Teste 4: Atualizar status de uma etapa
        print(f"\n📋 Teste 4: Atualizando status de etapa...")
        try:
            if stages:
                first_stage = stages[0]
                updated_stage = stage_service.update_stage_status(
                    first_stage.id,
                    ProjectLocationStageStatus.IN_PROGRESS,
                    "Iniciando etapa de teste"
                )
                print(f"✅ Status atualizado: {updated_stage.name} -> {updated_stage.status}")

        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
            return False

        # Teste 5: Resumo das etapas
        print(f"\n📋 Teste 5: Resumo das etapas do projeto...")
        try:
            summary = stage_service.get_project_stages_summary(project.id)
            print(f"✅ Resumo do projeto:")
            print(f"  - Total de etapas: {summary.total_stages}")
            print(f"  - Concluídas: {summary.completed_stages}")
            print(f"  - Em andamento: {summary.in_progress_stages}")
            print(f"  - Pendentes: {summary.pending_stages}")
            print(f"  - Atrasadas: {summary.overdue_stages}")
            print(f"  - Progresso geral: {summary.overall_progress:.1f}%")

        except Exception as e:
            print(f"❌ Erro ao obter resumo: {e}")
            return False

        print(f"\n🎉 Todos os testes de etapas passaram com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando teste de criação de etapas...")

    success = test_stages_creation()

    if success:
        print("\n✅ Sistema de etapas funcionando corretamente!")
        print("📋 Funcionalidades testadas:")
        print("  ✅ Criação de etapas padrão")
        print("  ✅ Criação de etapas personalizadas")
        print("  ✅ Busca de etapas")
        print("  ✅ Atualização de status")
        print("  ✅ Resumo de progresso")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs acima.")
        sys.exit(1)
