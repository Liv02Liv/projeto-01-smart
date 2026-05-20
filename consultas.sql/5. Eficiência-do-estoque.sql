-- 5. Eficiência do estoque (% dentro do intervalo ideal)
SELECT
    ROUND(100.0 * SUM(CASE WHEN Quantidade >= Minimo AND Quantidade <= Maximo THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ideal,
    ROUND(100.0 * SUM(CASE WHEN Quantidade <= 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ruptura,
    ROUND(100.0 * SUM(CASE WHEN Quantidade > Maximo THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_excesso
FROM estoque;