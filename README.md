Streaming Catalog Dashboard

Project Overview
This project is a data analysis dashboard that compares streaming platforms — Netflix, HBO Max, AppleTV+, Amazon Prime Video, and others — across multiple dimensions including catalog size, content quality, genre trends, and geographic reach. The core focus of the project is the integration of SQL directly inside Python code, where every query is written inside a dedicated Python function, creating a clean and structured data pipeline from database to dashboard.

Tech Stack
Python - Core logic, functions, error handling
MySQL - Database storage and Querying
Mysql-connector-python - Python to MySQL connector
Pandas - Data transformation and DataFrame handling
Streamlit - Dashboard display
Plotly Express - Interactive chart 

Database Setup
Prerequisites
Python
MySQL

Process
Step 1 - Clone the repository - git clone https://github.com/ritwika-dey26/Redi.git

Step 2 - Create a virtual environment

Step 3 - Install the dependencies - pip install -r requirements.txt

Step 4 - Setup the database in two ways- 
1. Open MySQL client and run
CREATE DATABASE streaming_db;
USE streaming_db;
SOURCE db.sql;

2. Open the terminal and run
mysql -u root -p streaming_db < db.sql

Step 5 - Update the credentials in the “get_connection” section 
Step 6 - Run Python - streamlit run genre_analysis.py

http://localhost:8501 - This page will automatically open with the dashboards

Author
Ritwika Dey
