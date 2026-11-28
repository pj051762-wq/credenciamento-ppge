from pathlib import Path
import zipfile
import re
import sqlite3
import pandas as pd

# Configurando caminhos relativos para a reprodutibilidade e integracao com SQL
projeto = Path(__file__).resolve().parent
caminho_zip = projeto / "dados_scimago" / "Revistas Scimago Journal (2022 - 2025).zip"
caminho_db = projeto / "dados_scimago" / "scimago.db"

conn = sqlite3.connect(caminho_db)

padrao_ano = re.compile(r"scimagojr\s*\d{2}(\d{2})", re.IGNORECASE)  
padrao_limpo = re.compile(r"[^a-z0-9]+")  

def nome_tabela(caminho: str) -> str:  
  name = Path(caminho).stem  
  area_bruta = name.split("-", 1)[-1].strip().lower()  
  area = padrao_limpo.sub("_", area_bruta).strip("_")  
  match_ano = padrao_ano.search(name)  
  ano = match_ano.group(1) if match_ano else ""  
  return f"{area}_{ano}" if ano else area  

def precisa_popular_banco(db_path: Path, qtd_esperada: int = 108) -> bool:
  if not db_path.exists():
    return True

  conn = sqlite3.connect(db_path)
  with conn:
    qtd_tabelas = conn.execute("""
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%';
        """).fetchone()[0]
  conn.close()
  return qtd_tabelas < qtd_esperada

if precisa_popular_banco(caminho_db, qtd_esperada = 108):
  conn = sqlite3.connect(caminho_db)
  with zipfile.ZipFile(caminho_zip, "r") as zf:  
    for item in zf.namelist():  
      if item.endswith("/"):  
        continue  

      tabela = nome_tabela(item)  
      conn.execute(f"DROP TABLE IF EXISTS {tabela}")  

      with zf.open(item) as f:  
        for pedaco in pd.read_csv(
            f, sep = ";", usecols = ["Sourceid", "Title", "SJR"], chunksize = 25_000
        ):  
          pedaco.to_sql(tabela, conn, if_exists = "append", index = False)  
  conn.commit()  
  conn.close()

print(pd.read_sql_query("SELECT MAX(SJR) FROM mathematics_25", conn))

conn.close()
