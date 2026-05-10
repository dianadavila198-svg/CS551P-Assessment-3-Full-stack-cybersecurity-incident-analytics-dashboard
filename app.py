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

#App routing for mapping the URLS to a specific function that will handle the logic for that URL. 
# In our application, the URL ('/') means the home page
@app.route('/')

#HOME PAGE LOGIC (lIST VIEW)
def index():
    #Stablish connection with data base function helper. 
    conn = get_db_connection()
    #Execute the query to select all data from 'incidents' table
    #Grabs all matching records and stores them in the 'rows' variable
    #Run 'execute' directly so SQLite creates internally a temporary cursor 
    rows = conn.execute("SELECT * from incidents").fetchall()
    #Terminates the connection 
    conn.close()

    #----GLOBAL DATA ANALYSIS ----
    #Read Data Base path into a data frame (df) so its readable with pandas library (as 2 dimensional data structure)
    df = pd.read_sql_query("SELECT * FROM incidents", sqlite3.connect(db_path))
    #Calculate total financial loss
    total_loss_raw = df['Financial_Loss_inMillion$'].sum()
    if total_loss_raw >= 1000:
        total_loss = f"${round(total_loss_raw/1000,2)} USD Billions"
    else:
        total_loss = f"${round(total_loss_raw,2)} USD Millions"
    
    #Identify the threat (attack_type) more frecuent
    #df['Attack_Type'] python grab the big table (df) and grab only the column "Attack_Type"
    primary_threat = df['Attack_Type'].mode()[0]

    #Count total records
    total_incidents = len(df)

    #Passes the data to 'index.html' 
    return render_template('index.html', 
                           rows=rows,
                           total_loss=total_loss,
                           primary_threat = primary_threat, 
                           total_incidents = total_incidents)

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