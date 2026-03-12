import streamlit as st
from preprocess import prepare_image
from receipt_parser import parse_receipt

st.title("ReceiptReader")

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Receipt")
    processed_image = prepare_image(uploaded_file)

    if(st.button("Parse Receipt")):
        st.image(processed_image, caption="Processed Receipt")
        response = parse_receipt(processed_image)
        st.write(response)