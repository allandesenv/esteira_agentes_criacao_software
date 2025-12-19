import os
import subprocess
from ai_service import AIService
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from jinja2 import Environment, FileSystemLoader

# Imports dos nossos novos módulos
from utils.logger import setup_logger
from utils.git_manager import GitManager

# --- Configuração Inicial ---
app = FastAPI(title="AI Orchestrator v0.5 - Robust Mode")
logger = setup_logger()

BASE_DIR = Path("projects")
BASE_DIR.mkdir(exist_ok=True)

# Configuração do Jinja2 (Templates)
TEMPLATES_DIR = Path("templates")
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

ai_brain = AIService()

# --- Funções Auxiliares de Renderização ---

def render_template(template_name: str, context: dict) -> str:
    """Renderiza um template Jinja2 com o contexto fornecido."""
    try:
        template = env.get_template(template_name)
        return template.render(**context)
    except Exception as e:
        logger.error(f"Erro ao renderizar template {template_name}: {e}")
        return f"Erro na geração do artefato: {e}"

# --- Endpoints ---

@app.post("/slack/commands")
async def slack_commands(
    command: str = Form(...),
    text: str = Form(""),
    user_name: str = Form("unknown")
):
    try:
        # ---------------------------------------------------------
        # 1. Extração e Definição do Nome do Projeto (CORREÇÃO AQUI)
        # ---------------------------------------------------------
        # Tenta pegar o primeiro nome do texto como nome do projeto
        # Ex: "/novo-produto SistemaEstoque" -> project_name = "sistemaestoque"
        if " " in text:
            raw_project_name = text.split(" ")[0]
            description = text # Mantém o texto todo como descrição
        else:
            raw_project_name = text if text else "projeto_sem_nome"
            description = text

        project_name = raw_project_name.replace(" ", "_").lower()
        project_path = BASE_DIR / project_name
        project_path.mkdir(exist_ok=True)

        # Inicializa o Git Manager para este caminho
        git_mgr = GitManager(project_path)

        # ---------------------------------------------------------
        # 2. Lógica dos Comandos
        # ---------------------------------------------------------
        if command == "/novo-produto":
            logger.info(f"Acionando IA para Discovery do projeto: {project_name}")
            
            # 1. IA Gera o Conteúdo (Dicionário)
            discovery_data = ai_brain.generate_discovery(description)
            
            # Adicionamos dados de infra ao dicionário da IA
            discovery_data["project_name"] = project_name
            discovery_data["date"] = datetime.now().strftime("%Y-%m-%d")

            # 2. Jinja2 Renderiza o Arquivo
            content = render_template("discovery.md.j2", discovery_data)
            
            # 3. Salvar e Checkpoint
            (project_path / "discovery.md").write_text(content, encoding="utf-8")
            git_mgr.checkpoint("Agente Discovery (IA): Criou discovery.md detalhado")

            return JSONResponse({
                "response_type": "in_channel",
                "text": f"Discovery Inteligente criado para: *{project_name}*.\nIA analisou Personas, Riscos e Perguntas."
            })

        elif command == "/definir-mvp":
            discovery_file = project_path / "discovery.md"
            if not discovery_file.exists():
                return {"text": "Erro: Discovery não encontrado."}

            discovery_content = discovery_file.read_text(encoding="utf-8")
            
            logger.info(f"Acionando IA para Definição de MVP: {project_name}")

            # 1. IA lê o Discovery e Gera o MVP (User Stories, Escopo)
            mvp_data = ai_brain.generate_mvp(discovery_content)
            
            # Adicionamos contexto extra
            mvp_data["project_name"] = project_name
            mvp_data["discovery_summary"] = discovery_content[:300] + "..."

            # 2. Renderiza
            content = render_template("mvp.md.j2", mvp_data)

            # 3. Salvar e Checkpoint
            (project_path / "mvp.md").write_text(content, encoding="utf-8")
            git_mgr.checkpoint(f"Agente Produto (IA): MVP definido com {len(mvp_data['user_stories'])} User Stories")

            return {"text": f"MVP Inteligente definido para: *{project_name}*."}
        # --- COMANDO REINSERIDO E ATUALIZADO ---
        elif command == "/arquitetura":
            discovery_file = project_path / "discovery.md"
            mvp_file = project_path / "mvp.md"

            # Validação: Regra de Ouro "Nenhuma etapa crítica roda sem artefato anterior"
            if not discovery_file.exists() or not mvp_file.exists():
                return {"text": "Erro: Discovery ou MVP ausentes. Siga a ordem da esteira."}

            # Leitura dos Contextos
            discovery_text = discovery_file.read_text(encoding="utf-8")
            mvp_text = mvp_file.read_text(encoding="utf-8")

            # Geração via Template
            content = render_template("arquitetura.md.j2", {
                "project_name": project_name,
                "discovery_context": discovery_text[:500] + "...", # Passa um resumo para o documento
                "mvp_context": mvp_text[:500] + "..."
            })

            # Salvar Artefato
            (project_path / "arquitetura.md").write_text(content, encoding="utf-8")

            # Versionamento Automático
            git_mgr.checkpoint("Agente Arquiteto: Definiu arquitetura.md e Stack Tecnológica")

            return JSONResponse({
                "response_type": "in_channel",
                "text": f"Arquitetura definida para: *{project_name}*.\nArquivo `arquitetura.md` gerado."
            })
        # ---------------------------------------

        elif command == "/gerar-codigo":
            # 1. Validação de Dependência
            if not (project_path / "arquitetura.md").exists():
                return {"text": "Erro: Arquitetura não definida. Execute /arquitetura primeiro."}

            logger.info(f"🏗️ Iniciando scaffolding para: {project_name}")

            # 2. Definição da Estrutura de Pastas (Baseado no Arquitetura.md)
            dirs_to_create = [
                project_path / "app",
                project_path / "app" / "api",
                project_path / "app" / "core",
                project_path / "app" / "domain",
                project_path / "tests"
            ]

            for d in dirs_to_create:
                d.mkdir(parents=True, exist_ok=True)
                # Cria __init__.py para tornar pacote Python
                (d / "__init__.py").touch()

            # 3. Renderização e Criação dos Arquivos
            files_map = {
                "main.py.j2": project_path / "app" / "main.py",
                "requirements.txt.j2": project_path / "requirements.txt",
                "test_health.py.j2": project_path / "tests" / "test_health.py",
                "README_TECNICO.md.j2": project_path / "README.md"
            }

            for template_name, file_path in files_map.items():
                content = render_template(template_name, {"project_name": project_name})
                file_path.write_text(content, encoding="utf-8")

            # 4. Checkpoint
            git_mgr.checkpoint("Agente Dev: Scaffolding completo (App, Tests, Configs)")

            return JSONResponse({
                "response_type": "in_channel",
                "text": f"Código base gerado para: *{project_name}*.\nEstrutura de pastas criada conforme Arquitetura."
            })

        elif command == "/revisar-codigo":
            logger.info(f"Iniciando revisão de código para: {project_name}")

            # -------------------------------------------
            # 1. Verificação Estrutural (Arquivos)
            # -------------------------------------------
            expected_files = [
                "app/main.py",
                "app/core",
                "requirements.txt",
                "Dockerfile",
                "README.md"
            ]
            
            structure_results = []
            all_files_exist = True
            
            for file_rel_path in expected_files:
                full_path = project_path / file_rel_path
                exists = full_path.exists()
                structure_results.append({
                    "file": file_rel_path,
                    "exists": exists
                })
                if not exists:
                    all_files_exist = False

            # -------------------------------------------
            # 2. Análise Estática (Ruff)
            # -------------------------------------------
            linter_output = ""
            linter_success = True
            total_issues = 0

            try:
                # Executa o Ruff apenas no diretório do projeto
                result = subprocess.run(
                    ["ruff", "check", str(project_path), "--output-format=text"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    linter_success = False
                    linter_output = result.stdout
                    # Conta linhas não vazias como aproximação de erros
                    total_issues = len([l for l in linter_output.split('\n') if l.strip()])
                
            except FileNotFoundError:
                linter_output = "ERRO: Ferramenta 'ruff' não instalada. Execute 'pip install ruff'."
                linter_success = False
                total_issues = 1

            # -------------------------------------------
            # 3. Compilar Dados e Renderizar
            # -------------------------------------------
            overall_success = all_files_exist and linter_success
            
            # Contagem de arquivos Python para estatística
            py_files_count = len(list(project_path.glob("**/*.py")))

            review_data = {
                "project_name": project_name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "success": overall_success,
                "total_files": py_files_count,
                "total_issues": total_issues,
                "structure_checks": structure_results,
                "linter_issues": not linter_success,
                "linter_output": linter_output.strip()
            }

            content = render_template("review.md.j2", review_data)
            
            # Salvar Relatório
            report_path = project_path / "review.md"
            report_path.write_text(content, encoding="utf-8")

            # Checkpoint Git
            status_msg = "Aprovado" if overall_success else "Com Apontamentos"
            git_mgr.checkpoint(f"Agente Reviewer: Relatório gerado ({status_msg})")

            return JSONResponse({
                "response_type": "in_channel",
                "text": f"Revisão concluída para *{project_name}*.\nStatus: *{'Aprovado' if overall_success else 'Atenção'}*\nRelatório salvo em `review.md`."
            })
        
        elif command == "/testes":
            mvp_file = project_path / "mvp.md"
            if not mvp_file.exists():
                return {"text": "Erro: MVP não encontrado."}
            
            mvp_text = mvp_file.read_text(encoding="utf-8")
            
            content = render_template("testes.md.j2", {
                "project_name": project_name,
                "mvp_summary": mvp_text[:300] + "..."
            })
            
            (project_path / "testes.md").write_text(content, encoding="utf-8")
            git_mgr.checkpoint("Agente QA: Definiu estratégia de testes")
            
            return {"text": f"Estratégia de testes definida para: *{project_name}*."}

        elif command == "/deploy":
            # Gera Dockerfile
            dockerfile_content = render_template("Dockerfile.j2", {"project_name": project_name})
            (project_path / "Dockerfile").write_text(dockerfile_content, encoding="utf-8")
            
            # Gera docker-compose.yml
            compose_content = render_template("docker-compose.yml.j2", {"project_name": project_name})
            (project_path / "docker-compose.yml").write_text(compose_content, encoding="utf-8")
            
            git_mgr.checkpoint("Agente DevOps: Configuração Docker gerada")
            
            return {"text": f"Arquivos de Deploy (Docker) gerados para: *{project_name}*."}

        elif command == "/release":
            mvp_file = project_path / "mvp.md"
            mvp_text = mvp_file.read_text(encoding="utf-8") if mvp_file.exists() else "MVP não localizado."
            
            content = render_template("release.md.j2", {
                "project_name": project_name,
                "version": "0.1.0-mvp",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "mvp_summary": mvp_text[:200] + "..."
            })
            
            (project_path / "release.md").write_text(content, encoding="utf-8")
            git_mgr.checkpoint("Agente Release: Release 0.1.0 preparada")
            
            return {"text": f"Release Note gerado com sucesso!"}

        return {"text": "Comando não reconhecido."}

    except Exception as e:
        logger.error(f"Erro processando comando: {e}")
        return {"text": f"Erro interno: {str(e)}"}

@app.get("/health")
def health():
    return {"status": "ok", "mode": "robust-no-ia"}