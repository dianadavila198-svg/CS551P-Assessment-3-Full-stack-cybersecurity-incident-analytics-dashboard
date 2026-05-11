# Assessment 3 for Advanced programming

## 1. PROJECT OVERVIEW
This program is a python based application designed to visualize and analyze global cybersecurity incidents from 2019 to 2024. The system focuses on data analysis using Pandas and web development with Flask to organize a dataset of over 3,000 records from an open data source.

1) Open source data (downloaded from kaggle)
https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024?resource=download

2) This application was developed according with the evaluation criteria specified in the assignment instructions for this course. 

## 2. LIVE URL 
The application is successfully published in a production environment via Render.https://cs551p-assessment-3-cybersecurity.onrender.com/

## 3. DEPLOYMENT & VERSION CONTROL
Git Hub : A connection with GitHub was established to facilitate version control. This allows for detailed tracking of code changes and provides full transparency into the development process and system architecture.

## 4. FULL STACK DESIGN
The project uses a modular approach to separate logic, structure, and design:

1) Python: Core logic implementing Object-Oriented Programming (OOP) and Flask routing.
2) HTML (Jinja): Dynamic front-end templates utilizing the Jinja engine for data rendering.
3) CSS: Custom stylesheets designed to provide a professional, responsive user interface for the dashboard.

## 5. HOW TO START?
### Option 1. Access Online
1) URL live app: https://cs551p-assessment-3-cybersecurity.onrender.com/

Important!**the application is hosted on a free tier and may require 30–60 seconds to "wake up" on the first visit due to render server sleep mode while not traffic. Render shows clearly while the application is loading. 

### Option 2. Execute the program locally on your machine
### Pre-requisites (on local machine)
1) Ensure you have Python 3 installed
2) Create and activate a virtual environment (optional but recommended).
2) Download the project folder & unzip it. (Make sure all files, including the SQLite database, remain in the same folder).
3) Open your terminal or command prompt and navigate to the project directory.
3) Run in the terminal 'pip install -r requirements.txt'.To install the libraries listed on the requirements.txt file. 
4) Execute program Type 'python app.py'
5) Open the browser and go to http://127.0.0.1:5000/

## 6. END USER NAVIGATION
The application is developed to transition seamless from global high level data analysis to granular record visualization. Below is the navigation path to follow for better visualization of app functionality:

### Home View (Summary data analysis)
1) The home page instantly pulls from the SQLite database to show the Global Financial Impact and the total number of records.

2) Custom charts (built with Flask and CSS) compare Defense vs. Attack Type efficiency and highlight the Top 10 Countries by financial loss. This view represent the more complex view of all analysis, merging different tables in the data base with SQL JOIN. 

3) Critical Recent Incidents to keep the interface showing the top lately incidents. 

### Historical View 
1) Clicking "View All Historical Records" uses a URL parameter (?all=true),hiding the charts and expanding the table to show the full 3,000+ record history.

### Granular Visualization (Incident Details)
1) Under "Actions" in "Critical Recent Incidents" click on "View Details" to view granular incident details. Here the data is fixed from the data set, separated by different card visualizators "General Information", "Technical Anlaysis" and "Impact Assessment" taking different fields across the main table for granular visualization. 

### Navigation Buttons
Navigation buttons are placed at the top of every table and detail page, allowing to jump back to the main dashboard, to the granular & historical view. 

## 7. TESTS
To ensure system correct functionality, follow the below steps to execute the automated tests:

1) Install pytest: pip install pytest
2) Run tests with detailed output: pytest -v
3) Testing Focus

Unit Testing: Verified that routes return a 200 OK status code and that the home page loads correctly.

Data Validation: Ensured Pandas correctly aggregates financial losses and threat counts from the SQLite source.

Toggle Logic: Tested the logic to confirm that the UI correctly hides or reveals dashboard components based on user navigation.

4) Validate Output. Expected Output: 
test_app.py::test_home_page_loads PASSED 
test_app.py::test_history_toggle PASSED 
test_app.py::test_incident_detail_loads PASSED 

## 8. CODE DEVELOPMENT PROCESS & GOOD PRACTICES FOLLOWED
1) Version Control: Used Git consistently with descriptive commits to track version history.
2) Data Comparison: Rather than just listing data, the app analyzes defense efficiency and financial comparisons.
3) Relational Schema connection & Normalized tables. A draft in paper was done before the start of code for data upload. 
3) Component Architecture: Logic was separated into appropriate files to ensure maintainability.

## 9. APPLICATION FILES ARQUITECTURE

│
├── instance/               # Database storage 
│   └── cyber_data.db       # SQLite database file
│
├── static/                 # CSS
│   └── style.css           # Web Page Styling
│
├── templates/              # HTML files
│   ├── base.html           # "Master" layout (Composite template)
│   ├── index.html          # Main dashboard
│   └── detail.html         # Individual record view
│
├── venv/                   # Virtual Environment 
│
├── .env                    # Configurations 
├── .gitignore              # Tells Git what to ignore 
├── app.py                  # The main Flask application controller
├── db_import.py            # Script to load CSV to SQL 
├── incidents.csv           # Raw open data source 
├── requirements.txt        # List of libraries needed to execute the program (Flask, Pandas, etc.)
├── README.md               # Documentation 
└── tests.py                # Unit tests to validate app proper functionality 

## 10. GIT HUB DOCUMENTATION
Refer to the below link for more detail on project construction, commits, and code push on git hub cloud. https://github.com/dianadavila198-svg/CS551P-Assessment-3

## ADDITIONAL NOTES
This project was developed for the course CS551P - Advanced Programming

## AI ACKNOWLEDGEMENT & SUPPORT
I acknowledge the use of AI as a supportive assistant during the development of this project. It was responsible used to help me understand and refine specific logic components, including:

1) Identification of syntax errors while troubleshooting. Such as variable errors with flask templates. 
2) Refining Jinja2 commands in templates. 
3) Refining Pandas commands for deeper data insights and optimizing CSS properties for the responsive bar charts.
4) Refining tests construction for pytest set up
5) CSS design for certain rules. 

## Author 
Diana Laura Davila Esparza
Student: 52534367
MsC IT with Cybersecurity




