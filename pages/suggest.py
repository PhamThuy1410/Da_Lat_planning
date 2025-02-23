import streamlit as st
import pandas as pd

# Khởi tạo session state nếu chưa có
if "data" not in st.session_state:
    st.session_state.data = []

st.title("Gợi ý thêm")

# Nhập thông tin
with st.form("suggest_form", clear_on_submit=True):
    ten_nguoi = st.text_input("Tên người *", placeholder="Nhập tên người")
    suggest = st.text_area("Gợi ý", placeholder="Nhập gợi ý (có thể để trống)")
    link = st.text_input("Link", placeholder="Nhập link (có thể để trống)")

    submitted = st.form_submit_button("Thêm vào bảng")

    if submitted and ten_nguoi:
        st.session_state.data.append({"Tên người": ten_nguoi, "Gợi ý": suggest, "Link": link})

# Hiển thị bảng với nút Xoá trên từng dòng
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    # Hiển thị bảng với các nút xoá
    for i, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])  # Chia layout
        col1.write(row["Tên người"])
        col2.write(row["Gợi ý"])
        col3.write(row["Link"])
        if col4.button("🗑️ Xoá", key=f"delete_{i}"):
            st.session_state.data.pop(i)
            st.rerun()  # Load lại trang để cập nhật bảng

else:
    st.write("🔹 Chưa có dữ liệu. Hãy thêm gợi ý!")

