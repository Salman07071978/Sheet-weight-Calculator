import streamlit as st
from PIL import Image
import numpy as np

# Title of the App
st.title('MS/SS Plate Size Estimator')

# Step 1: User input for thickness and material type
thickness = st.number_input("Enter the thickness of the plate (in mm):", min_value=0.1, step=0.1)
material_type = st.selectbox("Select the material type:", options=["Mild Steel (MS)", "Stainless Steel (SS)"])

# Step 2: Choose shape or upload image for irregular shape
shape = st.radio(
    "Choose the shape of the plate:",
    options=["Square", "Rectangle", "Circle", "Irregular (upload image)"]
)

# Initialize area variable
area = None

if shape == "Square":
    side = st.number_input("Enter the side length (in mm):", min_value=0.0)
    area = side ** 2
    st.write(f"Area of the square plate: {area} mm²")

elif shape == "Rectangle":
    length = st.number_input("Enter the length (in mm):", min_value=0.0)
    width = st.number_input("Enter the width (in mm):", min_value=
