# Orchestrator v0.4
# Backend mínimo com Discovery + MVP + Software Architect Agent

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from datetime import datetime
from agent_gerar_codigo import gerar_codigo
from agent_revisar_codigo import revisar_codigo
from agent_testes import definir_estrategia_testes
from agent_deploy import preparar_deploy
from agent_release import preparar_release
import os

app = FastAPI(title="AI Orchestrator v0.4")

BASE_DIR = "projects"
os.makedirs(BASE_DIR, exist_ok=True)

# -----------------------------
# Product Discovery Agent
# -----------------------------

def product_discovery_agent(description: str) -> str:
    return f"""
# Product Discovery

## Problema percebido
{description}

## Quem sofre o problema
- Usuários finais
- Operação do negócio

## Perguntas-chave
- Quem usará o sistema diariamente?
- Qual impacto se o problema NÃO for resolvido?
- Existe solução manual hoje?
- Qual urgência real?

## Riscos iniciais
- Expectativa inflada
- Falta de clareza do escopo

## Hipóteses de valor
- Resolver uma dor principal antes de expandir
- MVP simples pode gerar a maior parte do valor
"""

# -----------------------------
# Product Manager Agent (MVP)
# -----------------------------

def definir_mvp_agent(discovery_text: str) -> str:
    return f"""
# Definição de MVP

## Objetivo do MVP
Validar rapidamente se a solução resolve o problema principal de controle de estoque.

## Escopo do MVP (IN)
- Cadastro de produtos
- Controle de entrada e saída
- Definição de estoque mínimo
- Alerta simples de reposição

## Fora do MVP (OUT)
- Previsão com IA
- Relatórios avançados
- Aplicativo mobile
- Integração com ERP

## User Stories principais
1. Como operador, quero cadastrar produtos para controlar o estoque.
2. Como operador, quero registrar entradas e saídas para manter saldo correto.
3. Como operador, quero ser alertado quando o estoque estiver baixo.

## Critérios de sucesso
- Produto cadastrado em menos de 2 minutos
- Alerta funcionando em produção
- Uso diário pelo cliente

## Riscos aceitos
- Interface simples
- Processos manuais iniciais

---

Baseado no discovery:
{discovery_text}
"""

# -----------------------------
# Software Architect Agent
# -----------------------------

def arquitetura_agent(discovery_text: str, mvp_text: str) -> str:
    return f"""
# Arquitetura de Software

## Objetivo arquitetural
Entregar o MVP com simplicidade, baixo custo e facilidade de evolução.

## Estilo arquitetural
- Monólito modular
- Separação por camadas
- Preparado para evolução futura

## Stack sugerida
- Backend: Java 21 + Spring Boot
- Banco de dados: PostgreSQL
- API: REST
- Infraestrutura: Docker

## Estrutura de pastas sugerida
- domain
- application
- infrastructure
- interfaces

## Decisões arquiteturais (ADR)
1. Não utilizar microsserviços no MVP
2. Não utilizar mensageria no MVP
3. Priorizar legibilidade e simplicidade

## Riscos técnicos aceitos
- Escalabilidade limitada inicialmente
- Deploy manual no início

---

Referências:

## Discovery
{discovery_text}

## MVP
{mvp_text}
"""

# -----------------------------
# Slack Commands Endpoint
# -----------------------------

@app.post("/slack/commands")
async def slack_commands(
    command: str = Form(...),
    text: str = Form(""),
    user_name: str = Form("unknown")
):
    timestamp = datetime.utcnow().isoformat()

    if command == "/novo-produto":
        project_name = text.replace(" ", "_").lower() or "projeto_sem_nome"
        project_path = os.path.join(BASE_DIR, project_name)
        os.makedirs(project_path, exist_ok=True)

        discovery_output = product_discovery_agent(text)

        with open(os.path.join(project_path, "discovery.md"), "w", encoding="utf-8") as f:
            f.write(discovery_output)

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"Discovery criado para o projeto: {project_name}."
        })

    if command == "/definir-mvp":
        project_name = text.replace(" ", "_").lower()
        project_path = os.path.join(BASE_DIR, project_name)
        discovery_file = os.path.join(project_path, "discovery.md")

        if not os.path.exists(discovery_file):
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Discovery não encontrado. Execute /novo-produto primeiro."
            })

        with open(discovery_file, "r", encoding="utf-8") as f:
            discovery_text = f.read()

        mvp_output = definir_mvp_agent(discovery_text)

        with open(os.path.join(project_path, "mvp.md"), "w", encoding="utf-8") as f:
            f.write(mvp_output)

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"MVP definido com sucesso para o projeto: {project_name}."
        })
    
    if command == "/gerar-codigo":
        result = gerar_codigo(text)
        return {"text": result}
    
    if command == "/revisar-codigo":
        result = revisar_codigo(text)
        return {"text": result}
    
    if command == "/testes":
        result = definir_estrategia_testes(text)
        return {"text": result}
    
    if command == "/deploy":
        result = preparar_deploy(text)
        return {"text": result}
    
    if command == "/release":
        result = preparar_release(text)
        return {"text": result}

    if command == "/arquitetura":
        project_name = text.replace(" ", "_").lower()
        project_path = os.path.join(BASE_DIR, project_name)
        discovery_file = os.path.join(project_path, "discovery.md")
        mvp_file = os.path.join(project_path, "mvp.md")

        if not os.path.exists(discovery_file) or not os.path.exists(mvp_file):
            return JSONResponse({
                "response_type": "ephemeral",
                "text": "Discovery ou MVP não encontrado. Execute as etapas anteriores."
            })

        with open(discovery_file, "r", encoding="utf-8") as f:
            discovery_text = f.read()

        with open(mvp_file, "r", encoding="utf-8") as f:
            mvp_text = f.read()

        arquitetura_output = arquitetura_agent(discovery_text, mvp_text)

        with open(os.path.join(project_path, "arquitetura.md"), "w", encoding="utf-8") as f:
            f.write(arquitetura_output)

        return JSONResponse({
            "response_type": "in_channel",
            "text": f"Arquitetura definida para o projeto: {project_name}."
        })

    return JSONResponse({
        "response_type": "ephemeral",
        "text": "Comando não reconhecido."
    })

@app.get("/health")
def health():
    return {"status": "ok"}
