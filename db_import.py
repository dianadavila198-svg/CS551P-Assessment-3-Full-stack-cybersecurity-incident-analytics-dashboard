#Model: Handles automatic loading of open data into SQLite Database

import pandas as pd
import sqlite3
import os

#1. ENVIRONMENT SETUP
# Ensures the 'instance' folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

#2. DATABASE CONNECTION 
#This creates or opens the SQLite file. Using instance for mananing local data. 
#Connection to SQLite 
conn = sqlite3.connect('instance/cyber_data.db')

#3. DATA IMPORT AND TRANSFORMATION 
#Import each CSV into its own dedicated SQL table (Normalization)
#To use linked tables for the relational schema between tables.

# --- Table 1: Incidents (Main table)---
df_incidents = pd.read_csv('incidents.csv')
df_incidents.to_sql('incidents', conn, if_exists='replace', index=False) #index False prevents Pandas for adding an extra ID colum when is not requiered. 
print (f"Sucess {len(df_incidents)} records imported into 'incidents' table")


# --- Table 2: Countries (Lookup Table) ---
df_countries = pd.read_csv('countries.csv')
#to_sql take the data from the CSV file and put into the DataBase table inside SQLLite. Instead of writing INSERT TO for all rows. 
df_countries.to_sql('countries.csv', conn, if_exists='replace', index=False)
print (f"Sucess {len(df_countries)} records imported into 'countries' table")

# --- Table 2: Attack Types (Lookup Table) ---
df_attacks = pd.read_csv('attack_types.csv')
df_attacks.to_sql('attack_types.csv', conn, if_exists='replace', index=False)
print (f"Sucess {len(df_attacks)} records imported into 'attack_types' table")

#4. VERIFICATION 
print("Incidents Table Columns:", df_incidents.columns.tolist())
#tolist use to convert into a Python list, for after use of this output headers in the program. 

#5. CLOSE CONNECTION
conn.close()