import streamlit as st
import pandas as pd

def main():
    st.title("Project: Đà Lạt Planning")

    # Bảng chi phí
    st.header("Bảng Chi Phí")
    chi_phi_data = {
        "Khoản Chi": ["Tiền xe khách", "Tiền xăng", "Tiền thuê xe máy", "Tiền khách sạn", "Chi phí khác"],
        "Số Tiền (VND)": [0, 0, 0, 0, 0]
    }
    chi_phi_df = pd.DataFrame(chi_phi_data)

    # Sửa lỗi: Gán toàn bộ DataFrame thay vì chỉ một cột
    chi_phi_df = st.data_editor(chi_phi_df, num_rows="dynamic", key="chi_phi")

    # Tính tổng chi phí
    total_cost = chi_phi_df["Số Tiền (VND)"].sum()
    st.write(f"### Tổng Chi Phí: {total_cost:,} VND")

    # Bảng kế hoạch lịch trình
    st.header("Kế Hoạch Lịch Trình")
    plan_data = {
        "Thời Gian": [""],
        "Địa Điểm": [""],
        "Ước Tính Chi Phí (VND)": [0]
    }
    plan_df = pd.DataFrame(plan_data)

    # Cập nhật toàn bộ DataFrame thay vì chỉ một phần
    plan_df = st.data_editor(plan_df, num_rows="dynamic", key="plan")

    # Tổng chi phí lịch trình
    total_plan_cost = plan_df["Ước Tính Chi Phí (VND)"].sum()
    st.write(f"### Tổng Ước Tính Chi Phí Lịch Trình: {total_plan_cost:,} VND")

    # Xuất file CSV
    st.download_button(
        label="Tải Xuống Kế Hoạch (.csv)",
        data=plan_df.to_csv(index=False).encode('utf-8'),
        file_name="ke_hoach_du_lich.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()