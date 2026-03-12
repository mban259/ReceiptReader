import streamlit as st
from preprocess import prepare_image
from receipt_parser import parse_receipt

st.title("ReceiptReader")

files = st.file_uploader("Upload a receipt image", type=[
                         "jpg", "jpeg", "png"], accept_multiple_files=True)

if files:
    for uploaded_file in files:
        st.image(uploaded_file, caption="Uploaded Receipt")

    if st.button("Parse Receipts"):
        for uploaded_file in files:
            processed_image = prepare_image(uploaded_file)
            response = parse_receipt(processed_image)
            st.write(response)

