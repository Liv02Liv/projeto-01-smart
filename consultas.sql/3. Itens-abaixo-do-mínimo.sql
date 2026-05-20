-- 3. Itens abaixo do Minimo (mas com saldo positivo)
SELECT Item, Quantidade, Minimo,
       (Minimo - Quantidade) AS deficit,
       (Maximo - Quantidade) AS a_comprar,
       Localizacao
FROM estoque
WHERE Quantidade > 0 AND Quantidade < Minimo
ORDER BY deficit DESC;