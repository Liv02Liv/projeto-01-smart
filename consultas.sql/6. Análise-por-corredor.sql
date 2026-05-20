-- 6. Análise por corredor (primeiros 2 caracteres da Localização)
SELECT
    SUBSTR(Localizacao, 1, 2) AS corredor,
    COUNT(*) AS total_itens,
    SUM(CASE WHEN Quantidade <= 0 THEN 1 ELSE 0 END) AS rupturas,
    SUM(CASE WHEN Quantidade > 0 AND Quantidade < Minimo THEN 1 ELSE 0 END) AS abaixo_min,
    SUM(CASE WHEN Quantidade > Maximo THEN 1 ELSE 0 END) AS excesso
FROM estoque
GROUP BY corredor
ORDER BY corredor;

