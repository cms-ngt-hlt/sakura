import sqlite3

# Create merged database
merged_db = sqlite3.connect('merged.db')

# Attach source databases
merged_db.execute("ATTACH DATABASE 'local_database_1.db' AS db1;")
merged_db.execute("ATTACH DATABASE 'local_database_2.db' AS db2;")

# Get tables from the first source database
tables = merged_db.execute(
    "SELECT name FROM db1.sqlite_master WHERE type='table';"
).fetchall()

# Merge tables
for table in tables:
    table_name = table[0]
    
    # Create tables in merged.db
    schema = merged_db.execute(
        f"SELECT sql FROM db1.sqlite_master WHERE type='table' AND name='{table_name}';"
    ).fetchone()[0]
    merged_db.execute(schema)
    
    # Insert data with conflict handling
    merged_db.execute(f"INSERT INTO {table_name} SELECT * FROM db1.{table_name};")
    merged_db.execute(f"INSERT OR IGNORE INTO {table_name} SELECT * FROM db2.{table_name};")

# Commit and close
merged_db.commit()
merged_db.close()

print("Databases successfully merged into 'merged.db'.")
