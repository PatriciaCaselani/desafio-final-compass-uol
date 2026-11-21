# desafio-final-compass-uol
Projeto de Engenharia de Dados com ETL completo da API e CSV da Verdejar para PostgreSQL. Inclui limpeza e padronização de dados, validação de integridade, reconciliação, testes automatizados, idempotência e boas práticas de desenvolvimento com Python, SQLite e Pytest.
## Banco de dados
Caminho escolhido: C (pelo menos inicialmente, usar SQLite, modulo sqlite3 da biblioteca padrao).
Motivo: o Docker Desktop apresentou falha no motor (erro 500) e o
servico com.docker.service não pode ser iniciado sem privilegios de
administrador. Optei pelo caminho de contingencia previsto na errata v3... Caso haja tempo, tentarei novamente usar Docker.