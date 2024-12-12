import streamlit as st
import pandas as pd
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image

def render():
    st.header("Certificate Generator")
    st.write("This feature helps you generate certificates for event participants.")

# Function to generate certificate
def generate_certificate(name, lastname, template_path):
    # Load the certificate template
    template = cv2.imread(template_path)
    
    # Check if the image was loaded successfully
    if template is None:
        st.error("Error: Certificate template image not found. Please check the template path.")
        return None
    
    # Define the text properties
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 2.5
    color = (255,255,255)  # White color
    thickness = 4

    # Overlay text onto the template
    #Handling case of missing last name
    if pd.isna(lastname) or lastname.strip() == "":
        text = f"{name}" #Use only the first name
    else:
        text = f"{name} {lastname}"
    position = (680, 700)  # Adjust position based on your template
    cv2.putText(template, text, position, font, font_scale, color, thickness)
    
    # Convert OpenCV image (BGR) to RGB for PIL(Python Imaging Library) compatibility
    template_rgb = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
    
    # Convert the image to a PIL Image object
    pil_image = Image.fromarray(template_rgb)
    
    # Save the PIL image to a BytesIO object
    image_stream = BytesIO()
    pil_image.save(image_stream, format="PNG")
    image_stream.seek(0)  # Reset the pointer to the beginning of the stream
    
    return image_stream

# Streamlit interface
st.title("Certificate Generator")

# Upload participant CSV file
uploaded_file = st.file_uploader("Upload CSV file with participant details", type="csv")
template_path = "certificate_template.png"  # Make sure this path is correct

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.write(data)

    # Remove any extra spaces in column names
    data.columns = data.columns.str.strip()

    # Check if necessary columns are in the CSV file
    if 'Name' not in data.columns or 'Lastname' not in data.columns:
        st.error("CSV file must contain 'Name' and 'Lastname' columns.")
    else:
        if st.button("Generate Certificates"):
            pdf_bytes = BytesIO()

            # Create a PDF canvas
            pdf_canvas = canvas.Canvas(pdf_bytes)

            for index, row in data.iterrows():
                name = row["Name"]
                lastname = row["Lastname"]
                
                # Debugging log for certificate generation
                st.write(f"Generating certificate for {name} {lastname}")
                
                # Generate certificate image
                certificate_image_stream = generate_certificate(name, lastname, template_path)
                
                if certificate_image_stream is None:
                    continue
                
                st.write(f"Certificate image generated for {name} {lastname}")
                
                # Use ImageReader to process the image stream
                img_reader = ImageReader(certificate_image_stream)
                
                # Embed in the PDF
                pdf_canvas.drawImage(img_reader, 50, 400, width=500, height=300)
                pdf_canvas.showPage()

            pdf_canvas.save()
            
            st.success("Certificates generated successfully!")
            st.download_button(
                "Download Certificates as PDF",
                pdf_bytes.getvalue(),
                file_name="certificates.pdf"
            )
