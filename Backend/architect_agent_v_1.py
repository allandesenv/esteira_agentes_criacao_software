from pathlib import Path

class ContextBuilder:
    """
    Responsável por montar o contexto do projeto
    a partir dos artefatos existentes.
    """

    def __init__(self, project_name: str, base_dir: str = "projects"):
        self.project_path = Path(base_dir) / project_name

    def build(self) -> dict:
        context = {}

        discovery_file = self.project_path / "discovery.md"
        mvp_file = self.project_path / "mvp.md"

        if discovery_file.exists():
            context["discovery"] = discovery_file.read_text(encoding="utf-8")

        if mvp_file.exists():
            context["mvp"] = mvp_file.read_text(encoding="utf-8")

        return context

class ArchitectAgent:
    """
    Architect Agent v1.3
    Agente de decisão arquitetural consciente
    """

    def __init__(self, context: dict):
        self.context = context

    def generate_architecture(self, llm_call=None) -> str:
        maturity = self._assess_maturity()
        style = self._choose_architecture(maturity)

        architecture = f"""
# Arquitetura do Sistema

## Visão Geral
Arquitetura definida com base na maturidade **{maturity}** do produto.

## Estilo Arquitetural
**{style}**

## Justificativa
{self._justify(maturity, style)}

## Componentes Principais
{self._components(style)}

## Estratégia de Dados
{self._data_strategy(style)}

## Requisitos Não Funcionais
{self._nfrs(maturity)}

## Caminho de Evolução
{self._evolution_path(style)}
"""

        # 🔮 Futuro: LLM melhora a redação
        if llm_call:
            architecture = llm_call(architecture)

        return architecture.strip()

    # ------------------------
    # INTELIGÊNCIA INTERNA
    # ------------------------

    def _assess_maturity(self) -> str:
        discovery = self.context.get("discovery", "")
        mvp = self.context.get("mvp", "")

        if len(discovery) < 300 or len(mvp) < 300:
            return "baixa"
        if "critério" in mvp.lower() or "história" in mvp.lower():
            return "media"
        return "alta"

    def _choose_architecture(self, maturity: str) -> str:
        return {
            "baixa": "Monolito Modular",
            "media": "Monolito Modular com camadas bem definidas",
            "alta": "Microsserviços orientados a domínio"
        }[maturity]

    def _components(self, style: str) -> str:
        components = [
            "- API REST",
            "- Camada de Aplicação",
            "- Camada de Domínio",
            "- Infraestrutura"
        ]
        if "Micro" in style:
            components.append("- API Gateway")
            components.append("- Mensageria")
        return "\n".join(components)

    def _data_strategy(self, style: str) -> str:
        if "Micro" in style:
            return "- Banco por serviço\n- Consistência eventual\n- Event-driven"
        return "- Banco único\n- Consistência forte"

    def _nfrs(self, maturity: str) -> str:
        base = ["- Segurança", "- Observabilidade"]
        if maturity != "baixa":
            base += ["- Escalabilidade", "- Resiliência"]
        return "\n".join(base)

    def _evolution_path(self, style: str) -> str:
        if "Monolito" in style:
            return (
                "- Modularizar por domínio\n"
                "- Isolar contextos\n"
                "- Extrair serviços conforme necessidade"
            )
        return (
            "- Governança de contratos\n"
            "- Observabilidade distribuída\n"
            "- Gestão de custo por serviço"
        )

    def _justify(self, maturity: str, style: str) -> str:
        return (
            f"O estilo **{style}** foi escolhido para equilibrar velocidade, "
            f"custo e risco técnico considerando a maturidade atual do produto."
        )
