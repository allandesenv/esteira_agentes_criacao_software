# Orchestrator v0.6
# Orquestrador com Architect Agent v1.3 (contexto + geração consciente)

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path

# Agentes técnicos
from agent_gerar_codigo import gerar_codigo
from agent_revisar_codigo import revisar_codigo
from agent_testes import definir_estrategia_testes
from agent_deploy import preparar_deploy
from agent_release import preparar_release

# Agentes de produto
from product_discovery_agent import ProductDiscoveryAgent
from product_manager_agent import definir_mvp_agent

# Agente de arquitetura
from architect_agent_v_1 import ContextBuilder, ArchitectAgent

app = FastAPI(title="AI Orchestrator v0.6")

BASE_DIR = Path("projects")
BASE_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# LLM CALL (placeholder)
# --------------------------------------------------

def fake_llm_call(prompt: str) -> str:
    """
    Placeholder de LLM.
    Futuro: OpenAI / Azure / Ollama / Local LLM
    """
    return prompt

# --------------------------------------------------
# Slack Commands Endpoint
# --------------------------------------------------

@app.post("/slack/commands")
async def slack_commands(
    command: str = Form(...),
    text: str = Form(""),
    user_name: str = Form("unknown")
):
    timestamp = datetime.utcnow().isoformat()

    # ---------------- NOVO PRODUTO ----------------
    if command == "/novo-produto":

        if not text:
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Descreva o produto após o comando."
            })

        project_name = text.replace(" ", "_").lower()
        project_path = BASE_DIR / project_name

        #  Garante que o diretório existe
        project_path.mkdir(parents=True, exist_ok=True)

        agent = ProductDiscoveryAgent(text)
        result = agent.run()

        (project_path / "discovery.md").write_text(
            result["document"], encoding="utf-8"
        )

        if result["blocked"]:
            return JSONResponse({
                "response_type": "ephemeral",
                "text": (
                    "Discovery criado, mas BLOQUEADO\n\n"
                    "Perguntas pendentes:\n- " +
                    "\n- ".join(result["questions"])
                )
            })

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"Discovery criado e aprovado para o projeto: {project_name}"
        })

    # ---------------- DEFINIR MVP ----------------
    if command == "/definir-mvp":
        project_name = text.replace(" ", "_").lower()
        project_path = BASE_DIR / project_name
        discovery_file = project_path / "discovery.md"

        if not discovery_file.exists():
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Discovery não encontrado. Execute /novo-produto primeiro."
            })

        discovery_text = discovery_file.read_text(encoding="utf-8")
        mvp_output = definir_mvp_agent(discovery_text)
        (project_path / "mvp.md").write_text(mvp_output, encoding="utf-8")

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"MVP definido com sucesso para o projeto: {project_name}."
        })

    # ---------------- ARQUITETURA (AGENTE REAL) ----------------
    if command == "/arquitetura":
        project_name = text.replace(" ", "_").lower()
        project_path = BASE_DIR / project_name

        if not project_path.exists():
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Projeto não encontrado."
            })

        context = ContextBuilder(project_name).build()

        if not context.get("discovery") or not context.get("mvp"):
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Discovery ou MVP não encontrado. Execute as etapas anteriores."
            })

        agent = ArchitectAgent(context)
        architecture_output = agent.generate_architecture(fake_llm_call)

        (project_path / "arquitetura.md").write_text(
            architecture_output,
            encoding="utf-8"
        )

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"Arquitetura definida com sucesso para o projeto: {project_name}."
        })

    # ---------------- PIPELINE TÉCNICA ----------------
    if command == "/gerar-codigo":
        return {"text": gerar_codigo(text)}

    if command == "/revisar-codigo":
        return {"text": revisar_codigo(text)}

    if command == "/testes":
        return {"text": definir_estrategia_testes(text)}

    if command == "/deploy":
        return {"text": preparar_deploy(text)}

    if command == "/release":
        return {"text": preparar_release(text)}

    return JSONResponse({
        "response_type": "ephemeral",
        "text": "Comando não reconhecido."
    })


@app.get("/health")
def health():
    return {"status": "ok"}
