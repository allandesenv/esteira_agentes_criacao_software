from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path("projects")


def preparar_release(project_name: str, version: str = "0.1.0") -> str:
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        raise FileNotFoundError("Projeto não encontrado")

    release_md = project_dir / "release.md"
    success_md = project_dir / "sucesso_cliente.md"

    data = datetime.now().strftime("%Y-%m-%d")

    release_content = f"""
# Release {version}

## Data
{data}

## Escopo Entregue
- MVP conforme definido
- API funcional
- Health check
- Deploy via Docker

## Checklist Go / No-Go
- [x] MVP definido
- [x] Arquitetura aprovada
- [x] Código revisado
- [x] Estratégia de testes definida
- [x] Deploy validado

## Riscos Conhecidos
- Escopo inicial limitado
- Dependência de feedback real do usuário

## Próximos Passos
- Coletar feedback do cliente
- Priorizar melhorias
- Planejar próxima versão
"""

    success_content = """
# Sucesso do Cliente

## Objetivo
Garantir que o cliente obtenha valor real com o produto entregue.

## Métricas Iniciais
- Uso diário do sistema
- Funcionalidades mais acessadas
- Problemas reportados

## Plano de Acompanhamento
- Reunião de validação pós-release
- Coleta de feedback em 7 dias
- Ajustes rápidos conforme necessidade

## Riscos de Churn
- Baixa adoção
- Expectativa desalinhada

## Ações Preventivas
- Comunicação clara
- Evolução contínua baseada em dados
"""

    release_md.write_text(release_content.strip())
    success_md.write_text(success_content.strip())

    return f"Release {version} preparado com foco em entrega e sucesso do cliente"