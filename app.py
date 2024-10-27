import streamlit as st

# Title of the app
st.title("Weight Calculator for Plates")

# User input for thickness
thickness = st.number_input("Enter thickness (mm)", min_value=0.0, step=0.1)

# Selection for material type
material_type = st.selectbox("Select material type", ("Mild Steel (MS)", "Stainless Steel (SS)"))

# Button to calculate weight (no real calculation here yet)
if st.button("Calculate"):
    weight = thickness * 10  # Dummy calculation for demonstration
    st.write(f"Estimated weight: {weight} kg")  # Replace this with your calculation logic
