import streamlit as st

# Constants for densities (in kg/m³)
densities = {
    "Mild Steel (MS)": 7850,  # Density of MS
    "Stainless Steel (SS)": 8000  # Density of SS
}

# Title of the app
st.title("Weight Calculator for Plates")

# User input for dimensions
length = st.number_input("Enter length (mm)", min_value=0.0, step=0.1)
width = st.number_input("Enter width (mm)", min_value=0.0, step=0.1)
thickness = st.number_input("Enter thickness (mm)", min_value=0.0, step=0.1)

# Selection for material type
material_type = st.selectbox("Select material type", ("Mild Steel (MS)", "Stainless Steel (SS)"))

# Button to calculate weight
if st.button("Calculate"):
    # Convert dimensions from mm to m
    length_m = length / 1000
    width_m = width / 1000
    thickness_m = thickness / 1000
    
    # Calculate volume in m³
    volume = length_m * width_m * thickness_m
    
    # Calculate weight
    weight = volume * densities[material_type]
    
    st.write(f"Estimated weight: {weight:.2f} kg")
