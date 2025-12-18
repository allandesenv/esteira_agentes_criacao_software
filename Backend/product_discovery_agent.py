class ProductDiscoveryAgent:
    """
    Product Discovery Agent v2.1
    Discovery ativo com análise de risco e bloqueios.
    """

    def __init__(self, description: str):
        self.description = description.strip()
        self.ambiguities = []
        self.risks = []

    def run(self) -> dict:
        self._analyze_description()

        discovery_text = f"""
# Product Discovery

## 1. Problema percebido
{self.description}

## 2. Contexto do problema
{self._context()}

## 3. Quem sofre o problema
{self._stakeholders()}

## 4. Hipóteses iniciais de valor
{self._value_hypotheses()}

## 5. Riscos identificados
{self._format_list(self.risks)}

## 6. Ambiguidades detectadas
{self._format_list(self.ambiguities)}

## 7. Perguntas críticas obrigatórias
{self._critical_questions()}

## 8. Avaliação de maturidade
**{self._maturity_level()}**

## 9. Status do Discovery
**{self._status()}**

---
Gerado pelo Product Discovery Agent v2.1
""".strip()

        return {
            "document": discovery_text,
            "status": self._status(),
            "blocked": self._is_blocked(),
            "questions": self.ambiguities
        }

    # ------------------------
    # INTELIGÊNCIA INTERNA
    # ------------------------

    def _analyze_description(self):
        if len(self.description) < 80:
            self.ambiguities.append("Descrição muito curta para entendimento real do problema.")

        keywords = ["controle", "sistema", "plataforma", "app"]
        if not any(k in self.description.lower() for k in keywords):
            self.ambiguities.append("Tipo de solução não está claro (sistema, app, processo?).")

        if "usuário" not in self.description.lower():
            self.ambiguities.append("Usuário principal não foi identificado.")

        if "impacto" not in self.description.lower():
            self.risks.append("Impacto do problema não está claro.")

        if "manual" not in self.description.lower():
            self.risks.append("Processo atual não foi descrito.")

    def _context(self) -> str:
        return (
            "- Problema descrito de forma inicial\n"
            "- Requer validação com usuários reais\n"
            "- Pode envolver impacto operacional e financeiro"
        )

    def _stakeholders(self) -> str:
        return (
            "- Usuário final\n"
            "- Operação\n"
            "- Gestão\n"
            "- Time técnico"
        )

    def _value_hypotheses(self) -> str:
        return (
            "- Redução de erro humano\n"
            "- Aumento de visibilidade\n"
            "- Ganho de eficiência\n"
            "- Base para decisões futuras"
        )

    def _critical_questions(self) -> str:
        base_questions = [
            "Quem usa isso todos os dias?",
            "O que acontece se nada for feito?",
            "Como o processo funciona hoje?",
            "Qual métrica define sucesso?"
        ]

        if self.ambiguities:
            base_questions.append("Responder as ambiguidades listadas acima.")

        return self._format_list(base_questions)

    def _maturity_level(self) -> str:
        if self._is_blocked():
            return "Baixa — entendimento insuficiente"
        if len(self.risks) > 1:
            return "Média — riscos conhecidos"
        return "Alta — pronto para avançar"

    def _is_blocked(self) -> bool:
        return len(self.ambiguities) > 0

    def _status(self) -> str:
        return "BLOCKED" if self._is_blocked() else "OK"

    def _format_list(self, items) -> str:
        if not items:
            return "- Nenhum"
        return "\n".join([f"- {item}" for item in items])
