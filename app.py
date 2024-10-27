import torch
import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Define material densities in g/cm^3
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

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')  # Replace with custom model if trained

# Function to calculate weight from segmented area and thickness
def calculate_irregular_weight_with_segmentation(image, thickness, density, reference_width_real):
    results = model(image)  # Perform segmentation with YOLOv5
    results.render()  # Render segmentation mask on image
    segmented_image = results.imgs[0]  # Get the masked image

    # Extract the main object's contour from the segmentation
    gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        st.error("Object not found in the image.")
        return None

    main_contour = max(contours, key=cv2.contourArea)
    main_area_pixels = cv2.contourArea(main_contour)

    # Ask the user for the reference object width in real units
    st.write("Provide a reference object in the image for accurate scaling.")
    reference_width_pixels = max(cv2.boundingRect(main_contour)[2], 1)  # Avoid division by zero

    # Calculate pixel-to-cm scale
    pixel_to_cm_ratio = reference_width_real / reference_width_pixels
    main_area_real = main_area_pixels * (pixel_to_cm_ratio ** 2)  # Area in cm²

    # Calculate volume and weight
    volume = main_area_real * thickness  # Volume in cm³
    weight = volume * density  # Weight in grams
    return weight / 1000  # Convert to kg

# Streamlit app for user interaction
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

        reference_width_real = st.number_input(f"Enter the real width of reference object (in {unit})", min_value=0.0, format="%.2f")
        reference_width_real_cm = reference_width_real * conversion_factor  # convert to cm

        if uploaded_image is not None and reference_width_real_cm > 0:
            image = np.array(Image.open(uploaded_image))
            st.image(image, caption="Uploaded Image", use_column_width=True)

            if st.button("Calculate Weight"):
                weight = calculate_irregular_weight_with_segmentation(image, thickness, density, reference_width_real_cm)
                if weight is not None:
                    st.write(f"The estimated weight of the irregular sheet is {weight:.2f} kg.")

if __name__ == "__main__":
    main()
