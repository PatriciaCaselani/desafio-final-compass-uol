# ETL Verdejar: da API ao PostgreSQL

## Como rodar
1. Ambiente: `python -m venv .venv`, ativar, `pip install -r requirements.txt`
2. API (terminal separado): `python insumos\api_verdejar.py --dados insumos\dados`
3. Banco: `docker run --name verdejar-pg -e POSTGRES_PASSWORD=<sua_senha> -e POSTGRES_DB=verdejar -p 5432:5432 -d postgres:16`
   e depois `Get-Content insumos\schema.sql -Raw | docker exec -i verdejar-pg psql -U postgres -d verdejar`
4. Senha, em variável de ambiente (nada é versionado): `$env:POSTGRES_PASSWORD="<sua_senha>"`
5. ETL: `python -m etl.main`
6. Testes: `pytest` (com o contêiner ligado e a variável definida)

## Banco de dados
Caminho B (PostgreSQL 16 em Docker). Biblioteca de conexão: psycopg 3
(`pip install "psycopg[binary]"`).
Durante o desenvolvimento o Docker Desktop apresentou falhas (erro 500 no motor e
`docker.exe` não encontrado no PATH). Cheguei a preparar o caminho C (SQLite,
`schema_sqlite.sql`) como contingência, mas reinstalei o Docker Desktop e voltei
ao caminho B. O ETL em Python não muda entre os caminhos.

## Estratégia de idempotência
TRUNCATE das quatro tabelas seguido da recarga, na mesma transação. Se algo
falhar no meio, nada é gravado pela metade; rodar duas vezes deixa as mesmas contagens.

## Saída do ETL (duas execuções seguidas, mesmas contagens)
```
extracao: clientes paginas=5 registros=1000
extracao: pedidos paginas=26 registros_brutos=5100
transformacao: pedidos_unicos=5000 repetidos_descartados=100
transformacao: emails_nulos=81 estados_padronizados=151 datas_convertidas=1037 valores_convertidos=1255
carga: clientes=1000 produtos=12 pedidos=5000 itens=12455
reconciliacao: soma_valor_itens_origem=311228.75 soma_valor_itens_destino=311228.75 diferenca=0.00
divergentes: 238 pedidos com valor_total diferente da soma dos itens
```

## Consultas de validação (consultas_validacao.sql)
(a) Vendas por mês:
```
    mes     | total_vendas
------------+--------------
 2026-01-01 |     30449.02
 2026-02-01 |     33923.86
 2026-03-01 |     30678.70
 2026-04-01 |     31253.96
 2026-05-01 |     30890.02
 2026-06-01 |     31627.73
 2026-07-01 |     32796.17
 2026-08-01 |     29328.04
 2026-09-01 |     29995.71
 2026-10-01 |     31104.54
```
(b) Pedidos por estado (soma 5000):
```
 MG 476 | PR 974 | RS 1543 | SC 1127 | SP 880
```
(c) Pedidos divergentes: 238 linhas.

Teste de consulta: a soma dos meses é igual à soma geral
(`test_consulta_vendas_por_mes_soma_igual_ao_total`, em `tests/test_reconciliacao.py`).

## Saída do pytest
```
8 passed in 1.25s
```

## Documentos
CONTRATO_DE_DADOS.md, COMO_USEI_IA.md.