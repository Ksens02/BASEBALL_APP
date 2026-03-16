import pandas as pd
import sqlite3
from pathlib import Path

# Define database name
db_name = "baseball.db"

# Delete existing database if it exists
if Path(db_name).exists():
    Path(db_name).unlink()
    print(f"Removed existing {db_name}")

# Connect to SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Load CSV files
print("Loading CSV files...")
people_df = pd.read_csv("people.csv")
teams_df = pd.read_csv("teams .csv")  # Note the space in the filename
batting_df = pd.read_csv("batting.csv")

print(f"Loaded people.csv: {len(people_df)} rows")
print(f"Loaded teams.csv: {len(teams_df)} rows")
print(f"Loaded batting.csv: {len(batting_df)} rows")

# Create people table with playerID as primary key
print("\nCreating people table...")

# Define column types for people table
people_dtypes = {
    'ID': 'INTEGER',
    'playerID': 'TEXT',
    'birthYear': 'INTEGER',
    'birthMonth': 'INTEGER',
    'birthDay': 'INTEGER',
    'birthCity': 'TEXT',
    'birthCountry': 'TEXT',
    'birthState': 'TEXT',
    'deathYear': 'REAL',
    'deathMonth': 'REAL',
    'deathDay': 'REAL',
    'deathCountry': 'TEXT',
    'deathState': 'TEXT',
    'deathCity': 'TEXT',
    'nameFirst': 'TEXT',
    'nameLast': 'TEXT',
    'nameGiven': 'TEXT',
    'weight': 'REAL',
    'height': 'REAL',
    'bats': 'TEXT',
    'throws': 'TEXT',
    'debut': 'TEXT',
    'bbrefID': 'TEXT',
    'finalGame': 'TEXT',
    'retroID': 'TEXT'
}

# Create column definition string for people table
people_cols = []
for col in people_df.columns:
    dtype = people_dtypes.get(col, 'TEXT')
    if col == 'playerID':
        people_cols.append(f"`{col}` {dtype} PRIMARY KEY")
    else:
        people_cols.append(f"`{col}` {dtype}")

cursor.execute(f"CREATE TABLE people ({', '.join(people_cols)})")

# Insert data into people table
for _, row in people_df.iterrows():
    placeholders = ','.join(['?' for _ in people_df.columns])
    cursor.execute(f"INSERT INTO people VALUES ({placeholders})", tuple(row))

conn.commit()

# Create teams table with teamID and yearID as composite primary key
print("Creating teams table...")

# Define column types for teams table
teams_dtypes = {}
for col in teams_df.columns:
    if col in ['yearID', 'Rank', 'G', 'Ghome', 'W', 'L', 'R', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'SB', 'CS', 'HBP', 'SF', 'RA', 'ER', 'CG', 'SHO', 'SV', 'IPouts', 'HA', 'HRA', 'BBA', 'SOA', 'E', 'DP']:
        teams_dtypes[col] = 'INTEGER'
    elif col in ['ERA', 'FP', 'BPF', 'PPF']:
        teams_dtypes[col] = 'REAL'
    else:
        teams_dtypes[col] = 'TEXT'

# Create column definition string for teams table
teams_cols = []
for col in teams_df.columns:
    dtype = teams_dtypes.get(col, 'TEXT')
    teams_cols.append(f"`{col}` {dtype}")

teams_cols.append("PRIMARY KEY (`teamID`, `yearID`)")

cursor.execute(f"CREATE TABLE teams ({', '.join(teams_cols)})")

# Insert data into teams table
for _, row in teams_df.iterrows():
    placeholders = ','.join(['?' for _ in teams_df.columns])
    cursor.execute(f"INSERT INTO teams VALUES ({placeholders})", tuple(row))

conn.commit()

# Create batting table with playerID, yearID, stint as composite primary key
# and foreign keys to people and teams
print("Creating batting table...")

# Define column types for batting table
batting_dtypes = {}
for col in batting_df.columns:
    if col in ['yearID', 'stint', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'IBB', 'HBP', 'SH', 'SF', 'GIDP']:
        batting_dtypes[col] = 'INTEGER'
    else:
        batting_dtypes[col] = 'TEXT'

# Create column definition string for batting table
batting_cols = []
for col in batting_df.columns:
    dtype = batting_dtypes.get(col, 'TEXT')
    batting_cols.append(f"`{col}` {dtype}")

batting_cols.append("PRIMARY KEY (`playerID`, `yearID`, `stint`)")
batting_cols.append("FOREIGN KEY (`playerID`) REFERENCES people(`playerID`)")
batting_cols.append("FOREIGN KEY (`teamID`, `yearID`) REFERENCES teams(`teamID`, `yearID`)")

cursor.execute(f"CREATE TABLE batting ({', '.join(batting_cols)})")

# Insert data into batting table
for _, row in batting_df.iterrows():
    placeholders = ','.join(['?' for _ in batting_df.columns])
    cursor.execute(f"INSERT INTO batting VALUES ({placeholders})", tuple(row))

conn.commit()

# Verify the database structure
print("\n=== Database Structure ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables created: {[t[0] for t in tables]}")

for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"\n{table_name} table:")
    for col in columns:
        print(f"  {col[1]}: {col[2]}")

# Check for foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")
conn.commit()

print(f"\n✓ Database '{db_name}' created successfully!")
print(f"  - people table: {len(people_df)} rows (Primary key: playerID)")
print(f"  - teams table: {len(teams_df)} rows (Primary key: teamID, yearID)")
print(f"  - batting table: {len(batting_df)} rows (Primary key: playerID, yearID, stint)")

conn.close()
