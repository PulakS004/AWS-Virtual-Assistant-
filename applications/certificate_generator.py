import streamlit as st
import pandas as pd
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image

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
    color = (255, 255, 255)  # White color
    thickness = 4

    # Handling the case of a missing last name
    if pd.isna(lastname) or lastname.strip() == "":
        text = f"{name}"  # Use only the first name
    else:
        text = f"{name} {lastname}"
    position = (680, 700)  # Adjust position based on your template
    cv2.putText(template, text, position, font, font_scale, color, thickness)
    
    # Convert OpenCV image (BGR) to RGB for PIL compatibility
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
            # Create a new PDF for all certificates
            pdf_bytes = BytesIO()
            pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=(842.52, 595.27))  # Landscape A4 size
            
            # Counter for the position on the PDF (to avoid overlapping)
            y_position = 595.27  # Start at the bottom of the page

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

                # Full-page certificate in landscape
                page_width = 842.52  # Landscape width in points
                page_height = 595.27  # Landscape height in points

                # Ensure the certificate fits within the page by adjusting the position
                if y_position - page_height < 0:  # Start a new page if we run out of space
                    pdf_canvas.showPage()
                    y_position = page_height

                pdf_canvas.drawImage(img_reader, 0, y_position - page_height, width=page_width, height=page_height)
                y_position -= page_height  # Move down for the next certificate

            # Finalize the PDF
            pdf_canvas.save()

            # Allow download of the combined PDF
            st.success("Certificates generated successfully!")
            st.download_button(
                "Download All Certificates as PDF",
                pdf_bytes.getvalue(),
                file_name="all_certificates.pdf"
            )
