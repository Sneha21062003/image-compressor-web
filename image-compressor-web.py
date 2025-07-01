# image_com_web.py
import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Image Compressor", page_icon="🖼️")

st.title("🖼️ Image Compressor Web App")
st.write("Compress one or more images directly in your browser!")

quality_level = st.selectbox("Choose Quality Level", ["High", "Medium", "Low"])

def get_width(quality):
    if quality == "High":
        return 2000
    elif quality == "Medium":
        return 1000
    elif quality == "Low":
        return 500

target_width = get_width(quality_level)

uploaded_files = st.file_uploader("Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) == 1:
        uploaded_file = uploaded_files[0]
        img = Image.open(uploaded_file)

        wpercent = (target_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((target_width, hsize), Image.LANCZOS)

        buffer = io.BytesIO()
        img_format = img.format if img.format else "JPEG"
        img.save(buffer, format=img_format)
        st.image(img, caption="Compressed Image", use_column_width=True)

        st.download_button(
            label="Download Compressed Image",
            data=buffer.getvalue(),
            file_name=f"compressed_{uploaded_file.name}",
            mime=f"image/{img_format.lower()}"
        )

    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for file in uploaded_files:
                img = Image.open(file)
                wpercent = (target_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((target_width, hsize), Image.LANCZOS)

                img_bytes = io.BytesIO()
                img_format = img.format if img.format else "JPEG"
                img.save(img_bytes, format=img_format)

                zipf.writestr(f"compressed_{file.name}", img_bytes.getvalue())

        st.success(f"{len(uploaded_files)} images compressed.")
        st.download_button(
            label="Download All as ZIP",
            data=zip_buffer.getvalue(),
            file_name="compressed_images.zip",
            mime="application/zip"
        )
