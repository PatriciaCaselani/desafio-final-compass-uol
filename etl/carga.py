import os

import psycopg


def conectar():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="verdejar",
        user="postgres",
        password=os.environ["POSTGRES_PASSWORD"],
    )


def carregar(produtos, clientes, pedidos):
    """Idempotencia: TRUNCATE de todas as tabelas e recarga, na mesma transacao.
    Rodar duas vezes deixa as mesmas contagens."""
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "TRUNCATE itens_pedido, pedidos, clientes, produtos"
            )
            cur.executemany(
                "INSERT INTO produtos (produto_id, nome, categoria, preco_base) "
                "VALUES (%s, %s, %s, %s)",
                [(int(p["produto_id"]), p["nome"], p["categoria"], p["preco_base"])
                 for p in produtos],
            )
            cur.executemany(
                "INSERT INTO clientes (id, nome, email, cidade, estado, cadastro_em) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                [(c["id"], c["nome"], c["email"], c["cidade"], c["estado"],
                  c["cadastro_em"]) for c in clientes],
            )
            cur.executemany(
                "INSERT INTO pedidos (id, cliente_id, data_pedido, status, "
                "valor_total, valor_itens, divergente) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [(p["id"], p["cliente_id"], p["data_pedido"], p["status"],
                  p["valor_total"], p["valor_itens"], p["divergente"])
                 for p in pedidos],
            )
            itens = [
                (p["id"], linha, i["produto_id"], i["quantidade"], i["preco_unitario"])
                for p in pedidos
                for linha, i in enumerate(p["itens"], start=1)
            ]
            cur.executemany(
                "INSERT INTO itens_pedido (pedido_id, linha, produto_id, "
                "quantidade, preco_unitario) VALUES (%s, %s, %s, %s, %s)",
                itens,
            )
            cur.execute("SELECT COUNT(*) FROM itens_pedido")
            total_itens = cur.fetchone()[0]
            cur.execute("SELECT COALESCE(SUM(valor_itens), 0) FROM pedidos")
            soma_destino = float(cur.fetchone()[0])
    return total_itens, soma_destino