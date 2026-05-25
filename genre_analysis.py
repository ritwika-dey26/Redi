import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritwika@2026",
        database="demo")
    return conn

def fetch_platform_size():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        select platform, 
        total_titles,
        avg_imdb
        from platform_summary 
        where total_titles > 200
        order by avg_imdb DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_platform_quality():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        select platform, 
        total_titles,
        avg_imdb,
        avg_rt,
        avg_votes,
        total_awards
        from platform_summary 
        where total_titles > 200
        and avg_imdb > 6.5
        order by avg_imdb DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_yearly_trends():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT release_year,
        total_titles,
        movies,
        tv_shows,
        avg_imdb
        FROM yearly_release_trends
        where release_year >= 2000
        ORDER BY release_year ASC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_country_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT * FROM country_summary
        ORDER BY total_titles DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

"""
rows = fetch_platform_summary()
df = pd.DataFrame(rows)
print(df)

"""

def dashboard():
    st.title("Platform Analysis Dashboard")
    st.subheader("Platform Size Analysis")
    df = pd.DataFrame(fetch_platform_size())
    fig = px.bar(df, x='platform', y='total_titles', color='avg_imdb', title='Total Titles by Platform (Color by Avg IMDb)')
    st.plotly_chart(fig)
    
    