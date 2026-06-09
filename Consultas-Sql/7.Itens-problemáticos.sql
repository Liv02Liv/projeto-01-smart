-- Lista todos os itens problemáticos do corredor C1.
SELECT
    Item,
    Quantidade,
    Minimo,
    Maximo,
    Localizacao,
    CASE
        WHEN Quantidade <= 0 THEN 'RUPTURA'
        WHEN Quantidade < Minimo THEN 'Abaixo do minimo'
        WHEN Quantidade > Maximo THEN 'Excesso'
    END AS situacao,
    CASE
        WHEN Quantidade < Minimo THEN Minimo - Quantidade
        ELSE NULL
    END AS deficit,
    CASE
        WHEN Quantidade > Maximo THEN Quantidade - Maximo
        ELSE NULL
    END AS excedente
FROM estoque
WHERE SUBSTR(Localizacao, 1, 2) = 'C1'
  AND (Quantidade <= 0 OR Quantidade < Minimo OR Quantidade > Maximo)
ORDER BY
    CASE WHEN Quantidade <= 0 THEN 1
         WHEN Quantidade < Minimo THEN 2
         ELSE 3 END,
    Quantidade ASC;


-- Lista todos os itens problemáticos do corredor C2.
SELECT
    Item,
    Quantidade,
    Minimo,
    Maximo,
    Localizacao,
    CASE
        WHEN Quantidade <= 0 THEN 'RUPTURA'
        WHEN Quantidade < Minimo THEN 'Abaixo do minimo'
        WHEN Quantidade > Maximo THEN 'Excesso'
    END AS situacao,
    CASE
        WHEN Quantidade < Minimo THEN Minimo - Quantidade
        ELSE NULL
    END AS deficit,
    CASE
        WHEN Quantidade > Maximo THEN Quantidade - Maximo
        ELSE NULL
    END AS excedente
FROM estoque
WHERE SUBSTR(Localizacao, 1, 2) = 'C2'
  AND (Quantidade <= 0 OR Quantidade < Minimo OR Quantidade > Maximo)
ORDER BY
    CASE WHEN Quantidade <= 0 THEN 1
         WHEN Quantidade < Minimo THEN 2
         ELSE 3 END,
    Quantidade ASC;


-- Lista todos os itens problemáticos do corredor C3.
SELECT
    Item,
    Quantidade,
    Minimo,
    Maximo,
    Localizacao,
    CASE
        WHEN Quantidade <= 0 THEN 'RUPTURA'
        WHEN Quantidade < Minimo THEN 'Abaixo do minimo'
        WHEN Quantidade > Maximo THEN 'Excesso'
    END AS situacao,
    CASE
        WHEN Quantidade < Minimo THEN Minimo - Quantidade
        ELSE NULL
    END AS deficit,
    CASE
        WHEN Quantidade > Maximo THEN Quantidade - Maximo
        ELSE NULL
    END AS excedente
FROM estoque
WHERE SUBSTR(Localizacao, 1, 2) = 'C3'
  AND (Quantidade <= 0 OR Quantidade < Minimo OR Quantidade > Maximo)
ORDER BY
    CASE WHEN Quantidade <= 0 THEN 1
         WHEN Quantidade < Minimo THEN 2
         ELSE 3 END,
    Quantidade ASC;


-- Lista todos os itens problemáticos do corredor C4.
SELECT
    Item,
    Quantidade,
    Minimo,
    Maximo,
    Localizacao,
    CASE
        WHEN Quantidade <= 0 THEN 'RUPTURA'
        WHEN Quantidade < Minimo THEN 'Abaixo do minimo'
        WHEN Quantidade > Maximo THEN 'Excesso'
    END AS situacao,
    CASE
        WHEN Quantidade < Minimo THEN Minimo - Quantidade
        ELSE NULL
    END AS deficit,
    CASE
        WHEN Quantidade > Maximo THEN Quantidade - Maximo
        ELSE NULL
    END AS excedente
FROM estoque
WHERE SUBSTR(Localizacao, 1, 2) = 'C4'
  AND (Quantidade <= 0 OR Quantidade < Minimo OR Quantidade > Maximo)
ORDER BY
    CASE WHEN Quantidade <= 0 THEN 1
         WHEN Quantidade < Minimo THEN 2
         ELSE 3 END,
    Quantidade ASC;