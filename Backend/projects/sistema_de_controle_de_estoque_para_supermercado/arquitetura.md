
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

# Product Discovery

## Problema percebido
Sistema de controle de estoque para supermercado

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


## MVP

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

# Product Discovery

## Problema percebido
Sistema de controle de estoque para supermercado

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


