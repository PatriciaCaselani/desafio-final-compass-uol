\# Como usei IA



Ferramenta de IA utilizada: (preencha o nome e a versão)

Papel adotado: par com escopo limitado. Eu defino o escopo, a IA propõe

funções e testes, e eu executo, depuro e corrijo.



\## Sugestões aceitas



(Para cada item: trecho pedido, o que a IA propôs, justificativa

da decisão e como validei.)



\## Sugestões rejeitadas



(Para cada item: trecho pedido, o que a IA propôs, por que rejeitei,

o que fiz no lugar e como validei.)



\## Falhas e retrabalho



(Para cada item: o que a IA propôs, qual falha encontrei, como

descobri e qual retrabalho fiz.)

# Sugestões aceitas

## Escolha do banco de dados

**Pergunta feita à IA:** Como posso prosseguir com o desafio sem utilizar Docker?

**Sugestão recebida:** Utilizar SQLite como caminho alternativo, conforme permitido na errata do desafio.

**Decisão tomada:** Aceitei a sugestão após verificar a errata do desafio, que informa que o Docker passou a ser opcional e que o caminho C (SQLite) não gera perda de nota.

**Como validei:** Li a errata e confirmei que o desafio passou a aceitar três caminhos para o banco de dados: PostgreSQL local, PostgreSQL em Docker ou SQLite.

**Resultado:** Optei por SQLite para evitar bloqueios relacionados à configuração do Docker e continuar o desenvolvimento do ETL.

### Função extrair_rota (paginação)
- Trecho pedido: função que percorre todas as páginas de uma rota paginada,
  verificando status HTTP.
- O que a IA propôs: laço while até total_pages, com try/except e checagem
  de status_code.
- Justificativa: atende ao item 1 da Parte 1 e eu consigo explicar cada linha.
- Como validei: rodei o script e conferi clientes=1000 em 5 páginas e
  pedidos=5100 em 26 páginas; derrubei a API e vi a mensagem de erro.