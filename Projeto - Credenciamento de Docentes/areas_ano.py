from pathlib import Path
import sqlite3
import pandas as pd

projeto = Path(__file__).resolve().parent
caminho_db = projeto / "dados_scimago" / "scimago.db"

conn = sqlite3.connect(caminho_db)

tabelas = [
    linha[0]
    for linha in conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
    ORDER BY name;
    """)
]

conn.close()

qtd = 0
for nome in tabelas:
  qtd += 1
  print(nome)
print(qtd)