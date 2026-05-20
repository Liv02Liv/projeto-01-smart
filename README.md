# 📦 SmartInventory

> Sistema de análise e gestão de estoque utilizando **Python**, **Pandas** e **SQLite** como motor de consulta.

---

## 📋 Sobre o Projeto

O **SmartInventory** é uma solução de análise de estoque baseada em dados, que transforma uma planilha Excel em um banco de dados consultável via SQL. O objetivo é fornecer **visibilidade operacional em tempo real** sobre rupturas, excessos e eficiência do estoque — tudo de forma automatizada e reproduzível.

A análise é feita sobre o arquivo `smart-dados.xlsx`, contendo **100 itens** distribuídos em **4 corredores** (C1 a C4), cada um com 5 estantes e 5 prateleiras.

---

## 🗂️ Estrutura do Projeto

```
SmartInventory/
│
├── smart-dados.xlsx          # Base de dados principal (planilha de estoque)
├── estoque.db                # Banco SQLite gerado automaticamente
│
├── scripts/
│   ├── importar_dados.py     # Importa o Excel para o SQLite
│   ├── analise_geral.sql     # Situação geral e eficiência do estoque
│   ├── rupturas.sql          # Itens com quantidade <= 0
│   ├── abaixo_minimo.sql     # Itens abaixo do estoque mínimo
│   ├── excesso.sql           # Itens acima do estoque máximo
│   ├── corredor_c1.sql       # Análise detalhada — Corredor C1
│   ├── corredor_c2.sql       # Análise detalhada — Corredor C2
│   ├── corredor_c3.sql       # Análise detalhada — Corredor C3
│   └── corredor_c4.sql       # Análise detalhada — Corredor C4
│
├── relatorios/
│   ├── relatorio_estrategico_estoque.docx
│   └── analise_sqlite_perguntas_respostas.docx
│
└── README.md
```

---

## ⚙️ Requisitos

| Ferramenta | Versão recomendada |
|---|---|
| Python | 3.8 ou superior |
| pandas | `pip install pandas` |
| openpyxl | `pip install openpyxl` |
| SQLite | Nativo no Python (módulo `sqlite3`) |

---

## 🚀 Como Usar

### 1. Clonar o repositório

```bash
git clone https://github.com/Liv02Liv/SmartInventory.git
cd SmartInventory
```

### 2. Instalar as dependências

```bash
pip install pandas openpyxl
```

### 3. Importar os dados do Excel para o SQLite

```python
import pandas as pd
import sqlite3

# Lê a aba de estoque da planilha
df = pd.read_excel("smart-dados.xlsx", sheet_name="=== ESTOQUE ATUAL ===")

# Cria o banco e insere os dados
conn = sqlite3.connect("estoque.db")
df.to_sql("estoque", conn, if_exists="replace", index=False)

print("✅ Banco de dados criado com sucesso!")
conn.close()
```

### 4. Executar as consultas SQL

```bash
# Exemplo: ver todos os itens em ruptura
sqlite3 estoque.db < scripts/rupturas.sql

# Exemplo: eficiência geral do estoque
sqlite3 estoque.db < scripts/analise_geral.sql

# Exemplo: análise do corredor C3
sqlite3 estoque.db < scripts/corredor_c3.sql
```

---

## 🗃️ Estrutura da Tabela `estoque`

| Coluna | Tipo | Descrição |
|---|---|---|
| `Item` | TEXT | Nome do produto |
| `Quantidade` | INTEGER | Saldo atual em estoque |
| `Mínimo` | INTEGER | Estoque mínimo de segurança |
| `Máximo` | INTEGER | Estoque máximo permitido |
| `Status` | TEXT | Disponível / Estoque de Segurança / Fazer Pedido / Indisponível |
| `Localização` | TEXT | Código de posição: formato `CxEyPz` (Corredor, Estante, Prateleira) |

---

## 🔍 Principais Consultas SQL

### Situação geral — eficiência do estoque

```sql
SELECT
  ROUND(100.0 * SUM(CASE WHEN Quantidade >= Mínimo
    AND Quantidade <= Máximo THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ideal,
  ROUND(100.0 * SUM(CASE WHEN Quantidade <= 0
    THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ruptura,
  ROUND(100.0 * SUM(CASE WHEN Quantidade > Máximo
    THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_excesso
FROM estoque;
```

**Resultado atual:**

| pct_ideal | pct_ruptura | pct_excesso |
|---|---|---|
| 63,0% ⚠️ | 10,0% 🔴 | 13,0% 🔵 |

> Meta recomendada: `pct_ideal ≥ 80%`

---

### Itens em ruptura (quantidade ≤ 0)

```sql
SELECT Item, Quantidade, Mínimo, Localização
FROM estoque
WHERE Quantidade <= 0
ORDER BY Quantidade ASC;
```

---

### Itens abaixo do mínimo (com saldo positivo)

```sql
SELECT Item, Quantidade, Mínimo,
       (Mínimo - Quantidade) AS deficit,
       (Máximo - Quantidade) AS a_comprar,
       Localização
FROM estoque
WHERE Quantidade > 0 AND Quantidade < Mínimo
ORDER BY deficit DESC;
```

---

### Itens em excesso

```sql
SELECT Item, Quantidade, Máximo,
       (Quantidade - Máximo) AS excedente,
       Localização
FROM estoque
WHERE Quantidade > Máximo
ORDER BY excedente DESC;
```

---

### Análise por corredor

```sql
SELECT
    SUBSTR(Localização, 1, 2) AS corredor,
    COUNT(*) AS total_itens,
    SUM(CASE WHEN Quantidade <= 0 THEN 1 ELSE 0 END) AS rupturas,
    SUM(CASE WHEN Quantidade > 0 AND Quantidade < Mínimo THEN 1 ELSE 0 END) AS abaixo_min,
    SUM(CASE WHEN Quantidade > Máximo THEN 1 ELSE 0 END) AS excesso
FROM estoque
GROUP BY corredor
ORDER BY corredor;
```

**Resultado atual:**

| Corredor | Itens | Rupturas | Abaixo Mín. | Excesso |
|---|---|---|---|---|
| C1 — Ferramentas | 25 | 2 🔴 | 2 ⚠️ | 4 🔵 |
| C2 — Diagnóstico/Fluidos | 25 | 3 🔴 | 1 ⚠️ | 6 🔵 |
| C3 — Suspensão/Ignição | 25 | 2 🔴 | **9** ⚠️ | 1 🔵 |
| C4 — Elétrica/Pneus | 25 | 3 🔴 | 2 ⚠️ | 2 🔵 |

---

### Detalhe por corredor (itens problemáticos)

```sql
-- Substitua 'C1' por C2, C3 ou C4 conforme necessário
SELECT Item, Quantidade, Mínimo, Máximo, Localização,
  CASE
    WHEN Quantidade <= 0      THEN 'RUPTURA'
    WHEN Quantidade < Mínimo  THEN 'Abaixo do mínimo'
    WHEN Quantidade > Máximo  THEN 'Excesso'
  END AS situacao
FROM estoque
WHERE SUBSTR(Localização, 1, 2) = 'C1'
  AND (Quantidade <= 0 OR Quantidade < Mínimo OR Quantidade > Máximo)
ORDER BY
  CASE WHEN Quantidade <= 0 THEN 1
       WHEN Quantidade < Mínimo THEN 2
       ELSE 3 END,
  Quantidade ASC;
```

---

## 📊 Diagnóstico do Estoque Atual

### O que significa cada status?

| Status | Descrição |
|---|---|
| ✅ **Disponível** | Quantidade entre o mínimo e o máximo |
| ⚠️ **Estoque de Segurança** | Quantidade abaixo do mínimo, mas positiva |
| 🟠 **Fazer Pedido** | Nível crítico — reposição urgente necessária |
| 🔴 **Indisponível** | Quantidade zero ou negativa — ruptura total |

### O que é ruptura?

Ruptura significa que o item **não existe fisicamente** na prateleira. Quando a quantidade aparece como negativa (`-1`, `-2`), indica **erros de lançamento** no sistema — saídas registradas sem entrada correspondente. Nesses casos, é necessário:

1. Realizar **contagem física** do item
2. **Corrigir o saldo** no sistema
3. **Investigar** qual movimentação não foi registrada

### O que é excesso?

Itens com quantidade acima do máximo representam **capital imobilizado**: espaço ocupado, dinheiro parado e risco de obsolescência. A ação recomendada é pausar novos pedidos e avaliar redistribuição.

---

## 🗺️ Como interpretar a Localização

O código de localização segue o padrão **`CxEyPz`**:

```
C1 E 2 P 3
│  │   │
│  │   └── Prateleira (P1 a P5)
│  └────── Estante    (E1 a E5)
└────────── Corredor   (C1 a C4)
```

**Exemplo:** `C3E1P5` = Corredor 3, Estante 1, Prateleira 5

---

## 📁 Relatórios Gerados

| Arquivo | Conteúdo |
|---|---|
| `relatorio_estrategico_estoque.docx` | Relatório completo com KPIs, riscos, recomendações e plano de ação |
| `analise_sqlite_perguntas_respostas.docx` | Explicações detalhadas sobre ruptura, eficiência e análise por corredor |

---

## 🔧 Dicas de Uso

```bash
# Executar uma query e salvar o resultado em CSV
sqlite3 -csv -header estoque.db "SELECT * FROM estoque WHERE Quantidade <= 0;" > rupturas.csv

# Abrir o banco em modo interativo
sqlite3 estoque.db

# Ver todas as tabelas disponíveis
sqlite3 estoque.db ".tables"

# Ver a estrutura da tabela estoque
sqlite3 estoque.db ".schema estoque"
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests com melhorias nas queries, novos relatórios ou otimizações no processo de importação.

---

## 📄 Licença

Este projeto é de uso interno. Consulte o responsável pelo repositório para informações sobre licenciamento.

---

*Gerado em 03/05/2026 · Base: smart-dados.xlsx · 100 itens · SQLite*
