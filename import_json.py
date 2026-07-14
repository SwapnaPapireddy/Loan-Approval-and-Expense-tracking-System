import json
import psycopg2

# ---- 1. Connect to PostgreSQL ----
conn = psycopg2.connect(
    host="localhost",
    database="exp_ense_dbs",
    user="postgres",
    password="70762"
)
cursor = conn.cursor()

cursor.execute("SELECT current_database();")
print("Connected Database:", cursor.fetchone()[0])

# ---- 2. Make sure the table exists with the right columns ----
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bankdata (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        account_number VARCHAR(20) UNIQUE NOT NULL,
        amount NUMERIC(12, 2) NOT NULL
    );
""")
conn.commit()

# ---- 3. Load the JSON file ----
with open("bank_records.json", "r", encoding="utf-8") as file:
    bankdata = json.load(file)

# ---- 4. Insert records ----
inserted_count = 0
try:
    for emp in bankdata:
        cursor.execute(
            """
            INSERT INTO bankdata (name, account_number, amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (account_number) DO NOTHING;
            """,
            (
                emp["name"],
                emp["account_number"],
                emp["amount"]
            )
        )
        inserted_count += cursor.rowcount  # rowcount is 1 if inserted, 0 if skipped

    conn.commit()
    print(f"{len(bankdata)} records processed.")
    print(f"{inserted_count} new records inserted successfully.")
    print(f"{len(bankdata) - inserted_count} records skipped (duplicates).")

except Exception as e:
    conn.rollback()
    print(f"Error during import: {e}")

finally:
    cursor.close()
    conn.close()