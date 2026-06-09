-- 2. Itens em ruptura (quantidade <= 0)
SELECT Item, Quantidade, Minimo, Localizacao
FROM estoque
WHERE Quantidade <= 0
ORDER BY Quantidade ASC;

