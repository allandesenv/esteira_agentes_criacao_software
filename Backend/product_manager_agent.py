def definir_mvp_agent(discovery_text: str) -> str:
    """
    Product Manager Agent v1
    Define MVP com foco em valor
    """

    return f"""
# Definição de MVP

## Objetivo do MVP
Validar rapidamente se a solução resolve o problema principal identificado no discovery.

---

## Escopo IN (Essencial)
- Cadastro básico
- Operações principais
- Fluxo mínimo funcional

---

## Escopo OUT (Fora do MVP)
- IA avançada
- Relatórios complexos
- Integrações externas

---

## User Stories Essenciais
1. Como usuário, quero executar a operação principal sem erro.
2. Como usuário, quero visualizar o estado atual rapidamente.

---

## Critérios de Sucesso
- Usuário real usando
- Problema principal resolvido
- Feedback claro do cliente

---

## Riscos Aceitos
- Interface simples
- Processos manuais auxiliares

---

Baseado no Discovery:
{discovery_text}
"""
