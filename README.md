# csv_to_sqlserver_powerbi_python

Here’s a clean, professional **README.md** you can use for your project. It walks through everything end-to-end: installing SQL Server 2022 Express, configuring it, loading CSV via Python, and connecting to Power BI.

---

# 📊 CSV to SQL Server to Power BI Pipeline

This project demonstrates how to:

1. Load a CSV file using Python
2. Store it in a SQL Server database
3. Connect the database to Power BI for visualization

---

## 🧰 Tech Stack

* Python (pandas, sqlalchemy, pyodbc)
* SQL Server 2022 Express
* SQL Server Management Studio
* Power BI

---

## ⚙️ Step 1: Install SQL Server & Tools

### 1. Install SQL Server

* Download and install **SQL Server 2022 Express**
* During setup:

  * Instance Name: `SQLEXPRESS`
  * Authentication Mode: Windows Authentication
  * Ensure Database Engine Services is selected

✅ After installation, you should see:

* Server: `localhost\SQLEXPRESS`

---

### 2. Install SSMS

* Install **SQL Server Management Studio (SSMS)**
* Connect using:

  * Server name: `localhost\SQLEXPRESS`
  * Authentication: Windows Authentication

Run:


---
### manual creating of database:
Python code already includes this step:

IF DB_ID('BBBP_DB') IS NULL
CREATE DATABASE BBBP_DB

So the database will be created automatically the first time the script runs.

🟡 But if you want it manually in SQL Server Management Studio
You might want to run:
```
CREATE DATABASE BBBP_DB;
```
---

### 3. Install ODBC Driver

Install:

* **ODBC Driver 17 for SQL Server**

This is required for Python to connect.

---

## 🐍 Step 2: Python Environment Setup

Install required libraries:

```bash
pip install pandas sqlalchemy pyodbc
```

---

## 📥 Step 3: Python Script (CSV → SQL Server)

Use the following script:

```python
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Load CSV
url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"
df = pd.read_csv(url)

# 2. Clean columns
df.columns = df.columns.str.strip().str.lower()

# 3. SQL Server connection
server = "localhost\\SQLEXPRESS"
database = "BBBP_DB"

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string, fast_executemany=True)

# 4. Create database if not exists
with engine.connect() as conn:
    conn.execute(text(f"""
        IF DB_ID('{database}') IS NULL
        CREATE DATABASE {database}
    """))
    conn.commit()

# 5. Reload engine
engine = create_engine(connection_string, fast_executemany=True)

# 6. Load data
df.to_sql(
    name="BBBP",
    con=engine,
    if_exists="replace",
    index=False
)

# 7. Verify
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM BBBP"))
    print("Rows:", result.scalar())
```

---

## 🗄️ Step 4: Verify in SSMS

Run:

```sql
USE BBBP_DB;
SELECT TOP 10 * FROM BBBP;
```

✅ You should see data like:

* `num`
* `name`
* `p_np`
* `smiles`

---

## 🔌 Step 5: Connect to Power BI

### 1. Open Power BI Desktop

### 2. Click:

* **Get Data → SQL Server**

### 3. Enter:

* Server: `localhost\SQLEXPRESS`
* Database: `BBBP_DB`

### 4. Choose:

* Import (recommended for performance)

### 5. Select table:

* `BBBP`

---

## 📊 Step 6: Build Visuals in Power BI

Example ideas:

* Count of molecules (`num`)
* Distribution of `p_np`
* Table of compound names
* Custom filtering by properties

---

## ⚠️ Common Issues & Fixes

### ❌ Cannot connect to SQL Server

* Ensure SQL Server service is running
* Check instance name: `SQLEXPRESS`

---

### ❌ ODBC Driver Error

* Install **ODBC Driver 17**
* Or update connection string to Driver 18 if installed

---

### ❌ Login failed

* Ensure Windows Authentication is enabled
* Run SSMS as Administrator

---

### ❌ Table not visible in Power BI

* Refresh schema
* Ensure correct database selected

---

## 📁 Project Structure

```
project/
│
├── script.py
├── README.md
```

---

## ✅ Final Output

* SQL Database: `BBBP_DB`
* Table: `BBBP`
* Connected to Power BI for reporting

---

## 🚀 Next Improvements

* Add scheduled refresh in Power BI
* Normalize database schema
* Add indexes in SQL for performance
* Use stored procedures for ETL

---


## Some screenshot from PyCharm Terminal, SQL server settings and power BI import settings:

<img width="759" height="469" alt="{EDFFB5CE-6430-43FA-9918-A960CFA2B315}" src="https://github.com/user-attachments/assets/9b1ac3b1-d575-4cfe-be51-cd1618c5306a" />



<img width="247" height="156" alt="{ECCCC835-743D-4C2E-9D94-76FD050E95C7}" src="https://github.com/user-attachments/assets/e637701a-c78e-45c7-bd5a-f03c67ce821e" />


<img width="595" height="481" alt="{07BE5BF7-F705-4808-B0A1-E59C130C7D77}" src="https://github.com/user-attachments/assets/1bb3c45b-e530-4c89-852f-95e0e43698ec" />


<img width="643" height="446" alt="{F4915D4A-7ADC-4280-9B78-B9C954645480}" src="https://github.com/user-attachments/assets/35716bcc-9959-4b8c-a52a-34660957cc19" />
