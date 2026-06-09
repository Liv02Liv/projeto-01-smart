-- 1. Situação geral por status
SELECT Status, COUNT(*) AS total
FROM estoque
GROUP BY Status;

