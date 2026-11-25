import json

from etl.carga import conectar
from etl.transformacao import remover_repetidos, tratar_pedido


def _origem():
    with open("brutos/pedidos.json", encoding="utf-8") as f:
        bruto = json.load(f)
    unicos, _ = remover_repetidos(bruto)
    return [tratar_pedido(p) for p in unicos]


def test_reconciliacao_contagem_e_soma():
    origem = _origem()
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*), COALESCE(SUM(valor_itens), 0) FROM pedidos")
        qtd, soma = cur.fetchone()
    assert qtd == len(origem)
    assert abs(float(soma) - sum(p["valor_itens"] for p in origem)) <= 0.01


def test_consulta_vendas_por_mes_soma_igual_ao_total():
    with conectar() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT COALESCE(SUM(t), 0) FROM ("
            "SELECT SUM(valor_total) AS t FROM pedidos "
            "GROUP BY DATE_TRUNC('month', data_pedido)) m"
        )
        soma_meses = float(cur.fetchone()[0])
        cur.execute("SELECT COALESCE(SUM(valor_total), 0) FROM pedidos")
        soma_geral = float(cur.fetchone()[0])
    assert abs(soma_meses - soma_geral) <= 0.01