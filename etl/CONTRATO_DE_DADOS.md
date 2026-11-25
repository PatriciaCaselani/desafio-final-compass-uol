# Contrato de dados (ETL Verdejar)

Banco: PostgreSQL 16 em contêiner Docker. Esquema: insumos/schema.sql.

## clientes
| Campo | Tipo | Nulo? | Regra de transformação |
|---|---|---|---|
| id | INTEGER (PK) | Não | Vem da API sem alteração |
| nome | TEXT | Não | Sem alteração |
| email | TEXT | Sim | A1: ausente ou vazio vira NULL; o cliente é mantido; contamos quantos |
| cidade | TEXT | Não | Sem alteração |
| estado | CHAR(2) | Não | A2: sempre em maiúsculas (rs vira RS) |
| cadastro_em | DATE | Não | Vem em AAAA-MM-DD |

## produtos
| Campo | Tipo | Nulo? | Regra |
|---|---|---|---|
| produto_id | INTEGER (PK) | Não | Lido do produtos.csv |
| nome | TEXT | Não | Sem alteração |
| categoria | TEXT | Não | Sem alteração |
| preco_base | NUMERIC(10,2) | Não | Texto do CSV convertido para número |

## pedidos
| Campo | Tipo | Nulo? | Regra |
|---|---|---|---|
| id | INTEGER (PK) | Não | A5: pedidos repetidos são removidos pelo id, mantendo a primeira ocorrência |
| cliente_id | INTEGER (FK clientes.id) | Não | Sem alteração |
| data_pedido | DATE | Não | A3: aceita AAAA-MM-DD e DD/MM/AAAA; grava como DATE |
| status | TEXT | Não | Sem alteração |
| valor_total | NUMERIC(12,2) | Não | A4: número ou texto com vírgula decimal vira número com 2 casas |
| valor_itens | NUMERIC(12,2) | Não | Calculado: soma de quantidade x preco_unitario dos itens |
| divergente | BOOLEAN | Não | A6: verdadeiro se |valor_total - valor_itens| > 0,01 |

## itens_pedido
| Campo | Tipo | Nulo? | Regra |
|---|---|---|---|
| pedido_id | INTEGER (PK, FK pedidos.id) | Não | Id do pedido pai |
| linha | INTEGER (PK) | Não | A API não fornece. Usamos a posição do item no pedido, começando em 1 |
| produto_id | INTEGER (FK produtos.produto_id) | Não | Sem alteração |
| quantidade | INTEGER | Não | Sem alteração |
| preco_unitario | NUMERIC(10,2) | Não | Sem alteração |