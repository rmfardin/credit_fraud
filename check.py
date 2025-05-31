import sqlite3
import pandas as pd

conn = sqlite3.connect("fraud.db")

# Basic stats
df = pd.read_sql("SELECT * FROM transactions", conn)
print(f"Rows: {len(df)}")
print(f"Fraud cases: {df['isFraud'].sum()}")

# Time parsing
df['transactionDateTime'] = pd.to_datetime(df['transactionDateTime'])
print(df['transactionDateTime'].describe())

# Schema check
print(df.columns)

conn.close()
