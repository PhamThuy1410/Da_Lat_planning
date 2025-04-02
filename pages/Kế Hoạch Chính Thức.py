import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Kết nối với Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(credentials)
SPREADSHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"

@st.cache_data
def get_worksheet(sheet_name):
    """Cache worksheet to optimize performance."""
    try:
        return gc.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    except Exception as e:
        st.error(f"Không thể kết nối Google Sheets: {e}")
        return None

# Hàm tải dữ liệu từ Google Sheets
def load_data(sheet_name):
    worksheet = get_worksheet(sheet_name)
    if worksheet:
        try:
            return pd.DataFrame(worksheet.get_all_records())
        except Exception as e:
            st.error(f"Lỗi khi tải dữ liệu từ {sheet_name}: {e}")
    return pd.DataFrame()

# Hàm lưu dữ liệu lên Google Sheets
def save_data(sheet_name, df):
    worksheet = get_worksheet(sheet_name)
    if worksheet is not None:
        try:
            worksheet.clear()
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            st.success("Đã lưu thành công!")
        except Exception as e:
            st.error(f"Lỗi khi lưu dữ liệu vào {sheet_name}: {e}")

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
    st.markdown(f"**👥 TỔNG SỐ NGƯỜI THAM GIA:** {total_people}")
with col2:
    st.markdown(f"**💰 TỔNG CHI PHÍ:** {total_cost_people:,}")

# CHI PHÍ CỐ ĐỊNH
st.header("CHI PHÍ CỐ ĐỊNH")
chi_phi_df = load_data("ChiPhi_LichTrinh")
if "Chi phí" in chi_phi_df.columns:
    chi_phi_df["Chi phí"] = pd.to_numeric(chi_phi_df["Chi phí"].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
else:
    chi_phi_df["Chi phí"] = 0  
chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")
if st.button("Lưu", key="save_cost"):
    save_data("ChiPhi_LichTrinh", chi_phi_df)

total_fixed_cost = chi_phi_df["Chi phí"].sum()
st.markdown(f"**💰 TỔNG CHI PHÍ CỐ ĐỊNH:** {total_fixed_cost:,}")

# LỊCH TRÌNH VÀ CHI PHÍ
st.header("LỊCH TRÌNH VÀ CHI PHÍ")
plan_df = load_data("LichTrinh")
if not plan_df.empty:
    unique_dates = plan_df["Ngày"].unique()
    selected_date = st.selectbox("Chọn ngày để xem lịch trình:", unique_dates)
    filtered_plan_df = plan_df[plan_df["Ngày"] == selected_date]
    plan_df = st.data_editor(filtered_plan_df, num_rows="dynamic", key="plan", use_container_width=True)
else:
    st.warning("Không có dữ liệu lịch trình để hiển thị.")

if st.button("Lưu", key="save_plan"):
    save_data("LichTrinh", plan_df)

total_plan_cost = plan_df["Chi phí"].sum()
st.markdown(f"**💰 TỔNG CHI PHÍ LỊCH TRÌNH:** {int(total_plan_cost):,}")

# SỐ DƯ HIỆN TẠI
budget_remaining = total_cost_people - (total_fixed_cost + total_plan_cost)
st.markdown(f"**💰 SỐ DƯ HIỆN TẠI:** {int(budget_remaining):,}")
