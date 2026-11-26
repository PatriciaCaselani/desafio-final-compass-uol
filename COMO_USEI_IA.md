# Como usei IA

Ferramentas: Claude (Anthropic) e Gemini, em chat. Papel: par com escopo limitado.
Eu defino o escopo, a IA propõe funções e testes, e eu executo, depuro e corrijo.
Os dados são sintéticos. Por descuido, colei senhas de teste do banco local
(contêiner sem dados reais) em conversas com a IA e também no README.md (linha 3), o que o desafio pede para
evitar. Troquei a senha do banco depois (para ter certeza) e a mantenho só em variável de ambiente.

## Sugestões aceitas

### 1. Função extrair_rota (paginação)
- Pedi: função que percorre todas as páginas da API até total_pages, checando o status HTTP.
- Proposta: laço while com requests.get, page_size=200, try/except para conexão e 404.
- Decisão: aceitei. Atende ao item 1 da Parte 1 e eu consigo explicar cada linha.
- Validação: clientes=1000 em 5 páginas, pedidos=5100 em 26 páginas; com a API desligada, apareceu a mensagem de erro e o programa não quebrou.

### 2. Decimal em calcular_valor_itens
- Pedi: cálculo de valor_itens (soma de quantidade x preço).
- Proposta: usar Decimal com arredondamento ROUND_HALF_UP em vez de float.
- Decisão: aceitei, porque somar float pode gerar diferenças de centavos, que atrapalhariam a reconciliação.
- Validação: reconciliação com diferença 0.00 (origem 311228.75 = destino 311228.75) e teste A6.

## Sugestões rejeitadas

### 1. Trocar para SQLite (caminho C) em vez de Docker
- Contexto: depois das falhas do Docker, a IA recomendou abandonar o Docker e usar SQLite por ser mais seguro dentro do prazo.
- Decisão: rejeitei e insisti no Docker. Eu quis o caminho recomendado pelo ambiente de produção (PostgreSQL), pelo menos inicialmente, devido a corrida contra o tempo e o fato de dizer no desafio que o Docker é opcional, pois eu já havia perdido uma quantidade bem considerável de tempo em função dele.
- O que fiz: reinstalei o Docker Desktop (v4.100.1), confirmei com docker ps que o verdejar-pg estava Up.
- Validação: ETL rodou duas vezes com contagens idênticas no PostgreSQL.

### 2. Aceitar sem prova que os cards 0.1, 0.2 e 0.4 estavam concluídos (resposta do Gemini)
- Contexto: o Gemini disse que três cards estavam concluídos, sem evidência.
- Decisão: rejeitei a afirmação e conferi eu mesma com git status, git log, dir e docker --version.
- Resultado: descobri que havia duas cópias do repositório e que eu estava na pasta/branch errada.

## Falhas e retrabalho

### 1. Instrução da IA apagou arquivos meus
- A IA tratou como "duplicatas" os arquivos dentro de insumos_verdejar e orientou rmdir /s /q. Eram os originais do projeto (.gitignore, COMO_USEI_IA.md, README.md, etl, tests).
- Como descobri: git status mostrou "deleted" nos arquivos.
- Retrabalho: git restore recuperou tudo, pois estava commitado. Aprendi a rodar dir e conferir antes de qualquer apagamento e a fazer commits pequenos.

### 2. Erros de nomes de arquivo e ambiente
- pytest com collected 0 items: arquivos nomeados teste_*.py em vez de test_*.py e conftest.txt em vez de conftest.py (erro de import "No module named etl"). Corrigi com Rename-Item.
- KeyError POSTGRES_PASSWORD: a variável de ambiente só vale no terminal onde foi definida. Passei a definir no mesmo terminal do ETL.
- Comandos de PowerShell executados no CMD e docker run quebrado em duas linhas.