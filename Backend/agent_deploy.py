from pathlib import Path

PROJECTS_DIR = Path("projects")


def preparar_deploy(project_name: str) -> str:
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        raise FileNotFoundError("Projeto não encontrado")

    dockerfile = project_dir / "Dockerfile"
    compose = project_dir / "docker-compose.yml"

    dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    compose_content = """
version: '3.9'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
"""

    dockerfile.write_text(dockerfile_content.strip())
    compose.write_text(compose_content.strip())

    return "Arquivos de deploy criados (Dockerfile e docker-compose.yml)"