import sqlite3

# Connect to database (file will be created automatically)
conn = sqlite3.connect("data/loan_applications.db")

# Read schema file
with open("sql/schema.sql", "r") as file:
    schema_sql = file.read()

# Execute schema
conn.executescript(schema_sql)

conn.close()

print("✅ Database created successfully.")