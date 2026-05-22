# 🏭 Smart Inventores — Sistema de Gestão de Estoque

> Projeto desenvolvido pela **Equipe PCP — SENAI **  
> Disciplina: Planejamento e Controle da Produção (PCP)

---

## 📌 Sumário

1. [O Problema](#-o-problema)
2. [Protótipo Inicial — SIO](#-protótipo-inicial--sio)
3. [Solução Inicial — Planilhas](#-solução-inicial--planilhas)
4. [Evolução — Sistema em Python](#-evolução--sistema-em-python)
5. [Análise com SQLite](#-análise-com-sqlite)
6. [Consultas SQL Disponíveis](#-consultas-sql-disponíveis)
7. [Estrutura do Projeto](#-estrutura-do-projeto)
8. [Como Executar](#-como-executar)

---

## ⚠️ O Problema

Durante o desenvolvimento do projeto no curso de PCP, foi identificado um problema recorrente na indústria:

- **Tempo excessivo** na busca de materiais no estoque
- **Falta de organização** física e sistêmica dos itens
- **Paradas de máquina** por ausência de peças no momento certo

Esses fatores impactam diretamente a produtividade e os custos operacionais da empresa, tornando essencial um sistema confiável de controle de estoque.

---

## 🖼️ Protótipo Inicial — SIO

Antes de qualquer linha de código ou planilha estruturada, o projeto nasceu como uma **proposta conceitual** batizada de **SIO — Smart Inventory Optimization**.

### Slide de apresentação

O primeiro artefato do projeto foi um slide de apresentação que sintetizava a proposta de valor:

> *"Estoque organizado, empresa otimizada — o segredo para reduzir custos e aumentar a eficiência."*

O slide continha o logotipo do SIO, uma breve descrição do sistema e dois pontos de acesso: **Planilha** e **Feedback** — sinalizando desde o início que o projeto seria construído de forma iterativa, coletando retorno dos usuários a cada etapa.

### Planilha protótipo

A primeira versão operacional foi uma planilha no **Excel/OneDrive**, com as seguintes colunas:

| Coluna | Descrição |
|---|---|
| **ID do Item** | Identificador único (ITM001, ITM002…) |
| **Nome da Peça** | Descrição do item |
| **Quantidade/A** | Quantidade disponível |
| **Localização** | Corredor de armazenamento (C1, C2, C3…) |
| **Status** | Situação do item (ex.: INDISPONÍVEL, em destaque rosa) |
| **Data de Retirada** | Registro da última movimentação |
| **Peças Retiradas** | Quantidade retirada na operação |
| **Nome do Operador** | Responsável pela movimentação |

Essa versão já demonstrava os conceitos centrais do sistema — **rastreabilidade por localização**, **controle de status visual** e **registro de operador** — que foram mantidos e aprimorados em todas as versões seguintes.

> 💡 O protótipo foi fundamental para validar a estrutura de dados antes de migrar para Python e, posteriormente, para SQLite.

---

## 📊 Solução Inicial — Planilhas

A primeira abordagem foi desenvolvida utilizando **planilhas eletrônicas** (`smart-dados.xlsx`).

O objetivo era simular um sistema de controle de estoque com:

- Registro de entrada e saída de itens
- Organização por localização (corredor, estante e prateleira)
- Controle manual de quantidades mínimas e máximas

Essa etapa foi fundamental para **validar a ideia** e entender os dados reais do estoque antes de partir para uma solução mais robusta.

---

## 🐍 Evolução — Sistema em Python

Com a validação da planilha, o projeto evoluiu para um **sistema desktop com interface gráfica**, desenvolvido em Python (`smart_inventores_v2.py`).

### Funcionalidades implementadas

| Funcionalidade | Descrição |
|---|---|
| **Controle de estoque** | Registro de entradas e saídas com validação |
| **Estoque mínimo e máximo** | Limites personalizados por item |
| **Alertas automáticos** | Notificação ao atingir ponto de pedido ou estoque crítico |
| **Histórico de movimentações** | Log completo com data, hora, tipo e quantidade |
| **Localização automática** | Atribuição no formato `CxEyPz` (Corredor, Estante, Prateleira) |
| **Busca em tempo real** | Filtro dinâmico na tabela de estoque |
| **Exportação CSV** | Relatório com estoque atual e histórico completo |
| **Persistência de dados** | Salvamento automático em `inventory_data.json` |

### Interface gráfica

A interface foi construída com **Tkinter** e organizada em três painéis principais:

- **Painel de entrada** — campos para registrar movimentações e acionar funções
- **Tabela de estoque** — exibe todos os itens com status colorido:
  - 🟢 **Disponível** — quantidade acima de 50% do máximo
  - 🟡 **Fazer Pedido** — entre o mínimo e 50% do máximo
  - 🔴 **Estoque de Segurança** — quantidade no limite mínimo ou abaixo
  - ⚫ **Indisponível** — quantidade zerada
- **Histórico** — caixa de texto com todas as movimentações da sessão

### Como executar o sistema

```bash
# Instale o Python 3.10+ se necessário
python smart_inventores_v2.py
```

> O arquivo `inventory_data.json` é gerado automaticamente na primeira execução e persiste os dados entre sessões.

---

## 🗄️ Análise com SQLite

Com os dados coletados pela planilha (`smart-dados.xlsx`), foi realizada uma **análise aprofundada com SQLite**, permitindo consultas precisas sobre a saúde do estoque.

### Base de dados

- **100 itens** cadastrados
- **4 corredores** (C1 a C4), cada um com 25 itens
- Localização no formato `CxEyPz` — ex.: `C2E4P3`

### Indicadores de eficiência

| Indicador | Resultado | Significado |
|---|---|---|
| `pct_ideal` | **63,0%** | Itens dentro do intervalo saudável (entre mín. e máx.) |
| `pct_ruptura` | **10,0%** | Itens zerados ou negativos — sem produto para atender |
| `pct_excesso` | **13,0%** | Itens acima do máximo — capital parado |

> 💡 Os 14% restantes são itens com saldo positivo mas abaixo do mínimo — vulneráveis a nova ruptura com uma única saída.

### Resumo por corredor

| Corredor | Itens | Rupturas | Abaixo do Mín. | Excesso | Situação |
|---|---|---|---|---|---|
| **C1** — Ferramentas | 25 | 2 | 2 | 4 | Rupturas em ferramentas básicas |
| **C2** — Diagnóstico/Fluidos | 25 | 3 | 1 | 6 | Excesso em equipamentos de diagnóstico |
| **C3** — Suspensão/Ignição | 25 | 2 | 9 | 1 | 🔴 Mais crítico — 9 itens abaixo do mín. |
| **C4** — Elétrica/Pneus | 25 | 3 | 2 | 2 | 3 rupturas em itens de alto giro |

### Itens em ruptura (saldo ≤ 0)

| Item | Qtd. | Local | Situação |
|---|---|---|---|
| Filtro de combustível | −2 | C2E4P3 | Saídas não registradas |
| Chave de roda | −1 | C1E3P1 | Saída sem baixa no sistema |
| Terminal de direção | −1 | C3E1P5 | Saída sem baixa no sistema |

> ⚠️ Saldo negativo é fisicamente impossível. Indica erro de lançamento — realizar contagem física imediata.

---

## 🔍 Consultas SQL Disponíveis

Os arquivos `.sql` cobrem os principais cenários de análise do estoque. Execute com:

```bash
sqlite3 estoque.db < nome_do_arquivo.sql
```

### `1__Situação-geral-por-status.sql`
Conta quantos itens existem em cada status (Ruptura, Abaixo do mínimo, Ideal, Excesso).

```sql
SELECT Status, COUNT(*) AS total
FROM estoque
GROUP BY Status;
```

---

### `2__Itens-em-ruptura.sql`
Lista todos os itens com quantidade ≤ 0, ordenados do mais crítico ao menos crítico.

```sql
SELECT Item, Quantidade, Minimo, Localizacao
FROM estoque
WHERE Quantidade <= 0
ORDER BY Quantidade ASC;
```

---

### `3__Itens-abaixo-do-mínimo.sql`
Lista itens com saldo positivo mas abaixo do mínimo, mostrando o déficit e quanto comprar para atingir o máximo.

```sql
SELECT Item, Quantidade, Minimo,
       (Minimo - Quantidade) AS deficit,
       (Maximo - Quantidade) AS a_comprar,
       Localizacao
FROM estoque
WHERE Quantidade > 0 AND Quantidade < Minimo
ORDER BY deficit DESC;
```

---

### `4__Itens-acima-do-máximo.sql`
Identifica itens em excesso e o quanto ultrapassa o limite máximo.

```sql
SELECT Item, Quantidade, Maximo,
       (Quantidade - Maximo) AS excesso,
       Localizacao
FROM estoque
WHERE Quantidade > Maximo
ORDER BY excesso DESC;
```

---

### `5__Eficiência-do-estoque.sql`
Calcula os três percentuais de saúde do estoque em uma única consulta.

```sql
SELECT
    ROUND(100.0 * SUM(CASE WHEN Quantidade >= Minimo AND Quantidade <= Maximo THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ideal,
    ROUND(100.0 * SUM(CASE WHEN Quantidade <= 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ruptura,
    ROUND(100.0 * SUM(CASE WHEN Quantidade > Maximo THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_excesso
FROM estoque;
```

---

### `6__Análise-por-corredor.sql`
Resume os problemas agrupados por corredor — visão gerencial do armazém.

```sql
SELECT
    SUBSTR(Localizacao, 1, 2) AS corredor,
    COUNT(*) AS total_itens,
    SUM(CASE WHEN Quantidade <= 0 THEN 1 ELSE 0 END) AS rupturas,
    SUM(CASE WHEN Quantidade > 0 AND Quantidade < Minimo THEN 1 ELSE 0 END) AS abaixo_min,
    SUM(CASE WHEN Quantidade > Maximo THEN 1 ELSE 0 END) AS excesso
FROM estoque
GROUP BY corredor
ORDER BY corredor;
```

---

### `7__Itens-problemáticos.sql`
Lista todos os itens fora do intervalo ideal para cada corredor (C1 a C4), com colunas de déficit e excedente calculadas automaticamente.

```sql
-- Exemplo para o corredor C3 (mais crítico)
SELECT Item, Quantidade, Minimo, Maximo, Localizacao,
    CASE
        WHEN Quantidade <= 0      THEN 'RUPTURA'
        WHEN Quantidade < Minimo  THEN 'Abaixo do minimo'
        WHEN Quantidade > Maximo  THEN 'Excesso'
    END AS situacao,
    CASE WHEN Quantidade < Minimo THEN Minimo - Quantidade ELSE NULL END AS deficit,
    CASE WHEN Quantidade > Maximo THEN Quantidade - Maximo ELSE NULL END AS excedente
FROM estoque
WHERE SUBSTR(Localizacao, 1, 2) = 'C3'
  AND (Quantidade <= 0 OR Quantidade < Minimo OR Quantidade > Maximo)
ORDER BY
    CASE WHEN Quantidade <= 0 THEN 1
         WHEN Quantidade < Minimo THEN 2
         ELSE 3 END,
    Quantidade ASC;
```

> O arquivo completo contém a mesma query repetida para C1, C2, C3 e C4.

---

## 📁 Estrutura do Projeto

```
smart-inventores/
│
├── smart_inventores_v2.py          # Sistema desktop com interface gráfica
├── smart-dados.xlsx                # Planilha base com os 100 itens do estoque
├── inventory_data.json             # Dados persistidos pelo sistema (gerado em runtime)
│
├── sql/
│   ├── 1__Situação-geral-por-status.sql
│   ├── 2__Itens-em-ruptura.sql
│   ├── 3__Itens-abaixo-do-mínimo.sql
│   ├── 4__Itens-acima-do-máximo.sql
│   ├── 5__Eficiência-do-estoque.sql
│   ├── 6__Análise-por-corredor.sql
│   └── 7__Itens-problemáticos.sql
│
└── README.md
```

---

## ▶️ Como Executar

**Pré-requisitos:** Python 3.10+ (Tkinter já incluso na instalação padrão)

```bash
# 1. Clone ou baixe o repositório
# 2. Execute o sistema
python smart_inventores_v2.py
```

**Para as consultas SQL:**

```bash
# Importe a planilha para o SQLite (use DB Browser ou script de importação)
sqlite3 estoque.db

# Execute uma consulta
sqlite3 estoque.db < sql/6__Análise-por-corredor.sql
```

---

*Documento de uso interno — Gestão de Estoque com SQLite | Equipe PCP — SENAI Marechal Cândido Rondon*
