import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv("c:/Users/nagam/Downloads/vehicle_logs.csv")

# Function to connect to SQLite database
def get_data(query, params=None):
    conn = sqlite3.connect("policelog_database.sqlite")
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.set_page_config(page_title="Securecheck police Dashboard", layout="wide")


#st.title("Traffic Police security Post Log Reports")

#st.markdown("🚥 **Traffic Police Security Post Log Reports**", unsafe_allow_html=True)
#st.markdown("<span style='color:blue;'>Real-time monitoring and insights for law enforcement 🚨</span>", unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Direct Into", ["Project Introduction", "Vehical logs Visualization", "SQL Queries","Predicted Violation","Creator Info"])

if page == "Project Introduction":
    st.title("🚥 Traffic Security Analysis")
    tab1,tab2=st.tabs(["Project Introduction","Police Post Log Database"])
    with tab1:
        st.image("https://static.vecteezy.com/system/resources/previews/002/928/462/original/the-traffic-policeman-waved-his-hand-signal-at-the-crosswalk-vector.jpg",)  # Adding GIF
        st.subheader("🚨 A Streamlit App for Exploring Traffice Security logs")
        st.write("""
        Police check posts require a centralized system for logging, tracking, and analyzing vehicle movements. 
        Currently, manual logging and inefficient databases slow down security processes. 
        This project aims to build an SQL-based check post database with a Python-powered dashboard for real-time insights and alerts
    
        **Features:**
        - Display vehicle logs, violations, and officer reports.
        - Implement SQL-based search filters for quick lookups.
        - Generate analytics and trends (e.g., high-risk vehicles)

    
        **Database Used:** `Policelog_database.sqlite`
        """)
    with tab2:
        st.header("Policelog_Database")
        total_database = "select * from policelog_data"
        data = get_data(total_database)
        st.dataframe(data, use_container_width=True)

elif page == "Vehical logs Visualization":
    st.header("📊 Visualization")
    # Creating columns
    col1, col2, col3, col4,col5 = st.columns(5)
# Adding content to the first column
    with col1:
        total_stops = data.shape[0]
        st.metric("Total Police Stops", total_stops)
    with col2:
        arrests=data[data['stop_outcome'].str.contains("arrest",case=False,na=False)].shape[0]
        st.metric("Total Arrests",arrests)
    with col3:
        warnings=data[data['stop_outcome'].str.contains("warning",case=False,na=False)].shape[0]
        st.metric("Total Warnings",warnings)
    with col4:
        tickets=data[data['stop_outcome'].str.contains("ticket",case=False,na=False)].shape[0]
        st.metric("Total Tickets",tickets)
    with col5:
        drunk_driving=data[data['violation_raw'].str.contains("Drunk Driving",case=False,na=False)].shape[0]
        st.metric("Total Drunk Driving",drunk_driving)  

    st.subheader("Key Metrics Visualization")

# Prepare data for chart
    metrics = {
        "Metric": ["Total Police Stops",   "Arrests",   "Warnings",   "Tickets",   "Drunk Driving"],
        "Count": [total_stops,  arrests,  warnings,  tickets,  drunk_driving]
    }
    metrics_df = pd.DataFrame(metrics)
    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(metrics_df["Metric"], metrics_df["Count"], color='skyblue')
    ax.set_ylabel("Count")
    ax.set_title("Key Metrics")

    # Display the chart in Streamlit
    st.pyplot(fig)
    st.header("Visual Insights")
    tab1,tab2=st.tabs(["stops by violation","Driver Gender Distribution"])
    with tab1:
        if not data.empty and 'violation_raw' in data.columns:
            violation_data = data['violation_raw'].value_counts().reset_index()
            violation_data.columns = ['violation_raw', 'count']  # Ensure column names are correct
            # Create the bar chart
            fig = px.bar(
            violation_data,
            x='violation_raw',
            y='count',
            title="Stops by Violation Type",
            )
            # Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
    
    
    # Display the chart in Streamlit
    
        else:
            st.warning("No data available for violation chart")

    with tab2:
        if not data.empty and 'driver_gender' in data.columns:
            gender_data = data['driver_gender'].value_counts().reset_index()
            gender_data.columns = ['Gender', 'count']  # Ensure column name is 'count'
            # Correct column name for 'values' parameter
            fig = px.pie(gender_data, names='Gender', values='count', title="Driver Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for driver gender chart")
            
elif page == "SQL Queries":
    st.title("📋 SQL Query Results")
    tab1,tab2=st.tabs(["Basic Acumen","Advanced Acumen"])
    with tab1:
        st.header("🔍Preliminary Analysis")
        query = {
        "1. Total Number of Police Stops": "SELECT COUNT(*) AS Total_stops FROM policelog_data",
        "2. Count of Stops by Violation Type": "sELECT violation, COUNT(*) AS Count FROM policelog_data GROUP BY violation",
        "3. Number of Arrests vs. Warnings" : "SELECT stop_outcome, COUNT(*) AS Count FROM policelog_data WHERE stop_outcome IN ('Arrest', 'Warning') GROUP BY stop_outcome",
        "4. Average Age of Drivers Stopped" : "SELECT AVG(driver_age) AS Average_Age FROM policelog_data WHERE driver_age IS NOT NULL",
        "5. Top 5 Most Frequent Search Types" : "SELECT search_type, COUNT(*) AS Frequency FROM policelog_data GROUP BY search_type ORDER BY Frequency DESC LIMIT 5",
        "6. Count of Stops by Gender" : "SELECT driver_gender, COUNT(*) AS Count FROM policelog_data GROUP BY driver_gender",
        "7. Most Common Violation for Arrests" : "SELECT violation, COUNT(*) AS Count FROM policelog_data WHERE is_arrested = True GROUP BY violation ORDER BY Count DESC",
        "8. Average Stop Duration for Each Violation" : "SELECT violation, AVG(stop_duration) AS Average_Duration FROM policelog_data GROUP BY violation",
        "9. Number of Drug-Related Stops by Year" : "SELECT strftime('%Y', stop_date) AS Year, COUNT(*) AS Drug_Related_Stops FROM policelog_data WHERE drugs_related_stop = True GROUP BY Year ORDER BY Year ASC",
        "10. Drivers with the Highest Number of Stops" : "SELECT vehicle_number,driver_age,COUNT(*) AS Stop_Count FROM policelog_data GROUP BY vehicle_number,driver_age ORDER BY Stop_Count DESC Limit 10",
        "11. Number of Stops Conducted at Night (Between 10 PM - 5 AM)" : "SELECT COUNT(*) AS Night_Stops FROM Policelog_data WHERE CAST(strftime('%H', stop_time) AS INTEGER) BETWEEN 22 AND 23 OR CAST(strftime('%H', stop_time) AS INTEGER) BETWEEN 00 AND 5",
        "12. Number of Searches Conducted by Violation Type" : "SELECT violation, COUNT(*) AS Search_Count FROM policelog_data WHERE search_conducted = True GROUP BY violation ORDER BY Search_Count DESC",
        "13. Arrest Rate by Driver Gender" : "SELECT driver_gender, COUNT(CASE WHEN is_arrested = 1 THEN 1 END) * 100.0 / COUNT(*) AS Arrest_Rate FROM policelog_data GROUP BY driver_gender",
        "14. Violation Trends Over Time (Monthly Count of Violations)" : "SELECT strftime('%Y-%m', stop_date) AS Month, violation, COUNT(*) AS Violation_Count FROM policelog_data GROUP BY Month, violation ORDER BY Month ASC, Violation_Count DESC",
        "15. Most Common Stop Outcomes for Drug-Related Stops" : "SELECT stop_outcome, COUNT(*) AS Outcome_Count FROM policelog_data WHERE drugs_related_stop = 1 GROUP BY stop_outcome ORDER BY Outcome_Count DESC"
        }
        selected_query = st.selectbox("Choose a Query", list(query.keys()))
        if st.button("Run Query", key="run_query_button"):
            query_result = get_data(query[selected_query])
            if not query_result.empty:
                st.write(query_result)
            else:
                st.warning("No result founds for the selected query")


    with tab2:
        st.header("📚Advanced Acumen")
        queries = {
        "1. Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)": "WITH YearlyData AS (SELECT country_name,strftime('%Y', stop_date) AS Year,COUNT(*) AS Total_Stops,SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS Total_Arrests FROM policelog_data GROUP BY country_name, Year),RankedData AS (SELECT country_name,Year,Total_Stops,Total_Arrests,RANK() OVER (PARTITION BY Year ORDER BY Total_Stops DESC) AS Rank_By_Stops FROM YearlyData)SELECT country_name,Year,Total_Stops,Total_Arrests,Rank_By_Stops FROM RankedData ORDER BY Year ASC, Rank_By_Stops",
        "2. Driver Violation Trends Based on Age and Race (Join with Subquery)": "SELECT driver_age,driver_race,violation,COUNT(*) AS Violation_Count FROM policelog_data WHERE violation IN (SELECT DISTINCT violation FROM policelog_data WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL)GROUP BY driver_age, driver_race, violation ORDER BY driver_age ASC, Violation_Count DESC",
        "3. Time Period Analysis of Stops (Joining with Date Functions)" : "SELECT strftime('%Y', stop_date) AS Year,strftime('%m', stop_date) AS Month,COUNT(*) AS Total_Stops,SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS Total_Arrests FROM policelog_data GROUP BY Year, Month ORDER BY Year ASC, Month ASC",
        "4. Correlation Between Age, Violation, and Stop Duration (Subquery)" : "SELECT driver_age,violation,AVG(stop_duration) AS Avg_Stop_Duration,(SELECT COUNT(*) FROM policelog_data AS SubQuery WHERE SubQuery.driver_age = MainQuery.driver_age AND SubQuery.violation = MainQuery.violation) AS Total_Stops FROM policelog_data AS MainQuery GROUP BY driver_age, violation ORDER BY driver_age ASC, Avg_Stop_Duration DESC",
        "5. Violations with High Search and Arrest Rates (Window Function)" : "WITH ViolationStats AS (SELECT violation,COUNT(*) AS Total_Stops,SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) AS Search_Count,SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS Arrest_Count FROM policelog_data GROUP BY violation) SELECT violation,Total_Stops,Search_Count,Arrest_Count,ROUND(Search_Count * 100.0 / Total_Stops, 2) AS Search_Rate,ROUND(Arrest_Count * 100.0 / Total_Stops, 2) AS Arrest_Rate FROM ViolationStats WHERE (Search_Count * 100.0 / Total_Stops) > 30 OR (Arrest_Count * 100.0 / Total_Stops) > 20 ORDER BY (Search_Count * 100.0 / Total_Stops) DESC, (Arrest_Count * 100.0 / Total_Stops) DESC",
        "6. Driver Demographics by Country (Age, Gender, and Race)" : "SELECT country_name,ROUND(AVG(driver_age), 2) AS Average_Age,COUNT(*) AS Total_Stops,SUM(CASE WHEN driver_gender = 'Male' THEN 1 ELSE 0 END) AS Male_Count,SUM(CASE WHEN driver_gender = 'Female' THEN 1 ELSE 0 END) AS Female_Count,SUM(CASE WHEN driver_race = 'White' THEN 1 ELSE 0 END) AS White_Count,SUM(CASE WHEN driver_race = 'Black' THEN 1 ELSE 0 END) AS Black_Count,SUM(CASE WHEN driver_race = 'Asian' THEN 1 ELSE 0 END) AS Asian_Count,SUM(CASE WHEN driver_race = 'Hispanic' THEN 1 ELSE 0 END) AS Hispanic_Count,SUM(CASE WHEN driver_race NOT IN ('White', 'Black', 'Asian', 'Hispanic') THEN 1 ELSE 0 END) AS Other_Race_Count FROM policelog_data WHERE driver_age IS NOT NULL GROUP BY country_name ORDER BY Total_Stops DESC",
        "7. Top 5 Violations with Highest Arrest Rates" : "SELECT violation,COUNT(*) AS Total_Stops,SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS Arrest_Count,ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_Rate FROM policelog_data GROUP BY violation ORDER BY Arrest_Rate DESC LIMIT 5"
    }
        selected_query = st.selectbox("Choose a Query", list(queries.keys()))
        if st.button("Advance Query", key="reset_query_button"):
            query_result = get_data(queries[selected_query])
            
            if not query_result.empty:
                st.write(query_result)
            else:
                st.warning("No result founds for the selected query")
            
            
elif page == "Predicted Violation":
        
    st.title("🚔Predicted Violation")
    st.image("https://img.freepik.com/premium-photo/vector-illustration-policeman-giving-driver-traffic-violation-ticket_977617-89276.jpg")
    st.header("Police Log Report")
    with st.form("New_Log_Form"):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        country_name = st.text_input("Country Name")
        driver_gender = st.selectbox("Driver Gender", ["male", "female"])
        driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
        driver_race = st.text_input("Driver Race")
        search_conducted = st.selectbox("Search Conducted", ["0", "1"])
        search_type = st.text_input("Search Type")
        drugs_related_stop = st.selectbox("Drug Related", ["0", "1"])
        stop_duration = st.selectbox("Stop Duration", data['stop_duration'].dropna().unique())
        vehicle_number = st.text_input("Vehicle Number")
        timestamp = pd.Timestamp.now()

        submitted = st.form_submit_button("Prediction of Police Log")

    if submitted:
        filtered_data = data[
            (data['driver_gender'] == driver_gender) &
            (data['driver_age'] == driver_age) &
            (data['search_conducted'] == int(search_conducted)) &
            (data['stop_duration'] == stop_duration) &
            (data['drugs_related_stop'] == int(drugs_related_stop))
            ]
        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"
    # Fixed typo in variable name and logic
        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

        # Corrected indentation and removed redundant st.markdown
        st.markdown(f"""
        🚕 A {driver_age}-year-old {driver_gender} driver in {country_name} was stopped for {predicted_violation} at {stop_time.strftime('%I:%M %p')} on {stop_date}, {search_text}, and the stop {drug_text}. 
        Stop duration: **{stop_duration}**, Vehicle Number: **{vehicle_number}**.""")



elif page == "Creator Info":
    st.title("👩‍💻 Creator of this Project")
    st.image("https://media.giphy.com/media/1ynCEtlgMPAeNAqdnu/giphy.gif")
    st.write("""
    **Developed by:** Preethi Nagamuthu 

    **Skills:** Python, SQL,Streamlit, Pandas   
    """) 

          
