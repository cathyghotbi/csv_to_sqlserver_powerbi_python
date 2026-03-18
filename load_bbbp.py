import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------
# 1. Load CSV from URL
# -------------------------------
url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"
df = pd.read_csv(url)

print(f"CSV loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")

# -------------------------------
# 2. Clean column names
# -------------------------------
df.columns = df.columns.str.strip().str.lower()

# Optional: rename for SQL friendliness
df.rename(columns={
    "p_np": "p_np",
    "num": "num",
    "name": "name",
    "smiles": "smiles"
}, inplace=True)

# -------------------------------
# 3. SQL Server connection
# -------------------------------
server = "localhost\\SQLEXPRESS"
database = "BBBP_DB"

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string, fast_executemany=True)

print("Connected to SQL Server!")

# -------------------------------
# 4. Create database if not exists
# -------------------------------
with engine.connect() as conn:
    conn.execute(text(f"""
    IF DB_ID('{database}') IS NULL
    CREATE DATABASE {database}
    """))
    conn.commit()

print(f"Database '{database}' is ready.")

# -------------------------------
# 5. Reload engine to ensure DB context
# -------------------------------
engine = create_engine(connection_string, fast_executemany=True)

# -------------------------------
# 6. Load data into SQL table
# -------------------------------
df.to_sql(
    name="BBBP",
    con=engine,
    if_exists="replace",   # overwrite table if exists
    index=False
)

print("Data successfully loaded into table 'BBBP'!")

# -------------------------------
# 7. Verify load
# -------------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM BBBP"))
    count = result.scalar()

print(f"Rows in SQL table: {count}")
