from pathlib import Path

PROJECTS_DIR = Path("projects")


def revisar_codigo(project_name: str) -> str:
    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        raise FileNotFoundError("Projeto não encontrado")

    findings = []

    # 1. Estrutura básica
    expected_paths = [
        project_dir / "app" / "main.py",
        project_dir / "requirements.txt",
        project_dir / "tests",
    ]

    for path in expected_paths:
        if not path.exists():
            findings.append(f"FALTA: {path}")

    # 2. Verificar endpoint de health
    main_file = project_dir / "app" / "main.py"
    if main_file.exists():
        content = main_file.read_text()
        if "/health" not in content:
            findings.append("Endpoint /health não encontrado")

    # 3. Dependências mínimas
    req_file = project_dir / "requirements.txt"
    if req_file.exists():
        reqs = req_file.read_text()
        for dep in ["fastapi", "uvicorn", "pytest"]:
            if dep not in reqs:
                findings.append(f"Dependência ausente: {dep}")

    # 4. Testes
    tests_dir = project_dir / "tests"
    if tests_dir.exists():
        if not any(tests_dir.glob("test_*.py")):
            findings.append("Nenhum teste automatizado encontrado")

    # Resultado
    if not findings:
        return "Revisão concluída: código atende aos padrões iniciais"

    report = "REVISÃO DE CÓDIGO – PONTOS DE ATENÇÃO:\n"
    for item in findings:
        report += f"- {item}\n"

    return report