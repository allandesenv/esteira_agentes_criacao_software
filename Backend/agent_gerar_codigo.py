from pathlib import Path
import os

PROJECTS_DIR = Path("projects")


def gerar_codigo(project_name: str) -> str:
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        raise FileNotFoundError("Projeto não encontrado")

    # Estrutura base
    paths = [
        project_dir / "app" / "core",
        project_dir / "app" / "api",
        project_dir / "tests",
    ]

    for p in paths:
        p.mkdir(parents=True, exist_ok=True)

    # main.py
    (project_dir / "app" / "main.py").write_text(
        """
from fastapi import FastAPI

app = FastAPI(title='Sistema de Estoque')

@app.get('/health')
def health():
    return {'status': 'ok'}
"""
    )

    # health test
    (project_dir / "tests" / "test_health.py").write_text(
        """
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
"""
    )

    # requirements
    (project_dir / "requirements.txt").write_text(
        "fastapi\nuvicorn\npytest"
    )

    # README
    (project_dir / "README.md").write_text(
        "# Projeto Gerado Automaticamente\n\nAPI FastAPI inicial gerada pelo agente /gerar-codigo."
    )

    return "Código base gerado com sucesso"
