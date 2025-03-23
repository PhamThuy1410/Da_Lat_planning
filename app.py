import streamlit as st

# Tiêu đề của ứng dụng
st.title("Đà Lạt Planning")

# Mô tả
st.write("Vui lòng chọn trang:")

# Hiển thị liên kết đến các trang
st.page_link("pages/Chat bot.py", label="Chat bot", icon="🤖")
st.page_link("pages/Lưu ý và ghi nhớ.py", label="Lưu Ý Và Ghi Nhớ", icon="🎈")
st.page_link("pages/Kế Hoạch Chính Thức.py", label="Kế Hoạch Chính Thức", icon="📖")
st.page_link("pages/Gợi ý.py", label="Gợi Ý", icon="💡")
st.page_link("pages/Weather.py", label="Thời tiết", icon="☁️")
