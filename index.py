import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MySQL@123",
  database="py_medicine_tracker"
)

mycur=mydb.cursor()

st.set_page_config(
     page_title="Ex-stream-ly Cool DBMS App",
     page_icon="favicon.png",
     layout="wide",
     initial_sidebar_state="collapsed",
     menu_items=None
)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'is_user' not in st.session_state:
    st.session_state.is_user = False

if 'user' not in st.session_state:
    st.session_state.user = None

def page(str):
    st.session_state.page = str

def logout():
    st.session_state.is_admin = False
    st.session_state.is_user = False

st.title("Py Medicine Tracker")
st.sidebar.title("Pages")
st.sidebar.markdown("---")

if not st.session_state.is_user:
    page("login")
else:
    st.sidebar.button("Logout",on_click=logout)
    st.sidebar.markdown("---")


if st.session_state.is_user:
    st.sidebar.button("Home",on_click=page,args=["home"])
    st.sidebar.button("Patient",on_click=page,args=["patient"])
    st.sidebar.button("Register",on_click=page,args=["reg"])

if st.session_state.is_admin:    
    st.sidebar.button("Medicine",on_click=page,args=["medicine"])
    st.sidebar.button("Pharmacist",on_click=page,args=["pharmacist"])

    st.markdown("---")






        
if st.session_state.page=="login" and not st.session_state.is_admin and not st.session_state.is_user:
    st.write("Add Username And Password to Login")
    u_name=st.text_input("Username")
    pswd=st.text_input("Password",type="password")
    if st.button("Login",key="login"):
        mycur.execute("SELECT * FROM pharmacist WHERE userName=%s AND pwd=%s", (u_name, pswd))
        myresult = mycur.fetchall()
        if (u_name=="admin" and pswd=="admin") or (myresult!=None):
            st.session_state.is_user=True
            st.session_state.user=myresult[0][0]
            if myresult[0][2]==1 or (u_name=="admin" and pswd=="admin"):
                st.session_state.is_admin = True
            page("home")
            st.write("Logged In Successfully")
            
        else:
            st.error("Incorrect Username Or Password")
        
else:
    if st.session_state.page=="home":
        st.write("Welcome to the Py Medicine Tracker")
        st.markdown("---")
        st.markdown("This is a simple application to track medicines")
        st.markdown("---")
        st.markdown("This application is still in development")
        st.markdown("---")
        st.markdown("If you have any questions, please contact me at:")
       
#medicine page
if st.session_state.page=="medicine" and st.session_state.is_admin==True:
    st.write("Add Medicine")
    m_name=st.text_input("Medicine Name")
    m_price=st.text_input("Medicine Price")
    m_quantity=st.text_input("Medicine Quantity")
    m_date=st.date_input("Medicine Date")
    formatted_date = m_date.strftime('%Y-%m-%d %H:%M:%S')
    if st.button("Add Medicine",key="add"):
        mycur.execute("INSERT INTO stock (drugName, quantity, price, date_expired) VALUES (%s, %s, %s, %s)", (m_name, m_quantity, m_price, m_date))
        st.success("Added Successfully")
        st.write("You can now view the medicines")
        st.markdown("---")
        st.markdown("Medicine Name:")
        st.markdown(m_name)
        st.markdown("Medicine Price:")
        st.markdown(m_price)
        st.markdown("Medicine Quantity:")
        st.markdown(m_quantity)
        st.markdown("Medicine Date:")
        st.markdown(m_date)
        st.markdown("---")
        mydb.commit()

        



#patient page
if st.session_state.page=="patient" and st.session_state.is_user==True:
    st.write("Add Patient")
    pf_name=st.text_input("Patient first Name")
    pl_name=st.text_input("Patient last Name")
    
    if st.button("Add Patient",key="add"):
        mycur.execute("INSERT INTO customer (firstName, lastName) VALUES (%s, %s)", (pf_name, pl_name))
        mydb.commit()
        st.success("Added Successfully")
        st.write("You can now view the patients")
        st.markdown("---")
        st.markdown("Patient Name:")
        st.markdown(f"{pf_name} {pl_name}")
        st.markdown("---")
    if st.button("Delete Patient",key="del"):
        mycur.execute("DELETE FROM customer WHERE firstName=%s and lastName=%s", (pf_name, pl_name))
        mydb.commit()
        st.markdown("---")
        st.markdown("Patient Name:")
        st.markdown(f"{pf_name} {pl_name}")
        

#pharmacist page
if st.session_state.page=="pharmacist" and st.session_state.is_admin==True:
    st.write("Add Pharmacist")
    p_name=st.text_input("Pharmacist Name")
    pwd=st.text_input("Pharmacist Password",type="password")
    
    if st.button("Add Pharmacist",key="add"):
        mycur.execute("INSERT INTO pharmacist (userName,pwd,isAdmin) VALUES (%s, %s,false)", (p_name, pwd))
        mydb.commit()
        st.success("Added Successfully")
        st.write("You can now view the pharmacist")
        st.markdown("---")
        st.markdown("Pharmacist Name:")
        st.markdown(p_name)
        st.markdown("---")
    if st.button("Delete Pharmacist",key="del"):
        mycur.execute("delete from pharmacist where userName='{}'" .format(p_name))
        mydb.commit()
        st.markdown("---")
        st.markdown("Pharmacist Name:")
        st.markdown(p_name)
        st.markdown("---")
        st.success("Deleted Successfully")


#register page
if st.session_state.page=="reg" and st.session_state.is_user==True:
    st.write("")
    mycur.execute("SELECT drugName FROM stock")
    myresult = mycur.fetchall()
    mlist=[i[0] for i in myresult[:]]
    med=st.selectbox("Medicine",mlist)
    st.write("")
    qut=st.number_input("Quantity",min_value=1,max_value=10)
    mycur.execute("SELECT firstName,lastName FROM customer")
    myresult = mycur.fetchall()
    plist=[f"{i[0]} {i[1]}" for i in myresult[:]]
    c_name=st.selectbox("Patient",plist)
    st.write("")
    
    if st.button("order",key="order"):
        mycur.execute("UPDATE stock SET quantity=quantity-%s WHERE drugName=%s", (qut,med))
        mydb.commit()
        st.success("Ordered Successfully")
    st.write("")
