import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets config
SHEET_NAME = "GoiY"
SHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"
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
        return pd.DataFrame(data) if data else pd.DataFrame(columns=["Tên người", "Gợi ý", "Link"])
    return pd.DataFrame(columns=["Tên người", "Gợi ý", "Link"])

def save_data(df):
    """Lưu dữ liệu vào Google Sheets"""
    if sheet:
        sheet.clear()
        sheet.append_row(["Họ và tên", "Gợi ý", "Link", "Chi phí"])
        if not df.empty:
            sheet.update("A2", df.values.tolist())  

# Khởi tạo session state nếu chưa có
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("📌 Gợi ý thêm")

# Hiển thị bảng nhập dữ liệu trực tiếp
st.subheader("✏️ Nhập dữ liệu trực tiếp vào bảng")
edited_data = st.data_editor(st.session_state.data, num_rows="dynamic", use_container_width=True)

# Khi người dùng nhấn "Lưu dữ liệu"
if st.button("💾 Lưu dữ liệu"):
    st.session_state.data = edited_data
    save_data(st.session_state.data)
    st.success("✅ Dữ liệu đã được lưu!")
    st.rerun()
