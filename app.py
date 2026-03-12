import streamlit as st
from preprocess import prepare_image
from receipt_parser import parse_receipt
import json

st.title("ReceiptReader")

files = st.file_uploader("Upload a receipt image", type=[
                         "jpg", "jpeg", "png"], accept_multiple_files=True)

if files:
    for uploaded_file in files:
        st.image(uploaded_file, caption="Uploaded Receipt")
    
    if st.button("Parse Receipts"):
        results = []
        total_sum = 0
        
        for uploaded_file in files:
            processed_image = prepare_image(uploaded_file)
            response = parse_receipt(processed_image)
            
            # JSON解析
            try:
                if isinstance(response, str):
                    receipt_data = json.loads(response)
                else:
                    receipt_data = response
                
                result = {
                    "filename": uploaded_file.name,
                    "receipt_data": receipt_data
                }
                results.append(result)
                
                # 合計金額を加算
                if "total_amount" in receipt_data and receipt_data["total_amount"]:
                    total_sum += receipt_data["total_amount"]
                
                st.write(f"**{uploaded_file.name}**")
                st.json(receipt_data)
            except:
                st.error(f"Failed to parse {uploaded_file.name}")
        
        # まとめたJSON作成
        summary = {
            "receipts": results,
            "total_sum": total_sum
        }
        
        # ダウンロードボタン
        json_str = json.dumps(summary, ensure_ascii=False, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="receipts_summary.json",
            mime="application/json"
        )
