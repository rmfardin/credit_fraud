# etl.py
import pandas as pd
import sqlite3
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("etl.log"), logging.StreamHandler()]
)

def load_to_sqlite(csv_path: str, db_path: str = "fraud.db", table_name: str = "transactions"):
    if not os.path.exists(csv_path):
        logging.error(f"CSV file not found: {csv_path}")
        return

    logging.info(f"Reading CSV from {csv_path} …")
    df = pd.read_csv(csv_path)

    logging.info(f"Loaded {len(df)} rows × {len(df.columns)} columns")
    logging.info(f"Columns: {list(df.columns)}")

    nulls = df.isna().sum().sum()
    dupes = df.duplicated().sum()
    logging.info(f"Total null values: {nulls}")
    logging.info(f"Total duplicate rows: {dupes}")

    # Write to SQLite
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logging.info(f"Successfully wrote table '{table_name}' to {db_path}")
    finally:
        conn.close()

if __name__ == "__main__":
    load_to_sqlite("data/transactions.csv")
