#Handles automatic loading of data set into the Database, with Pandas library support. 

import os
import pandas as pd
import sqlite3
#os library allows python to interact with the file system
from dotenv import load_dotenv

#Load dynamic Configuration from .env
load_dotenv()

#ENVIRONMENT SETUP
def import_all_data():
    #Data base path from .env 
    db_path = os.getenv('DATABASE_URL')

    #ENSURE THE INSTANCE FOLDER EXISTS. This is especially for local files and configuration that shouldn´t.
    # be commited to version control.    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    #DATABASE CONNECTION 
    #Using db_path variable to use the dynamic Data base connection specified on .env configuratino. 
    conn = sqlite3.connect(db_path)

    #DATA IMPORT AND TRANSFORMATION (Normalized tables)

    #To use linked tables for the relational schema between tables.
    # --- Table 1: Incidents (Main table)---
    df_incidents = pd.read_csv(os.getenv('INCIDENTS_CSV'))
    #Cleaning data, looking for additional spaces on headers
    df_incidents.columns = df_incidents.columns.str.replace(' ', '').str.replace('(', '').str.replace(')', '')
    df_incidents.to_sql('incidents', conn, if_exists='replace', index=False) #index False prevents Pandas for adding an extra ID colum when is not requiered. 
    print (f"SucCess {len(df_incidents)} records imported into 'incidents' table")


    # --- Table 2: Countries (Lookup Table) ---
    df_countries = pd.read_csv(os.getenv('COUNTRIES_CSV'))
    #Cleaning data, looking for additional spaces on headers
    df_countries.columns = df_countries.columns.str.replace(' ', '').str.replace('(', '').str.replace(')', '')
    #to_sql take the data from the CSV file and put into the DataBase table inside SQLLite. Instead of writing INSERT TO for all rows. 
    df_countries.to_sql('countries', conn, if_exists='replace', index=False)
    print (f"Sucess {len(df_countries)} records imported into 'countries' table")

    # --- Table 3: Attack Types (Lookup Table) ---
    df_attacks = pd.read_csv(os.getenv('ATTACK_TYPES_CSV'))
    #Cleaning data, looking for additional spaces on headers
    df_attacks.columns = df_attacks.columns.str.replace(' ', '').str.replace('(', '').str.replace(')', '')
    df_attacks.to_sql('attack_types', conn, if_exists='replace', index=False)
    print (f"Sucess {len(df_attacks)} records imported into 'attack_types' table")

    #VERIFICATION 
    print("Verification Complete")
    print("Incidents Table Columns:", df_incidents.columns.tolist())
    #tolist use to convert into a Python list, for after use of this output headers in the program. 

    #5. CLOSE CONNECTION 
    conn.close()

#EXECUTION CONTROL
#Ensures this block acts as a reusable module. Can be reuse by other components such as test.py as a whole module without triggering a full database import process automatically. 
if __name__ == "__main__":
    import_all_data()
