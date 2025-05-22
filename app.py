import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io

def convert_pdf_to_dark_mode(input_file):
    # Loads the PDF from the uploaded file
    doc = fitz.open(stream=input_file.read(), filetype="pdf")

    output_buffer = io.BytesIO()  # Buffer to store the modified PDF

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)

        # Renders the page as image (2x DPI for better quality)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

        # Converts it to a PIL image and invert colors for dark mode
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        inverted_img = ImageOps.invert(img)

        # Saves the inverted image to memory as a JPEG (compressed)
        img_buffer = io.BytesIO()
        inverted_img.save(img_buffer, format="JPEG", quality=90)
        img_buffer.seek(0)

        # Clears the original content and inserts the inverted image
        page_rect = page.rect
        page.clean_contents()
        page.insert_image(page_rect, stream=img_buffer.read())

    # Saves the modified PDF to the output buffer
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)
    return output_buffer

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🌓 PDF Dark Mode Converter")
st.write("Upload a PDF and get a dark mode version instantly.")

uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Converting to dark mode..."):
        dark_pdf = convert_pdf_to_dark_mode(uploaded_file)

    st.success("✅ Conversion complete! Download your dark mode PDF below.")
    st.download_button(
        label="📥 Download Dark Mode PDF",
        data=dark_pdf,
        file_name="dark_mode_output.pdf",
        mime="application/pdf"
    )
