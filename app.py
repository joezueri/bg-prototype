import streamlit as st
from database import get_connection
from init import create_table

create_table()  # run once to ensure table exists

st.title("Hello Streamlit Cloud!")
st.write("This is my first deployed app 🚀")



name = st.text_input("Name")

if st.button("Add project"):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO projecttable (name) VALUES (?)", (name)
    st.text(sql) 
    cursor.execute(sql)
    conn.commit()
    conn.close()
    st.success("Project added!")

# Display users
if st.button("Show all projects"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projecttable")
    rows = cursor.fetchall()
    conn.close()
    
    st.write(rows)


