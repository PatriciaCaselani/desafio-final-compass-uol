import csv
import json
import os
import requests

URL_BASE = "http://127.0.0.1:8000"
PAGE_SIZE = 200


def extrair_rota(rota, page_size=PAGE_SIZE):
    """Percorre todas as paginas de uma rota da API.
    Devolve (lista_de_registros, total_de_paginas).
    Em caso de erro, imprime uma mensagem e devolve (None, 0)."""
    registros = []
    pagina = 1
    total_paginas = 1  # valor inicial; sera atualizado pela resposta da API

    while pagina <= total_paginas:
        try:
            resposta = requests.get(
                f"{URL_BASE}/{rota}",
                params={"page": pagina, "page_size": page_size},
                timeout=10,
            )
        except requests.exceptions.ConnectionError:
            print(f"erro: nao foi possivel conectar a API em {URL_BASE}. Ela esta rodando?")
            return None, 0
        except requests.exceptions.RequestException as erro:
            print(f"erro: falha na requisicao de {rota}: {erro}")
            return None, 0

        if resposta.status_code == 404:
            print(f"erro: pagina {pagina} de {rota} nao existe (404)")
            return None, 0
        if resposta.status_code != 200:
            print(f"erro: {rota} pagina {pagina} devolveu status {resposta.status_code}")
            return None, 0

        dados = resposta.json()
        registros.extend(dados["items"])
        total_paginas = dados["total_pages"]
        pagina += 1

    return registros, total_paginas


def salvar_json(nome_arquivo, dados):
    os.makedirs("brutos", exist_ok=True)
    caminho = os.path.join("brutos", nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)


def ler_produtos(caminho="insumos/dados/produtos.csv"):
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    clientes, pag_clientes = extrair_rota("clientes")
    if clientes is None:
        return
    print(f"extracao: clientes paginas={pag_clientes} registros={len(clientes)}")

    pedidos, pag_pedidos = extrair_rota("pedidos")
    if pedidos is None:
        return
    print(f"extracao: pedidos paginas={pag_pedidos} registros_brutos={len(pedidos)}")

    produtos = ler_produtos()
    print(f"extracao: produtos registros={len(produtos)}")

    salvar_json("clientes.json", clientes)
    salvar_json("pedidos.json", pedidos)
    salvar_json("produtos.json", produtos)


if __name__ == "__main__":
    main()