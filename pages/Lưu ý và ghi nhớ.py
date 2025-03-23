import streamlit as st

def main():
    st.set_page_config(page_title="Lưu ý và Ghi nhớ", page_icon="📝")
    
    st.title("📌 Lưu ý và Ghi nhớ cho Chuyến đi Đà Lạt")
    
    # Di chuyển
    st.header("🚍 Di chuyển")
    st.write("- **Xe khách Phương Trang**: Khởi hành lúc **05:00 ngày 17/04/2025** tại Bến xe miền Tây.")
    st.write("- Vui lòng đến trước **30 phút** để làm thủ tục check-in thuận tiện hơn.")
    
    # Phương tiện di chuyển tại Đà Lạt
    st.header("🏍 Phương tiện di chuyển tại Đà Lạt")
    st.write("- **Ngọc Dũng** - **0336 689 692** (Cho thuê xe máy).")
    
    # Chỗ ở
    st.header("🏨 Chỗ ở")
    st.write("- **Khách sạn ABC**")
    st.write("- **Địa chỉ**: 123 Đường Số 3, Phường 3, Thành phố Đà Lạt.")
    
    # Danh sách đồ cần mang theo
    st.header("🎒 Danh sách đồ cần mang theo")
    items = [
        "📱 Điện thoại",
        "🔋 Sạc dự phòng, sạc điện thoại",
        "🎧 Tai nghe",
        "🪪 Bằng lái xe + CCCD",
        "💵 Tiền mặt",
        "🪥 Bàn chải, kem đánh răng",
        "🌞 Kem chống nắng",
        "💄 Đồ skincare, make up",
        "🧣 Khăn tắm, khăn lau mặt - Nếu ngại sử dụng của khách sạn",
        "👕 Quần áo xinh",
        "🧥 Áo khoác lạnh, khăn choàng",
        "🧤 Vớ, bao tay, khăn choàng",
        "📷 Tripod",
        "👟 Giày, dép",
        "🤢 Thuốc say xe, túi chống nôn",
        "🧴 Dầu gội, sữa tắm",
        "🛍️ Bịch nilong đựng đồ dơ"
    ]
    for item in items:
        st.write(f"- {item}")
    
    # Lưu ý
    st.header("⚠️ Lưu ý quan trọng")
    st.write("- Kiểm tra đầy đủ giấy tờ tùy thân trước khi đi.")
    st.write("- Mang theo đủ tiền mặt và thẻ ngân hàng dự phòng.")
    st.write("- Đảm bảo điện thoại và sạc dự phòng đầy pin.")
    st.write("- Kiểm tra dự báo thời tiết trước để chuẩn bị trang phục phù hợp.")
    st.write("- Đừng quên thuốc cá nhân nếu bạn có bệnh lý riêng.")
    
    st.success("Hãy ghi nhớ những thông tin quan trọng này để có chuyến đi thuận lợi! 🏕️")

if __name__ == "__main__":
    main()