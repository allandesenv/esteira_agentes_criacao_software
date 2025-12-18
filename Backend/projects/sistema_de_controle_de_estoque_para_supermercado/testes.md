# Estratégia de Testes

## Objetivo
Garantir qualidade mínima, evitar regressões e dar segurança para evolução do produto.

## Tipos de Testes

### 1. Testes Unitários
- Funções puras
- Regras de negócio
- Validações

### 2. Testes de Integração
- Endpoints principais
- Integração com banco de dados
- Fluxos críticos do MVP

### 3. Testes Automatizados Iniciais
- Endpoint /health
- Inicialização da aplicação

## Ferramentas
- pytest
- fastapi.testclient

## Critérios de Aceite
- Cobertura mínima nos fluxos do MVP
- Testes executando automaticamente
- Falha em testes bloqueia avanço

## Riscos
- Falsa sensação de segurança
- Testes frágeis ou excessivos

## Próximos Passos
- Expandir testes conforme features
- Avaliar testes de carga futuramente