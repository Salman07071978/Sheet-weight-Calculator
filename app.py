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

# Function to calculate area and weight of irregular shape with reference object
def calculate_irregular_weight_with_reference(image, thickness, density, reference_width_real):
    # Convert image to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the largest contour as our main object
    main_contour = max(contours, key=cv2.contourArea)
    main_area_pixels = cv2.contourArea(main_contour)

    # Assume reference object is the second largest contour (after main object)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    reference_contour = contours[1] if len(contours) > 1 else None

    if reference_contour is None:
        st.error("Reference object not found in the image. Please ensure a reference object is present.")
        return None

    # Get the width of the reference object in pixels
    ref_x, ref_y, ref_w, ref_h = cv2.boundingRect(reference_contour)
    reference_width_pixels = ref_w

    # Calculate pixel-to-real-world scale
    pixel_to_cm_ratio = reference_width_real / reference_width_pixels

    # Calculate real area of the main object
    main_area_real = main_area_pixels * (pixel_to_cm_ratio ** 2)  # in cm^2

    # Estimate weight
    volume = main_area_real * thickness  # in cm^3
    weight = volume * density  # weight in grams
    return weight / 1000  # convert to kg

# Streamlit app
def main():
    st.title("MS/SS Sheet Weight Calculator with Irregular Shape Detection")

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
        uploaded_image = st.file_uploader("Upload an image of the sheet with a reference object", type=["jpg", "png", "jpeg"])

        # Ask user for real-world reference width
        reference_width_real = st.number_input(f"Enter the real width of reference object (in {unit})", min_value=0.0, format="%.2f")
        reference_width_real_cm = reference_width_real * conversion_factor  # convert to cm

        if uploaded_image is not None and reference_width_real_cm > 0:
            image = np.array(Image.open(uploaded_image))
            st.image(image, caption="Uploaded Image", use_column_width=True)

            if st.button("Calculate Weight"):
                weight = calculate_irregular_weight_with_reference(image, thickness, density, reference_width_real_cm)
                if weight is not None:
                    st.write(f"The estimated weight of the irregular sheet is {weight:.2f} kg.")

if __name__ == "__main__":
    main()
