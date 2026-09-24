import streamlit as st

st.title("Medical Emergency Assistance")

st.write("Hello! You are in safe hands now.")
st.write("Do you have a medical emergency?")

name = st.text_input("What is you first and last name?")

if name:
    st.success(f"Welcome, {name}!")

sickness = st.selectbox("What is your medical condition?", ["Heart Attack", "Stroke", "Severe Bleeding", "Other"])
if sickness:
    st.write(f"You selected: {sickness}")

number = st.slider("How much pain are you currently feeling?", 0, 10, 5)

st.write("Your selected pain level:", number)
