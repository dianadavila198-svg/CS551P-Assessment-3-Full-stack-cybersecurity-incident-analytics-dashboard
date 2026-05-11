#---- SET UP ----
import os 
import sqlite3
import pandas as pd
from flask import Flask, render_template
from dotenv import load_dotenv

#Load dynamic configuration from .env
load_dotenv()
#Data base path
db_path = os.getenv('DATABASE_URL')

#Helper function for DataBase connection, to reuse with all routes and for app scalability. 
def get_db_connection():
    #Open the connection to the data base
    conn = sqlite3.connect(db_path)
    #Enable accessing data by column names
    conn.row_factory = sqlite3.Row
    return conn

#Initialize app 
app = Flask(__name__)


#----HOME PAGE LOGIC (lIST VIEW)----

#App routing for mapping the URLS to a specific function that will handle the logic for that URL. 
# In our application, the URL ('/') means the home page
@app.route('/')
def index():
    #Stablish connection with data base with function helper. 
    conn = get_db_connection()
    # (DESC LIMIT 10) Select the top 10 incidents sorted by Year and Financial loss
    sql_top_10= "SELECT * FROM incidents ORDER BY Year DESC, [Financial_Loss_inMillion$] DESC LIMIT 10"
    #Grabs all matching records and stores them in the 'rows' variable
    #Run 'execute' directly so SQLite creates internally a temporary cursor 
    rows = conn.execute(sql_top_10).fetchall()
    #Close connection after finding rows
    conn.close()

    #----DATA ANALYSIS ----
    #Load the incidents table into a DataFrame for data analysis with pandas lirary
    #Read Data Base path into a data frame (df) so its readable with pandas library (as 2 dimensional data structure)
    analysis_global = sqlite3.connect(db_path)
    df_incidents = pd.read_sql_query("SELECT * FROM incidents", analysis_global)

    #Load attach_types table to link it with incidents table
    try:
        df_attacks = pd.read_sql_query("SELECT * FROM  attack_types", analysis_global)
    except:
        #work around, to load from CSV in case the table is not in the database yet
        df_attacks = pd.read_csv('attack_types.csv')

    #---TABLE JOINNIN---
    #Join incidents with attack_types using incident ID colum (primary key)
    #left_on=,right_on= specifies in what level to do the merging on the DataFrame to the left-right.
    df_merged = df_incidents.merge(df_attacks, left_on='Attack_typeID', right_on='Type_ID')

    #Calculate average loss and Average Resolution per Defense Used with Attack type.
    #convert it into a dicionary for HTML template readiness
    #.mean() to calculate the average loss for each defense type
    #.sort_values() organize the results, showing from the lowest average loss to the highest
    #.to_dict() for easier readiness for HTML templates in python dictionary
    #agg as aggregate. Enable to run multiple different calculations
    #'mean' for average value calculation
    # Find the colum names to avoid key errors, looking by keywords.
    col_loss = [c for c in df_merged.columns if 'Financial_Loss' in c][0]
    col_time = [c for c in df_merged.columns if 'Resolution_Time' in c][0]
    col_attack = [c for c in df_merged.columns if 'Attack' in c and 'ID' not in c][0]
    col_defense = [c for c in df_merged.columns if 'Defense' in c and 'ID' not in c][0]

    #Run multi-Dimensional Analysis using the found names
    performance_stats = df_merged.groupby([col_defense, col_attack]).agg({
    col_loss: 'mean',
    col_time: 'mean'
    }).sort_values(col_loss, ascending=False).head(6).to_dict('index')

    #Get top 5 countries with the highest total financial loss
    #.sort_values() organize the results, showing from the lowest average loss to the highest
    #.to_dict() for easier readiness for HTML templates in python dictionary
    country_stats = df_incidents.groupby('Country')['Financial_Loss_inMillion$'].sum().sort_values().to_dict()

     
    #---DASHBOARD VISUALIZATION---
    #Summarize total financial loss 
    total_loss_raw = df_incidents['Financial_Loss_inMillion$'].sum()
    #Format the number as billions or millions for easier user readiness
    if total_loss_raw >= 1000:
        total_loss = f"${round(total_loss_raw/1000,2)} USD Billions"
    else:
        total_loss = f"${round(total_loss_raw,2)} USD Millions"
    
    #Find the top 3 most common type of attacks
    #.head(3) to keep only the top 3 values
    #tolist() to convert it into a list for easier readiness
    top_3 = df_incidents['Attack_Type'].value_counts().head(3).index.tolist()

    #['Attack_Type'] python grab the incidents table and grab only the column "Attack_Type"
    #Add else "N/A" for error handling
    primary_threat = top_3[0] if len(top_3) > 0 else "N/A"
    secondary_threat = top_3[1] if len(top_3) > 1 else "N/A"
    third_threat = top_3[2] if len(top_3) > 2 else "N/A"

    #Count total number of rows in the dataset
    total_incidents = len(df_incidents)

    #---RENDER TEMPLATE ---
    #Send all variables to 'index.html' 
    return render_template('index.html', 
                           rows=rows,
                           total_loss=total_loss,
                           primary_threat = primary_threat, 
                           secondary_threat = secondary_threat,
                           third_threat = third_threat,
                           total_incidents = total_incidents,
                           performance_stats = performance_stats,
                           country_stats = country_stats)

#MAIN TEMPLATE LAYOUT (index & detail to plug into)
#<int:incident_id define ID as int variable, called 'incident_id'
@app.route('/incident/<int:incident_id>')
def detail(incident_id):
    #Helper to get Data Base connection
    conn = get_db_connection()

    #Using '?' to delimeter queries and prevent SQL injection. 
    #fetchone() to return a single specific object,becuase IDs are unique. This for memory efficiency. 
    #(incident_id,) tuple with comma,helps to pass variables into SQL queries safely. 
    incident = conn.execute("SELECT * FROM incidents WHERE Incident_ID = ?", (incident_id,)).fetchone()
    #Close connection to Data Base
    conn.close()

    #Validation to validate that the incident exists
    if incident is None:
        return "Incident not found"
    
    #Send the specific record to the detail page 
    return render_template('detail.html', incident=incident)

#EXECUTION CONTROL
#Ensures app.py acts as a resusable module. This allows other tools such as tests.py
#to import the Flask app configuration without actually starting the web server until 
#I explicity tell it to
if __name__ == "__main__":
    #app.run(debug=True) triggers the local development server
    #1) Automaticallly restarts the server when the code changes
    #2)Iterative debugger, provides detail error details directly in the browser for troubleshooting
    #Automatically reload the server, live update
    #Iterative debugger in case there is an error send a clear message or error, for coding debug. 
    app.run(debug=True)