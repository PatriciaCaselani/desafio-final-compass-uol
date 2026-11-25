from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


def tratar_cliente(cliente):
    """A1: e-mail ausente vira None (cliente e mantido).
    A2: sigla do estado em maiusculas."""
    novo = dict(cliente)
    email = novo.get("email")
    if email is None or str(email).strip() == "":
        novo["email"] = None
    novo["estado"] = str(novo["estado"]).strip().upper()
    return novo


def converter_data(texto):
    """A3: aceita AAAA-MM-DD e DD/MM/AAAA; devolve AAAA-MM-DD."""
    texto = str(texto).strip()
    if "/" in texto:
        data = datetime.strptime(texto, "%d/%m/%Y")
    else:
        data = datetime.strptime(texto, "%Y-%m-%d")
    return data.date().isoformat()


def converter_valor(valor):
    """A4: aceita numero ou texto com virgula decimal; devolve float com 2 casas."""
    if isinstance(valor, str):
        valor = valor.strip().replace(",", ".")
    return round(float(valor), 2)


def remover_repetidos(pedidos):
    """A5: mantem a primeira ocorrencia de cada id.
    Devolve (lista_sem_repetidos, quantidade_descartada)."""
    vistos = set()
    unicos = []
    for pedido in pedidos:
        if pedido["id"] not in vistos:
            vistos.add(pedido["id"])
            unicos.append(pedido)
    return unicos, len(pedidos) - len(unicos)


def calcular_valor_itens(itens):
    """A6 (parte 1): soma de quantidade x preco_unitario, com 2 casas."""
    total = sum(
        Decimal(str(i["quantidade"])) * Decimal(str(i["preco_unitario"]))
        for i in itens
    )
    return float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def tratar_pedido(pedido):
    """Aplica A3, A4 e A6 a um pedido."""
    novo = dict(pedido)
    novo["data_pedido"] = converter_data(pedido["data_pedido"])
    novo["valor_total"] = converter_valor(pedido["valor_total"])
    novo["valor_itens"] = calcular_valor_itens(pedido["itens"])
    diferenca = round(abs(novo["valor_total"] - novo["valor_itens"]), 2)
    novo["divergente"] = diferenca > 0.01
    return novo