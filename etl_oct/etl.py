import pandas as pd
import sqlite3
from datetime import datetime

class ETLError(Exception):
    pass

def run_etl(csv_file, db_file="bank.db"):
    try:
        # Extract
        try:
            df = pd.read_csv(csv_file)
            print(f"the extracted file is : \n {df.head()} ")
            if df.empty:
                raise ETLError("CSV file is empty!")
        except FileNotFoundError:
            raise ETLError(f"CSV file '{csv_file}' not found.")
        except pd.errors.ParserError as e:
            raise ETLError(f"Error parsing CSV: {e}")

        # Transform
        try:
            # 1. Fill missing balances with 0
            df['balance'] = df['balance'].fillna(0)

            # 2. Ensure all balances are non-negative floats
            df['balance'] = df['balance'].apply(lambda x: float(x) if isinstance(x, (int, float)) and x >= 0 else 0)

            # 3. Standardize customer names to title case
            df['customer_name'] = df['customer_name'].astype(str).str.title()

            # 4. Convert last_transaction to datetime format
            df['last_transaction'] = pd.to_datetime(df['last_transaction'], errors='coerce')

            # 5. Add a new column: 'is_active' based on recent transaction (within 90 days)
            today = pd.Timestamp(datetime.today())
            df['is_active'] = df['last_transaction'].apply(
                lambda x: (today - x).days <= 90 if pd.notnull(x) else False
            )
            print(f"Final File is : \n {df.head()}")
        except Exception as e:
            raise ETLError(f"Transformation failed: {e}")

        # Load
        try:
            conn = sqlite3.connect(db_file)
            df.to_sql("accounts", conn, if_exists="replace", index=False)
            conn.close()
        except sqlite3.Error as e:
            raise ETLError(f"Database error: {e}")

        print("ETL Completed Successfully!")

    except ETLError as e:
        print(f" ETL Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    run_etl("bank_data.csv")
