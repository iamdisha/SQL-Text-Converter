from dotenv import load_dotenv
load_dotenv() ##load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai 

## configure genai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load Googlr gemini Model and provide queries as response
##llm model ka kaam is generating the query
#prompt what gemini pro model needs to behave like
def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0], question])
    return response.text

#functionto retreive query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    

    for row in rows:
        print(row)
    return rows

## define your prompt
prompt=[
    """
 You are an expert in converting English questions to SQL query!
      The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
      SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
      the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
      \nExample 2 - Tell me all the students studying in Data Science class?, 
      the SQL command will be something like this SELECT * FROM STUDENT 
      where CLASS="Data Science"; 
      also the sql code should not have ``` in beginning or end and sql word in output
"""
]

##streamlit app
st.set_page_config(page_title="I can retreive any SQL query")
st.markdown(
 """
    <style>
     
    .title {
        color: black; /* Custom color for title */
        font-size: 36px; /* Font size for title */
        font-weight: bold; /* Make the title bold */
        text-align: center; /* Center align the title */
        margin-bottom: 20px; /* Space below the title */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Add a shadow for depth */
        border-bottom: 3px solid black; /* Add a bottom border for emphasis */
        padding-bottom: 10px; /* Padding below the title */
    }
     .custom-button {
        background-color: #CBC3E3; /* Blue background */
        color: white; /* White text */
        border: none; /* No border */
        padding: 10px 25px; /* Padding around text */
        text-align: center; /* Center text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block for spacing */
        font-size: 16px; /* Font size */
        margin: 4px 2px; /* Margin around button */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 8px; /* Rounded corners */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Light shadow */
        transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transitions */
    }
    .custom-button:hover {
        background-color: #CBC3E3; /* Darker blue on hover */
        transform: scale(1.05); /* Slightly enlarge button */
    }
    .custom-button:active {
        background-color: #CBC3E3; /* Even darker blue when clicked */
        transform: scale(0.95); /* Slightly shrink button */
    .header {
          color: black; /* Bright blue color for headers */
        font-size: 30px;
        font-weight: 600; /* Semi-bold font weight */
        text-align: center;
        margin-bottom: 15px;
        font-family: 'Arial', sans-serif; /* Modern sans-serif font */
    }
    .markdown {
       color: black; /* Vibrant green color for markdown text */
        font-size: 24px;
        font-weight: 500; /* Medium font weight */
        text-align: center;
        margin-bottom: 15px;
        font-family: 'Arial', sans-serif; /* Modern sans-serif font */
    }
    .query {
         color: black; /* Eye-catching red color for SQL queries */
        font-size: 18px;
        font-weight: 500; /* Medium font weight */
        text-align: center;
        margin-bottom: 15px;
        font-family: 'Arial', sans-serif; /* Modern sans-serif font */
    }
    .response {
        color: black; /* Custom color for query results */
        font-size: 16px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>Gemini app to Retreive SQL Data</div>", unsafe_allow_html=True)
question=st.text_input("Input ")
# Create a custom button
submit=st.markdown(
    "<button class='custom-button' onclick='document.querySelector(\"button\").click();'>Ask the question</button>",
    unsafe_allow_html=True
)
#submit=st.button("Ask the question")

#if submit is clicked
if submit:
    response=get_gemini_response(question, prompt)
    st.markdown(f"<div class='query'>Generated SQL query: {response}</div>",unsafe_allow_html=True)  # Show the generated query
    response=read_sql_query(response,"student.db")
    #why prompt 0 imagine you have 3 buttons 0-->first
    #1-->second 2-->

    #display the results
    if response:
        st.markdown("<div class='markdown'>The response is:</div>",unsafe_allow_html=True)
        for row in response:
            st.write(row)
    else:
        st.write("No data found or query error.")
