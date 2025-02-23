import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets config
SHEET_NAME = "GoiY"
SHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"  # Cập nhật Google Sheet ID
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials từ Streamlit secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

# Mở Google Sheet
try:
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
except Exception as e:
    st.error(f"Không thể kết nối Google Sheets: {e}")
    sheet = None

def load_data():
    """Load dữ liệu từ Google Sheets"""
    if sheet:
        data = sheet.get_all_records()
        return data if data else []
    return []

def save_data(data):
    """Lưu dữ liệu vào Google Sheets"""
    if sheet:
        sheet.clear()
        sheet.append_row(["Tên người", "Gợi ý", "Link"])
        if data:
            sheet.update("A2", [list(row.values()) for row in data])  # Cập nhật nhanh hơn

# Khởi tạo session state nếu chưa có
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("Gợi ý thêm")

# Nhập thông tin mới
with st.form("suggest_form", clear_on_submit=True):
    ten_nguoi = st.text_input("Tên người *", placeholder="Nhập tên người")
    suggest = st.text_area("Gợi ý", placeholder="Nhập gợi ý (có thể để trống)")
    link = st.text_input("Link", placeholder="Nhập link (có thể để trống)")

    submitted = st.form_submit_button("Thêm vào bảng")

    if submitted and ten_nguoi:
        new_entry = {"Tên người": ten_nguoi, "Gợi ý": suggest, "Link": link}
        st.session_state.data.append(new_entry)
        save_data(st.session_state.data)
        st.success("Gợi ý đã được lưu!")
        st.rerun()

# Hiển thị bảng với nút Xoá trên từng dòng
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    for i, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        col1.write(row["Tên người"])
        col2.write(row["Gợi ý"])
        col3.write(row["Link"])
        if col4.button("🗑️ Xoá", key=f"delete_{i}"):
            st.session_state.data.pop(i)
            save_data(st.session_state.data)
            st.success("Gợi ý đã được xoá!")
            st.rerun()
else:
    st.write("🔹 Hãy thêm gợi ý của ní!")
