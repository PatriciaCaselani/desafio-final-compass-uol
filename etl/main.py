from etl.extracao import extrair_rota, ler_produtos, salvar_json
from etl.transformacao import tratar_cliente, tratar_pedido, remover_repetidos
from etl.carga import carregar


def main():
    clientes, pag_c = extrair_rota("clientes")
    if clientes is None:
        return
    print(f"extracao: clientes paginas={pag_c} registros={len(clientes)}")
    pedidos, pag_p = extrair_rota("pedidos")
    if pedidos is None:
        return
    print(f"extracao: pedidos paginas={pag_p} registros_brutos={len(pedidos)}")
    produtos = ler_produtos()
    salvar_json("clientes.json", clientes)
    salvar_json("pedidos.json", pedidos)
    salvar_json("produtos.json", produtos)

    unicos, descartados = remover_repetidos(pedidos)
    print(f"transformacao: pedidos_unicos={len(unicos)} repetidos_descartados={descartados}")

    emails_nulos = sum(1 for c in clientes if not c.get("email"))
    estados_pad = sum(1 for c in clientes if c["estado"] != c["estado"].upper())
    datas_conv = sum(1 for p in unicos if "/" in str(p["data_pedido"]))
    valores_conv = sum(1 for p in unicos if isinstance(p["valor_total"], str))

    clientes_ok = [tratar_cliente(c) for c in clientes]
    pedidos_ok = [tratar_pedido(p) for p in unicos]
    print(f"transformacao: emails_nulos={emails_nulos} estados_padronizados={estados_pad} "
          f"datas_convertidas={datas_conv} valores_convertidos={valores_conv}")

    total_itens, soma_destino = carregar(produtos, clientes_ok, pedidos_ok)
    print(f"carga: clientes={len(clientes_ok)} produtos={len(produtos)} "
          f"pedidos={len(pedidos_ok)} itens={total_itens}")

    soma_origem = round(sum(p["valor_itens"] for p in pedidos_ok), 2)
    dif = round(abs(soma_origem - soma_destino), 2)
    print(f"reconciliacao: soma_valor_itens_origem={soma_origem:.2f} "
          f"soma_valor_itens_destino={soma_destino:.2f} diferenca={dif:.2f}")
    divergentes = sum(1 for p in pedidos_ok if p["divergente"])
    print(f"divergentes: {divergentes} pedidos com valor_total diferente da soma dos itens")


if __name__ == "__main__":
    main()