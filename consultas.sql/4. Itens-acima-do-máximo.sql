-- 4. Itens acima do máximo (excesso)
SELECT Item, Quantidade, Maximo,
       (Quantidade - Maximo) AS excesso,
       Localizacao
FROM estoque
WHERE Quantidade > Maximo
ORDER BY excesso DESC;