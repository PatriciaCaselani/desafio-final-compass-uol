from etl.transformacao import (
    tratar_cliente, converter_data, converter_valor,
    remover_repetidos, calcular_valor_itens, tratar_pedido,
)


def test_a1_email_nulo_mantem_cliente():
    c = tratar_cliente({"id": 1, "email": None, "estado": "RS"})
    assert c["email"] is None
    assert c["id"] == 1


def test_a2_estado_em_maiusculas():
    assert tratar_cliente({"id": 1, "email": "a@b.com", "estado": "rs"})["estado"] == "RS"


def test_a3_data_nos_dois_formatos():
    assert converter_data("2026-03-05") == "2026-03-05"
    assert converter_data("05/03/2026") == "2026-03-05"


def test_a4_valor_com_virgula_vira_numero():
    assert converter_valor("125,84") == 125.84
    assert converter_valor(94.34) == 94.34


def test_a5_pedido_repetido_e_descartado():
    pedidos = [{"id": 1, "x": "a"}, {"id": 2, "x": "b"}, {"id": 1, "x": "a"}]
    unicos, descartados = remover_repetidos(pedidos)
    assert [p["id"] for p in unicos] == [1, 2]
    assert descartados == 1


def test_a6_valor_itens_e_divergencia():
    itens = [
        {"produto_id": 1, "quantidade": 2, "preco_unitario": 3.50},
        {"produto_id": 2, "quantidade": 1, "preco_unitario": 4.20},
    ]
    assert calcular_valor_itens(itens) == 11.20
    base = {"id": 1, "data_pedido": "2026-01-01", "itens": itens}
    assert tratar_pedido({**base, "valor_total": 11.20})["divergente"] is False
    assert tratar_pedido({**base, "valor_total": 16.20})["divergente"] is True