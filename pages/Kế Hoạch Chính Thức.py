import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Kết nối với Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(credentials)
SPREADSHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"

def load_data(sheet_name):
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()

def save_data(sheet_name, df):
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("Đã lưu thành công!")
    except Exception as e:
        st.error(f"Lỗi khi lưu dữ liệu: {e}")

def main():
    st.title("Project: Đà Lạt Planning")

    # Load danh sách người tham gia
    st.header("Danh Sách Người Tham Gia")
    people_df = load_data("NguoiThamGia")
    if people_df.empty:
        people_df = pd.DataFrame({"STT": [], "Họ và Tên": [], "Chi Phí (VNĐ)": []})
    
    people_df["STT"] = range(1, len(people_df) + 1)
    people_df["Họ và Tên"] = people_df["Họ và Tên"].astype(str)  # Ép kiểu về chuỗi
    people_df = st.data_editor(people_df, num_rows="dynamic", key="people")
    
    
    total_people = people_df["Họ và Tên"].nunique()
    total_cost_people = people_df["Chi Phí (VNĐ)"].sum()
    
    if st.button("Lưu Danh Sách Người Tham Gia"):
        save_data("NguoiThamGia", people_df)

    # KPI Cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="👥 Tổng Số Người Tham Gia", value=total_people)
    with col2:
        st.metric(label="💰 Tổng Chi Phí Người Tham Gia", value=f"{int(total_cost_people):,} VND")

    # Bảng chi phí
    st.header("Bảng Chi Phí")
    chi_phi_df = load_data("ChiPhi_LichTrinh")
    if chi_phi_df.empty:
        chi_phi_df = pd.DataFrame({
            "Khoản Chi": ["Tiền xe khách", "Tiền xăng", "Tiền thuê xe máy", "Tiền khách sạn", "Chi phí khác"],
            "Số Tiền (VND)": [0, 0, 0, 0, 0]
        })
    chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")
    
    total_cost = chi_phi_df["Số Tiền (VND)"].sum()
    st.write(f"### Tổng Chi Phí: {total_cost:,} VND")
    
    if st.button("Lưu Chi Phí"):
        save_data("ChiPhi_LichTrinh", chi_phi_df)

    # Bảng kế hoạch lịch trình
    st.header("Kế Hoạch Lịch Trình")
    plan_df = load_data("LichTrinh")
    if plan_df.empty:
        plan_df = pd.DataFrame({
            "Ngày": [""],
            "Thời Gian": [""],
            "Địa Điểm": [""],
            "Link tham khảo": [""],
            "Ước Tính Chi Phí (VND)": [0]
        })
    plan_df = st.data_editor(plan_df, num_rows="dynamic", key="plan")
    
    total_plan_cost = plan_df["Ước Tính Chi Phí (VND)"].sum()
    st.write(f"### Tổng Ước Tính Chi Phí Lịch Trình: {int(total_plan_cost):,} VND")
    
    if st.button("Lưu Lịch Trình"):
        save_data("LichTrinh", plan_df)

    # Xuất file CSV
    st.download_button(
        label="Tải Xuống Kế Hoạch (.csv)",
        data=plan_df.to_csv(index=False).encode('utf-8'),
        file_name="ke_hoach_du_lich.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
