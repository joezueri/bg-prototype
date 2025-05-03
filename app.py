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

    sql = "INSERT INTO projecttable (name) VALUES (?)"
    params = (name,)  # Note the comma to make it a tuple

    st.text(sql) 
    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    st.success("Project added!")

# Display users
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM projecttable")
rows = cursor.fetchall()


for row in rows:
    id_, name = row
    cols = st.columns([1, 4, 1])
    cols[0].write(id_)
    cols[1].write(name)
    if cols[2].button('❌dtest', key=f'del_{id_}'):
        cursor.execute("DELETE FROM projecttable WHERE id = ?", (id_,))
        conn.commit()
        st.success(f"Deleted project ID {id_}")
        st.experimental_rerun()
conn.close()
#st.write(rows)


