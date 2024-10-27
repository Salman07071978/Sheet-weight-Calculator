import streamlit as st
import numpy as np
import cv2
import torch
from PIL import Image

# Function to calculate the weight of the plate
def calculate_weight(thickness, area, material_density):
    return thickness * area * material_density

# Function to get the area of a detected shape
def get_area_from_image(image):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', source='local')
    
    results = model(image)
    results.show()  # This will display the detected objects if run locally
    
    # Process results to find the area
    area = 0
    for *box, conf, cls in results.xyxy[0]:  # Get results
        x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers
        area += (x2 - x1) * (y2 - y1)  # Calculate area of bounding box

    return area

# Streamlit app layout
st.title("Weight Calculator for MS/SS Plates")

# User input for thickness and dimensions
thickness = st.number_input("Enter the thickness (mm)", min_value=0.0, step=0.1)
material_type = st.selectbox("Select material type", ("Mild Steel (MS)", "Stainless Steel (SS)"))
density = 7.85 if material_type == "Mild Steel (MS)" else 8.00  # g/cm^3

shape_type = st.selectbox("Select shape type", ("Rectangular", "Square", "Irregular"))

if shape_type in ["Rectangular", "Square"]:
    length = st.number_input("Enter length (mm)", min_value=0.0, step=0.1)
    width = st.number_input("Enter width (mm)", min_value=0.0, step=0.1)

    area = length * width if shape_type == "Rectangular" else length ** 2
    weight = calculate_weight(thickness / 1000, area / 1000000, density)  # Convert units to m^3
    st.write(f"The weight of the {shape_type} plate is: {weight:.2f} kg")

elif shape_type == "Irregular":
    uploaded_file = st.file_uploader("Upload an image of the irregular shape", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Convert image to numpy array for YOLOv5
        image_np = np.array(image)
        
        # Get the area from the image using YOLOv5
        area = get_area_from_image(image_np)
        weight = calculate_weight(thickness / 1000, area / 1000000, density)  # Convert units to m^3
        st.write(f"The estimated weight of the irregular plate is: {weight:.2f} kg")
