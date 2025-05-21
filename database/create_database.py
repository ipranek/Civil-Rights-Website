import pandas as pd 
import sqlite3
import numpy as np 
import os

country_scores = pd.read_csv("/Users/ipekoner/Desktop/programming/personal_website/data/cleaned_countryscore_data.csv")
country_items = pd.read_csv("/Users/ipekoner/Desktop/programming/personal_website/data/cleaned_incidents2.csv")

print(country_items.head())  # Check the first few rows of the 'country_items' DataFrame
print(country_scores.head())



# Convert Year and Score columns to numeric in country_scores
#country_items['Year of incident'] = pd.to_numeric(country_items['Year of incident'], errors='coerce').astype('Int64')

country_scores['Year'] = pd.to_numeric(country_scores['Year'], errors='coerce')
country_scores['Score'] = pd.to_numeric(country_scores['Score'], errors='coerce')

# country_scores = pd.read_csv("../data/cleaned_countryscore_data.csv")
# country_items = pd.read_csv("../data/cleaned_incidents_.csv")

conn = sqlite3.connect("relational_database.db")

cursor = conn.cursor()
print("Dropping existing tables...")
cursor.execute("DROP TABLE IF EXISTS country")
cursor.execute("DROP TABLE IF EXISTS score_table")
cursor.execute("DROP TABLE IF EXISTS item_table")

print("Creating new tables...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS country( 
            name TEXT PRIMARY KEY
            );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS score_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Country TEXT,
        Year INTEGER,
        Metric TEXT,
        Score INTEGER,
        FOREIGN KEY(Country) REFERENCES country(name)
        );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "Incident name" TEXT,
        "Brief description of the incident" TEXT,
        "What is the motive? Why is the state cracking down? (if known)" TEXT,
        "Country where incident took place" TEXT,
        "Date of incident" TEXT,
        "Year of incident" TEXT,
        FOREIGN KEY("Country where incident took place") REFERENCES country(name)
    );
""")

print("Committing changes...")
conn.commit()

country_items["Country where incident took place"] = country_items["Country where incident took place"].replace("Turkey", "Türkiye")
country_scores["Country"] = country_scores["Country"].replace("Turkey", "Türkiye")

print("Inserting country data...")
countries = country_items[['Country where incident took place']].drop_duplicates()
countries.columns = ["name"]
print(countries.head, country_scores)
countries.to_sql("country", conn, if_exists = "append", index = False)

print("Inserting score data...")
country_scores.to_sql("score_table", conn, if_exists = "append", index=False)

print("Inserting incident data...")
country_items.to_sql("item_table", conn, if_exists = "append", index = False)

conn.commit()
conn.close()


