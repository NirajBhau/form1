import streamlit as st
import pyodbc

# MSSQL connection
def init_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-CEIB8QQ\NIRAJ;"  # Replace with your MSSQL server name
        "DATABASE=form;"  # Replace with your MSSQL database name
        "UID=DESKTOP-CEIB8QQ\NIRAJ;"  # Replace with your MSSQL username
        "PWD=001122;"  # Replace with your MSSQL password
    )
    return pyodbc.connect(conn_str)

conn = init_connection()
c = conn.cursor()

# Function to add a person to the database
def add_person(name, age, email, address):
    query = 'INSERT INTO Person (Name, Age, Email, Address) VALUES (?, ?, ?, ?)'
    c.execute(query, (name, age, email, address))
    conn.commit()

# Function to view all persons
def view_all_persons():
    c.execute('SELECT * FROM Person')
    return c.fetchall()

# Function to delete a person
def delete_person(person_id):
    c.execute('DELETE FROM Person WHERE ID = ?', (person_id,))
    conn.commit()

# Function to update a person's details
def update_person(person_id, name, age, email, address):
    query = '''
        UPDATE Person
        SET Name = ?, Age = ?, Email = ?, Address = ?
        WHERE ID = ?
    '''
    c.execute(query, (name, age, email, address, person_id))
    conn.commit()

# Streamlit App
st.title("Person Details Management App")

menu = ["Add Person", "View Persons", "Update Person", "Delete Person"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Person":
    st.subheader("Add a New Person")
    
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    email = st.text_input("Email")
    address = st.text_area("Address")
    
    if st.button("Add"):
        add_person(name, age, email, address)
        st.success(f"Person '{name}' added successfully!")

elif choice == "View Persons":
    st.subheader("View All Persons")
    persons = view_all_persons()
    
    if persons:
        for person in persons:
            st.write(f"ID: {person[0]} | Name: {person[1]} | Age: {person[2]} | Email: {person[3]} | Address: {person[4]}")
    else:
        st.info("No persons found.")

elif choice == "Update Person":
    st.subheader("Update Person Details")
    
    person_id = st.number_input("Enter Person ID", min_value=1)
    
    if st.button("Load Person Details"):
        c.execute('SELECT * FROM Person WHERE ID = ?', (person_id,))
        person = c.fetchone()
        
        if person:
            name = st.text_input("Name", value=person[1])
            age = st.number_input("Age", min_value=0, max_value=120, value=person[2])
            email = st.text_input("Email", value=person[3])
            address = st.text_area("Address", value=person[4])
            
            if st.button("Update"):
                update_person(person_id, name, age, email, address)
                st.success(f"Person ID '{person_id}' updated successfully!")
        else:
            st.warning(f"Person ID '{person_id}' not found.")

elif choice == "Delete Person":
    st.subheader("Delete a Person")
    
    person_id = st.number_input("Enter Person ID", min_value=1)
    
    if st.button("Delete"):
        delete_person(person_id)
        st.success(f"Person ID '{person_id}' deleted successfully!")

# Close the connection to the database
conn.close()
