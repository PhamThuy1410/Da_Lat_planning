import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Kết nối với Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Lấy thông tin service account từ secrets
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(credentials)

# Thay bằng ID Google Sheets thực tế của bạn
SPREADSHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"

# Hàm lấy dữ liệu từ Google Sheets
def load_data(sheet_name):
    """Đọc dữ liệu từ Google Sheets và trả về DataFrame."""
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()

# Hàm lưu dữ liệu lên Google Sheets
def save_data(sheet_name, df):
    """Lưu DataFrame vào Google Sheets."""
    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success(f"Dữ liệu {sheet_name} đã lưu thành công!")
    except Exception as e:
        st.error(f"Lỗi khi lưu dữ liệu: {e}")

# Giao diện Streamlit
def main():
    st.title("Project: Đà Lạt Planning")

    # Bảng chi phí
    st.header("Bảng Chi Phí")
    chi_phi_df = load_data("ChiPhi")
    
    if chi_phi_df.empty:  # Nếu sheet trống hoặc lỗi, khởi tạo dữ liệu mặc định
        chi_phi_df = pd.DataFrame({
            "Khoản Chi": ["Tiền xe khách", "Tiền xăng", "Tiền thuê xe máy", "Tiền khách sạn", "Chi phí khác"],
            "Số Tiền (VND)": [0, 0, 0, 0, 0]
        })
    
    chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")
    
    total_cost = chi_phi_df["Số Tiền (VND)"].sum()
    st.write(f"### Tổng Chi Phí: {total_cost:,} VND")
    
    if st.button("Lưu Chi Phí"):
        save_data("ChiPhi", chi_phi_df)

    # Bảng kế hoạch lịch trình
    st.header("Kế Hoạch Lịch Trình")
    plan_df = load_data("LichTrinh")

    if plan_df.empty:  # Nếu sheet trống hoặc lỗi, khởi tạo dữ liệu mặc định
        plan_df = pd.DataFrame({
            "Thời Gian": [""],
            "Địa Điểm": [""],
            "Ước Tính Chi Phí (VND)": [0]
        })
    
    plan_df = st.data_editor(plan_df, num_rows="dynamic", key="plan")
    
    total_plan_cost = plan_df["Ước Tính Chi Phí (VND)"].sum()
    st.write(f"### Tổng Ước Tính Chi Phí Lịch Trình: {total_plan_cost:,} VND")
    
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
