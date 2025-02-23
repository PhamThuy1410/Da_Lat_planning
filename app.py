import streamlit as st

# Tiêu đề của ứng dụng
st.title("Đà Lạt Planning")

# Mô tả
st.write("Vui lòng chọn trang: Planning hoặc Suggest")

# Hiển thị liên kết đến các trang
st.page_link("pages/Kế Hoạch Chính Thức.py", label="Trang Planning", icon="📖")
st.page_link("pages/Gợi ý.py", label="Trang Gợi Ý", icon="💡")
