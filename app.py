# Import libraries
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from pyngrok import ngrok

# Constants for material densities (in g/cm^3)
DENSITIES = {
    "MS": 7.85,  # Mild Steel
    "SS": 8.00   # Stainless Steel
}

def calculate_weight(density, thickness, area):
    # Density in g/cm^3, thickness and area should be in cm^2
    return density * thickness * area

def get_area_from_dimensions(shape, length, width=None):
    if shape == "Rectangle":
        return length * width
    elif shape == "Square":
        return length * length
    else:
        return None

def process_irregular_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Assume largest contour is the object
        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)
        return area  # in pixel units
    return None

def main():
    st.title("Metal Sheet Weight Calculator")

    # User selects material type
    material_type = st.selectbox("Select Material Type", ("MS", "SS"))
    density = DENSITIES[material_type]

    # User inputs thickness
    thickness = st.number_input("Enter Thickness (cm)", min_value=0.01)

    # User selects shape
    shape = st.selectbox("Select Shape", ("Rectangle", "Square", "Irregular"))

    if shape == "Irregular":
        uploaded_file = st.file_uploader("Upload Image of Sheet", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            image = np.array(image.convert('RGB'))
            area = process_irregular_image(image)
            if area is not None:
                # Here we assume a scale (e.g., each pixel represents 0.01 cm^2, which can be calibrated)
                scale_factor = 0.01  # Adjust based on image calibration
                area_cm2 = area * scale_factor
                weight = calculate_weight(density, thickness, area_cm2)
                st.write(f"Calculated Weight: {weight:.2f} grams")
            else:
                st.write("Could not detect shape in image.")
    else:
        # Regular shapes
        length = st.number_input("Enter Length (cm)", min_value=0.01)
        if shape == "Rectangle":
            width = st.number_input("Enter Width (cm)", min_value=0.01)
        else:
            width = length

        # Calculate area and weight
        area = get_area_from_dimensions(shape, length, width)
        weight = calculate_weight(density, thickness, area)
        st.write(f"Calculated Weight: {weight:.2f} grams")
