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

        # Kiểm tra và ép kiểu dữ liệu
        for col in df.columns:
            if "VND" in col:  # Nếu cột chứa tiền, đảm bảo là số
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("Đã lưu thành công!")
    except Exception as e:
        st.error(f"Lỗi khi lưu dữ liệu: {e}")

def main():
    st.title("PROJECT: ĐÀ LẠT PLANNING")

    # Load danh sách người tham gia
    st.header("DANH SÁCH THAM GIA")
    people_df = load_data("NguoiThamGia")

    if people_df.empty:
        people_df = pd.DataFrame({"STT": [], "Họ và Tên": [], "Chi Phí (VNĐ)": []})

    # Xử lý dữ liệu: đảm bảo "Chi Phí (VNĐ)" không có NaN và là số nguyên
    people_df["STT"] = range(1, len(people_df) + 1)
    people_df["Họ và Tên"] = people_df["Họ và Tên"].astype(str)  # Ép kiểu về chuỗi

    # Xử lý cột "Chi Phí (VNĐ)"
    people_df["Chi Phí (VNĐ)"] = (
        pd.to_numeric(people_df["Chi Phí (VNĐ)"].astype(str).str.replace(",", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )

    # Hiển thị bảng chỉnh sửa dữ liệu
    people_df = st.data_editor(people_df, num_rows="dynamic", key="people")

    # Tổng số người & chi phí
    total_people = people_df["Họ và Tên"].nunique()
    total_cost_people = people_df["Chi Phí (VNĐ)"].sum()

    # Lưu dữ liệu khi nhấn nút
    if st.button("Lưu", key="save_people"):
        save_data("NguoiThamGia", people_df)

    col1, col2 = st.columns(2)

    # CSS để đổi màu xanh
    st.markdown(
        """
        <style>
            .metric-container {
                color: #00FF00 !important; /* Màu xanh */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    #Card KPI
    with col1:
        st.metric(label="👥 TỔNG SỐ NGƯỜI THAM GIA", value=total_people)
        st.markdown('<p class="metric-container">👥 TỔNG SỐ NGƯỜI THAM GIA</p>', unsafe_allow_html=True)
    
    with col2:
        st.metric(label="💰 TỔNG CHI PHÍ", value=f"{int(total_cost_people):,} VND")
        st.markdown('<p class="metric-container">💰 TỔNG CHI PHÍ</p>', unsafe_allow_html=True)



    # Bảng chi phí
    st.header("CHI PHÍ CỐ ĐỊNH")
    chi_phi_df = load_data("ChiPhi_LichTrinh")

    if chi_phi_df.empty:
        chi_phi_df = pd.DataFrame({
            "Khoản Chi": ["Tiền xe khách", "Tiền xăng", "Tiền thuê xe máy", "Tiền khách sạn", "Chi phí khác"],
            "Số Tiền (VND)": [0, 0, 0, 0, 0]
        })

    # Chuyển cột "Số Tiền (VND)" thành số, xử lý dấu phẩy nếu có
    chi_phi_df["Số tiền (VND)"] = (
        pd.to_numeric(chi_phi_df["Số tiền (VND)"].astype(str).str.replace(",", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )

    chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")

    total_cost_trip = chi_phi_df["Số tiền (VND)"].sum()
    st.write(f"### TỔNG CHI PHÍ: {total_cost_trip:,} VND")

    if st.button("Lưu", key="save_cost"):
        save_data("ChiPhi_LichTrinh", chi_phi_df)


    # Bảng kế hoạch lịch trình
    st.header("LỊCH TRÌNH VÀ CHI PHÍ")
    plan_df = load_data("LichTrinh")

    if plan_df.empty:
        plan_df = pd.DataFrame({
            "Ngày": [""],
            "Thời Gian": [""],
            "Địa điểm": [""],
            "Link tham khảo": [""],
            "Ước tính chi phí (VND)": [0]
        })

    # Xử lý dữ liệu: chuyển cột "Ước Tính Chi Phí (VND)" thành số nguyên
    plan_df["Ước tính chi phí (VND)"] = (
        pd.to_numeric(plan_df["Ước tính chi phí (VND)"].astype(str).str.replace(",", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )

    plan_df = st.data_editor(
    plan_df,
    num_rows="dynamic",
    key="plan",
    use_container_width=True,
    column_config={
        "Phân loại": st.column_config.SelectboxColumn(
            "Phân loại", options=["Checking", "Ăn uống"], required=True)
        }
    )

    total_plan_cost = plan_df["Ước tính chi phí (VND)"].sum()
    st.write(f"### TỔNG CHI PHÍ: {total_plan_cost:,} VND")

    if st.button("Lưu", key="save_plan"):
        save_data("LichTrinh", plan_df)

    # Hiển thị KPI Budget còn lại
    # Tính toán Budget còn lại
    budget_remaining = int(total_cost_people - (total_cost_trip + total_plan_cost))  # Đảm bảo kiểu int

    # Hiển thị KPI Budget còn lại
    st.header("💰 SỐ TIỀN CÒN LẠI")
    st.metric(label=" ", value=f"{budget_remaining:,} VND")

if __name__ == "__main__":
    main()
