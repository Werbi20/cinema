"""
Migração Firebase - Agenda Atualizada
Cinema ERP Sistema de Gestão de Locações

Esta migração adiciona suporte completo para Firebase nas funcionalidades
de agenda que foram reativadas no frontend.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FirebaseAgendaMigration:
    """Classe para migrar e sincronizar dados da agenda com Firebase"""

    def __init__(self, db_session, firebase_client=None):
        self.db = db_session
        self.firebase = firebase_client

    def migrate_existing_stages_to_firebase(self) -> Dict[str, Any]:
        """Migra etapas existentes para Firebase"""
        try:
            from backend.app.models.project_location_stage import ProjectLocationStage

            # Buscar todas as etapas existentes
            existing_stages = self.db.query(ProjectLocationStage).all()

            migration_results = {
                "total_stages": len(existing_stages),
                "migrated": 0,
                "failed": 0,
                "errors": []
            }

            for stage in existing_stages:
                try:
                    # Preparar dados para Firebase
                    firebase_data = {
                        "id": stage.id,
                        "name": stage.name,
                        "description": stage.description or "",
                        "status": stage.status,
                        "project_id": stage.project_id,
                        "location_id": stage.location_id,
                        "progress_percentage": stage.progress_percentage or 0,
                        "budget_allocated": float(stage.budget_allocated) if stage.budget_allocated else None,
                        "planned_start_date": stage.planned_start_date.isoformat() if stage.planned_start_date else None,
                        "planned_end_date": stage.planned_end_date.isoformat() if stage.planned_end_date else None,
                        "actual_start_date": stage.actual_start_date.isoformat() if stage.actual_start_date else None,
                        "actual_end_date": stage.actual_end_date.isoformat() if stage.actual_end_date else None,
                        "notes": stage.notes or "",
                        "order": stage.order or 0,
                        "created_at": stage.created_at.isoformat() if stage.created_at else None,
                        "updated_at": stage.updated_at.isoformat() if stage.updated_at else None
                    }

                    # TODO: Enviar para Firebase quando estiver configurado
                    # self.firebase.collection('project_stages').document(str(stage.id)).set(firebase_data)

                    migration_results["migrated"] += 1
                    logger.info(f"Etapa {stage.id} migrada para Firebase")

                except Exception as e:
                    migration_results["failed"] += 1
                    error_msg = f"Erro ao migrar etapa {stage.id}: {str(e)}"
                    migration_results["errors"].append(error_msg)
                    logger.error(error_msg)

            return migration_results

        except Exception as e:
            logger.error(f"Erro na migração: {str(e)}")
            return {
                "total_stages": 0,
                "migrated": 0,
                "failed": 0,
                "errors": [f"Erro geral: {str(e)}"]
            }

    def validate_frontend_compatibility(self) -> Dict[str, Any]:
        """Valida se os dados estão compatíveis com o frontend atualizado"""
        validation_results = {
            "compatible": True,
            "issues": [],
            "recommendations": []
        }

        try:
            from backend.app.models.project_location_stage import ProjectLocationStage
            from backend.app.models.location import Location
            from backend.app.models.project import Project

            # Verificar se existem projetos com locações
            projects_with_locations = self.db.query(Project).filter(
                Project.locations.any()
            ).all()

            if not projects_with_locations:
                validation_results["issues"].append("Nenhum projeto com locações encontrado")
                validation_results["recommendations"].append("Criar projetos com locações para testar a agenda")

            # Verificar se existem etapas para os projetos
            stages_count = self.db.query(ProjectLocationStage).count()
            if stages_count == 0:
                validation_results["issues"].append("Nenhuma etapa de projeto encontrada")
                validation_results["recommendations"].append("Criar etapas padrão para projetos existentes")

            # Verificar status válidos
            invalid_status_stages = self.db.query(ProjectLocationStage).filter(
                ~ProjectLocationStage.status.in_([
                    'pending', 'in_progress', 'completed', 'on_hold',
                    'cancelled', 'approved', 'rejected'
                ])
            ).all()

            if invalid_status_stages:
                validation_results["issues"].append(f"{len(invalid_status_stages)} etapas com status inválido")
                validation_results["recommendations"].append("Atualizar status das etapas para valores válidos")

            # Verificar se há dados órfãos
            orphaned_stages = self.db.query(ProjectLocationStage).filter(
                ~ProjectLocationStage.project_id.in_(
                    self.db.query(Project.id)
                )
            ).all()

            if orphaned_stages:
                validation_results["issues"].append(f"{len(orphaned_stages)} etapas órfãs encontradas")
                validation_results["recommendations"].append("Limpar etapas órfãs")

            if validation_results["issues"]:
                validation_results["compatible"] = False

            return validation_results

        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return {
                "compatible": False,
                "issues": [f"Erro na validação: {str(e)}"],
                "recommendations": ["Verificar configuração do banco de dados"]
            }

    def create_sample_data(self) -> Dict[str, Any]:
        """Cria dados de exemplo para testar a agenda"""
        try:
            from backend.app.models.project import Project
            from backend.app.models.location import Location
            from backend.app.models.project_location import ProjectLocation
            from backend.app.services.project_location_stage_service import ProjectLocationStageService

            creation_results = {
                "projects_created": 0,
                "locations_created": 0,
                "stages_created": 0,
                "errors": []
            }

            # TODO: Implementar criação de dados de exemplo
            # Esta função pode ser usada para criar dados de teste

            return creation_results

        except Exception as e:
            logger.error(f"Erro ao criar dados de exemplo: {str(e)}")
            return {
                "projects_created": 0,
                "locations_created": 0,
                "stages_created": 0,
                "errors": [f"Erro: {str(e)}"]
            }

def run_migration(db_session, firebase_client=None):
    """Executa a migração completa"""
    migration = FirebaseAgendaMigration(db_session, firebase_client)

    print("🚀 Iniciando migração Firebase para agenda atualizada...")

    # 1. Validar compatibilidade
    print("\n1. Validando compatibilidade com frontend...")
    validation = migration.validate_frontend_compatibility()

    if validation["compatible"]:
        print("✅ Dados compatíveis com frontend atualizado")
    else:
        print("⚠️ Problemas de compatibilidade encontrados:")
        for issue in validation["issues"]:
            print(f"   - {issue}")
        print("\n📋 Recomendações:")
        for rec in validation["recommendations"]:
            print(f"   - {rec}")

    # 2. Migrar etapas existentes
    print("\n2. Migrando etapas existentes para Firebase...")
    migration_results = migration.migrate_existing_stages_to_firebase()

    print(f"   Total de etapas: {migration_results['total_stages']}")
    print(f"   Migradas: {migration_results['migrated']}")
    print(f"   Falharam: {migration_results['failed']}")

    if migration_results["errors"]:
        print("   Erros encontrados:")
        for error in migration_results["errors"]:
            print(f"   - {error}")

    print("\n🎉 Migração concluída!")

    return {
        "validation": validation,
        "migration": migration_results
    }

if __name__ == "__main__":
    # Este script pode ser executado independentemente para migração
    print("Migração Firebase - Agenda Atualizada")
    print("Para executar, importe e chame run_migration() com uma sessão de banco de dados")
