import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Kết nối với Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(credentials)
SPREADSHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"

# Hàm tải dữ liệu từ Google Sheets
def load_data(sheet_name):
    try:
        worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
        return pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()

# Hàm lưu dữ liệu lên Google Sheets
def save_data(sheet_name, df):
    try:
        worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("Đã lưu thành công!")
    except Exception as e:
        st.error(f"Lỗi khi lưu dữ liệu: {e}")

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Anton&display=swap" rel="stylesheet">
    <style>
        body { background-color: #0E1117; color: white; font-family: 'Anton', sans-serif; }
        h1 { color: #A0D683 !important; font-size: 50px !important; font-weight: 700 !important; font-family: 'Anton', sans-serif; }
        h2 { color: #B3C8CF !important; font-size: 40px !important; font-weight: 700 !important; font-family: 'Anton', sans-serif; }
        .custom-metric-label { color: #FFE3E3 !important; font-weight: 700 !important; font-size: 25px !important; font-family: 'Anton', sans-serif; }
        .custom-metric-value { color: #FFFFFF !important; font-size: 30px !important; font-family: 'Anton', sans-serif; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("PROJECT: ĐÀ LẠT PLANNING")

# DANH SÁCH THAM GIA
st.header("DANH SÁCH THAM GIA")
people_df = load_data("NguoiThamGia")
if people_df.empty:
    people_df = pd.DataFrame({"Họ và Tên": [], "Budget": []})
people_df["Budget"] = pd.to_numeric(people_df["Budget"].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
people_df = st.data_editor(people_df, num_rows="dynamic", key="people")

total_people = people_df["Họ và Tên"].nunique()
total_cost_people = people_df["Budget"].sum()
if st.button("Lưu", key="save_people"):
    save_data("NguoiThamGia", people_df)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='custom-metric-label'>👥 TỔNG SỐ NGƯỜI THAM GIA</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-metric-value'>{total_people}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='custom-metric-label'>💰 TỔNG CHI PHÍ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-metric-value'>{total_cost_people:,}</div>", unsafe_allow_html=True)

# CHI PHÍ CỐ ĐỊNH
st.header("CHI PHÍ CỐ ĐỊNH")
chi_phi_df = load_data("ChiPhi_LichTrinh")
if "Chi phí" in chi_phi_df.columns:
    chi_phi_df["Chi phí"] = (
        pd.to_numeric(chi_phi_df["Chi phí"].astype(str).str.replace(",", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )
else:
    chi_phi_df["Chi phí"] = 0  
chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")
if st.button("Lưu", key="save_cost"):
    save_data("ChiPhi_LichTrinh", chi_phi_df)

st.markdown(f"<div class='custom-metric-label'>💰 TỔNG CHI PHÍ CỐ ĐỊNH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='custom-metric-value'>{chi_phi_df['Chi phí'].sum():,}</div>", unsafe_allow_html=True)

# LỊCH TRÌNH VÀ CHI PHÍ
st.header("LỊCH TRÌNH VÀ CHI PHÍ")
plan_df = load_data("LichTrinh")
chi_phi_df = load_data("ChiPhi_LichTrinh")

if "Chi phí" in chi_phi_df.columns:
    chi_phi_df["Chi phí"] = (
        pd.to_numeric(chi_phi_df["Chi phí"].astype(str).str.replace(",", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )
else:
    chi_phi_df["Chi phí"] = 0  

if not plan_df.empty:
    unique_dates = plan_df["Ngày"].unique()
    selected_date = st.selectbox("Chọn ngày để xem lịch trình:", unique_dates)
    
    # Lọc dữ liệu theo ngày được chọn
    filtered_plan_df = plan_df[plan_df["Ngày"] == selected_date]
    
    plan_df = st.data_editor(filtered_plan_df, num_rows="dynamic", key="plan", use_container_width=True)
else:
    st.warning("Không có dữ liệu lịch trình để hiển thị.")

if st.button("Lưu", key="save_plan"):
    save_data("LichTrinh", plan_df)
    
total_plan_cost = plan_df["Chi phí"].sum()
st.markdown(f"<div class='custom-metric-label'>💰 TỔNG CHI PHÍ LỊCH TRÌNH</div>", unsafe_allow_html=True)
st.markdown(f"<div class='custom-metric-value'>{int(total_plan_cost):,}</div>", unsafe_allow_html=True)

# SỐ DƯ HIỆN TẠI
budget_remaining = total_cost_people - (chi_phi_df["Chi phí"].sum() + plan_df["Chi phí"].sum())
st.markdown(f"<div class='custom-metric-label'>💰 SỐ DƯ HIỆN TẠI</div>", unsafe_allow_html=True)
st.markdown(f"<div class='custom-metric-value'>{int(budget_remaining):,}</div>", unsafe_allow_html=True)
