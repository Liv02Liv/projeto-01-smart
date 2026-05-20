import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///dados.db")

# Csv1 estoque 

df1 = pd.read_csv("estoque-atual-v2.csv", sep=";")
df1.to_sql("estoque", engine, if_exists="replace", index=False)

# Csv2 historico 

df2 = pd.read_csv("historico-movimentacoes-v2.csv", sep=";")
df2.to_sql("historico", engine, if_exists="replace", index=False)



