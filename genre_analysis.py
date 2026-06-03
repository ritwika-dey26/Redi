import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="****",
            database="demo")
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def fetch_platform_size():
    conn = get_connection()
    if conn is None:
        return []
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
    if conn is None:
        return []
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
    if conn is None:
        return []
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
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT country,
        total_titles,
        avg_imdb,
        top_platform
        FROM country_summary
        ORDER BY total_titles DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def dashboard():
    st.title("Platform Analysis Dashboard")
    st.subheader("Platform Size Analysis")
    with st.spinner("Loading platform size data..."):
        df = pd.DataFrame(fetch_platform_size())
    if df.empty:
        st.warning("No data available for platform size analysis.")
    else:
        fig = px.bar(df, x='platform', y='total_titles', color='avg_imdb', title='Total Titles by Platform (Color by Avg IMDb)')
        st.plotly_chart(fig)
    
    st.subheader("Platform Quality Analysis")
    with st.spinner("Loading platform quality data..."):
        df2 = pd.DataFrame(fetch_platform_quality())
    if df2.empty:
        st.warning("No data available for platform quality analysis.")
    else:
        fig2 = px.bar(df2, x='platform', y='avg_imdb', color = "total_awards",title='Platform Quality Analysis (Avg IMDb by Platform)')
        st.plotly_chart(fig2)
    
    st.subheader("Content Growth Over Time")
    with st.spinner("Loading yearly trends data..."):
        df3 = pd.DataFrame(fetch_yearly_trends())
    if df3.empty:
        st.warning("No data available for yearly trends analysis.")
    else:
        fig3a = px.line(df3, x='release_year', y='total_titles', markers=True, title='Content Growth Over Time')
        st.plotly_chart(fig3a)
        fig3b = px.line(df3, x="release_year",y=["movies", "tv_shows"], markers=True, title="Movies vs TV Shows Over Time")
        st.plotly_chart(fig3b)
    
    st.subheader("Country Content Analysis")
    with st.spinner("Loading country summary data..."):
        df4 = pd.DataFrame(fetch_country_summary())
    if df4.empty:
        st.warning("No data available for country content analysis.")
    else:
        fig4 = px.bar(df4, x='total_titles', y='country', orientation='h', color='avg_imdb', title='Top Countries by Content Output')
        st.plotly_chart(fig4)
        fig5 = px.bar(df4, x = "country", y = "avg_imdb", color = "total_titles", title = "Country Quality Ranking")
        st.plotly_chart(fig5)
    
dashboard()
