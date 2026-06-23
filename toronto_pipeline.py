import requests
import pandas as pd
import pyodbc

print("📡 Connecting to City of Toronto Open Data Portal...")
api_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
params = {"id": "apartment-building-evaluation"}
response = requests.get(api_url, params=params).json()
resources = response["result"]["resources"]

# Find the official active CSV dataset link
csv_url = None
for r in resources:
    if r["format"].lower() == "csv" and "current" in r["name"].lower():
        csv_url = r["url"]
        break

if not csv_url:
    csv_url = [r["url"] for r in resources if r["format"].lower() == "csv"][0]

print(f"📥 Found live CSV file. Downloading evaluation entries...")
df = pd.read_csv(csv_url)

# Exact column mappings from your specific terminal output
id_col = '_id'
address_col = 'SITE ADDRESS'
score_col = 'CURRENT BUILDING EVAL SCORE'
ward_col = 'WARD'
ward_name_col = 'WARDNAME'

# Force the score column to be numbers, turning any weird text into blank spaces (NaN)
df[score_col] = pd.to_numeric(df[score_col], errors='coerce')

# Drop any blank rows where there is no score
df_clean = df.dropna(subset=[score_col])
records_to_load = df_clean.head(500) # Load 500 rows for lightning speed

print(f"🗄️ Connecting to local SQL Server...")
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"  # Kept your working server connection path
    "Database=TorontoHousing;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Clear table to keep it fresh
cursor.execute("TRUNCATE TABLE BuildingEvaluations;")

print(f"⚡ Streaming records into SQL Server...")
for index, row in records_to_load.iterrows():
    rec_id = int(row[id_col])
    address = str(row[address_col])
    score = float(row[score_col])
    ward_val = str(row[ward_col])
    ward_name_val = str(row[ward_name_col])

    cursor.execute(
        """
        INSERT INTO BuildingEvaluations (RecordID, SiteAddress, SafetyScore, Neighbourhood, Ward)
        VALUES (?, ?, ?, ?, ?)
        """,
        rec_id, address, score, ward_name_val, ward_val
    )

conn.commit()
cursor.close()
conn.close()
print("🏆 Victory! Toronto public housing pipeline successfully loaded to SQL Server.")