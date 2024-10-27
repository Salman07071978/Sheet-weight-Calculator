# Import necessary libraries
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Material densities in g/cm^3
MATERIAL_DENSITIES = {
    'MS': 7.85,  # Mild Steel
    'SS': 8.00   # Stainless Steel
}

# Conversion factors to centimeters
UNIT_CONVERSIONS = {
    'cm': 1,
    'mm': 0.1,
    'inch': 2.54
}

# Function to calculate weight for regular shapes
def calculate_weight(thickness, length, width, density):
    volume = thickness * length * width  # in cm^3
    weight = volume * density  # weight in grams
    return weight / 1000  # convert to kg

# Function to calculate area of irregular shape using calibration
def calculate_irregular_weight(image, thickness, density, calibration_length, calibration_pixels):
    # Convert image to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)
    area_pixels = cv2.contourArea(largest_contour)

    # Calculate real area using calibration
    scale_factor = (calibration_length / calibration_pixels) ** 2  # (cm/pixel)^2
    area_cm2 = area_pixels * scale_factor  # Convert pixel area to cm²

    # Estimate weight
    volume = area_cm2 * thickness  # in cm^3
    weight = volume * density  # weight in grams
    return weight / 1000  # convert to kg

# Streamlit app
def main():
    st.title("MS/SS Sheet Weight Calculator")

    # Material selection
    material_type = st.selectbox("Select Material Type", ("MS", "SS"))
    density = MATERIAL_DENSITIES[material_type]

    # Unit selection
    unit = st.selectbox("Select Unit of Measurement", ("cm", "mm", "inch"))
    conversion_factor = UNIT_CONVERSIONS[unit]

    # Shape selection
    shape = st.selectbox("Select Shape", ("Rectangular", "Square", "Irregular"))

    if shape in ["Rectangular", "Square"]:
        thickness = st.number_input("Enter Thickness", min_value=0.0, format="%.2f") * conversion_factor
        length = st.number_input("Enter Length", min_value=0.0, format="%.2f") * conversion_factor
        width = st.number_input("Enter Width", min_value=0.0, format="%.2f") * conversion_factor

        if st.button("Calculate Weight"):
            weight = calculate_weight(thickness, length, width, density)
            st.write(f"The weight of the {shape.lower()} sheet is {weight:.2f} kg.")

    elif shape == "Irregular":
        thickness = st.number_input("Enter Thickness", min_value=0.0, format="%.2f") * conversion_factor
        calibration_length = st.number_input("Enter the known length of a reference object in the image (in selected unit)", min_value=0.0, format="%.2f") * conversion_factor
        uploaded_image = st.file_uploader("Upload an image of the sheet", type=["jpg", "png", "jpeg
