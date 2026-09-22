import streamlit as st

st.title("My First Streamlit App")

st.write("Hello! This webpage was created with Python.")

name = st.text_input("What is your name?")

if name:
    st.success(f"Welcome, {name}!")

number = st.slider("Choose a number", 0, 100, 50)

st.write("You selected:", number)
