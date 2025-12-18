from pathlib import Path

PROJECTS_DIR = Path("projects")


def definir_estrategia_testes(project_name: str) -> str:
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        raise FileNotFoundError("Projeto não encontrado")

    testes_md = project_dir / "testes.md"

    conteudo = """
# Estratégia de Testes

## Objetivo
Garantir qualidade mínima, evitar regressões e dar segurança para evolução do produto.

## Tipos de Testes

### 1. Testes Unitários
- Funções puras
- Regras de negócio
- Validações

### 2. Testes de Integração
- Endpoints principais
- Integração com banco de dados
- Fluxos críticos do MVP

### 3. Testes Automatizados Iniciais
- Endpoint /health
- Inicialização da aplicação

## Ferramentas
- pytest
- fastapi.testclient

## Critérios de Aceite
- Cobertura mínima nos fluxos do MVP
- Testes executando automaticamente
- Falha em testes bloqueia avanço

## Riscos
- Falsa sensação de segurança
- Testes frágeis ou excessivos

## Próximos Passos
- Expandir testes conforme features
- Avaliar testes de carga futuramente
"""

    testes_md.write_text(conteudo.strip())

    return "Estratégia de testes criada com sucesso"