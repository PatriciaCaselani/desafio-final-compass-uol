-- (a) total de vendas por mes
SELECT DATE_TRUNC('month', data_pedido)::date AS mes,
       SUM(valor_total) AS total_vendas
FROM pedidos
GROUP BY 1
ORDER BY 1;

-- (b) quantidade de pedidos por estado
SELECT c.estado, COUNT(*) AS pedidos
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
GROUP BY c.estado
ORDER BY c.estado;

-- (c) pedidos divergentes
SELECT id, valor_total, valor_itens,
       ROUND(valor_total - valor_itens, 2) AS diferenca
FROM pedidos
WHERE divergente
ORDER BY id;