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

if shape == "Square":
    side = st.number_input("Enter the side length (in mm):", min_value=0.0)
    area = side ** 2
    st.write(f"Area of the square plate: {area} mm²")

elif shape == "Rectangle":
    length = st.number_input("Enter the length (in mm):", min_value=0.0)
    width = st.number_input("Enter the width (in mm):", min_value=0.0)
    area = length * width
    st.write(f"Area of the rectangular plate: {area} mm²")

elif shape == "Circle":
    radius = st.number_input("Enter the radius (in mm):", min_value=0.0)
    area = np.pi * radius ** 2
    st.write(f"Area of the circular plate: {area:.2f} mm²")

elif shape == "Irregular (upload image)":
    uploaded_file = st.file_uploader("Upload an image of the plate:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        st.write("For irregular shapes, you can calculate the area manually or use external tools.")

# Optional: Calculating approximate weight based on material and area
if st.button("Calculate Weight"):
    density = 0  # density of the material (g/mm³)
    if material_type == "Mild Steel (MS)":
        density = 0.00785  # g/mm³
    elif material_type == "Stainless Steel (SS)":
        density = 0.0080  # g/mm³

    weight = area * thickness * density
    st.write(f"Approximate weight of the plate: {weight:.2f} grams")

