import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory

# Cấu hình API Gemini
GEMINI_API_KEY = st.secrets["gemini"]["google_api_key"]
chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp", google_api_key=GEMINI_API_KEY)

# Cấu hình bộ nhớ chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kết nối với Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(credentials)
SPREADSHEET_ID = "1pWDgcnuznQDXz-bOw1fttpZZP1-HWnW9nnznUsFHc7A"

def load_data(sheet_name):
    try:
        worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
        return pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()

people_df = load_data("NguoiThamGia")
chi_phi_df = load_data("ChiPhi_LichTrinh")
lich_trinh_df = load_data("LichTrinh")

people_list = ", ".join(people_df["Họ và Tên"].tolist())
total_budget = people_df["Budget"].sum()
total_fixed_cost = chi_phi_df["Chi phí"].sum()
total_plan_cost = lich_trinh_df["Chi phí"].sum()
remaining_budget = total_budget - (total_fixed_cost + total_plan_cost)

import pandas as pd

def ask_ai(question):
    # Tìm ngày cụ thể nếu có trong câu hỏi
    detected_date = None
    for date in sorted(lich_trinh_df["Ngày"].unique()):
        if date in question:
            detected_date = date
            break

    # Tạo danh sách lịch trình
    schedule_summary = {}
    for date in sorted(lich_trinh_df["Ngày"].unique()):
        activities = lich_trinh_df[lich_trinh_df["Ngày"] == date]
        activity_list = "\n".join(
            f"- {row['Thời gian']}: {row['Địa điểm']} ({row['Địa chỉ']})"
            + (f" 🔗 [{row['Link tham khảo']}]({row['Link tham khảo']})" if row['Link tham khảo'] else "")
            + f" 💰 {row['Chi phí']:,} VND"
            for _, row in activities.iterrows()
        )
        schedule_summary[date] = activity_list

    # Chỉ hiển thị lịch trình của ngày được hỏi (nếu có)
    if detected_date:
        schedule_info = f"📅 Ngày {detected_date}:\n{schedule_summary[detected_date]}"
    else:
        schedule_info = "\n\n".join(f"📅 Ngày {date}:\n{activities}" for date, activities in schedule_summary.items())

    # Prompt linh hoạt hỗ trợ cả tài chính & lịch trình
    prompt = f"""
    Bạn là một trợ lý thông minh hỗ trợ lập kế hoạch chuyến đi Đà Lạt. Dữ liệu của bạn gồm:
    
    🧑‍🤝‍🧑 **Danh sách người tham gia**: {people_list}
    💰 **Tài chính**:
      - Tổng ngân sách: {total_budget:,} VND
      - Tổng chi phí cố định: {total_fixed_cost:,} VND
      - Số dư còn lại: {remaining_budget:,} VND

    📆 **Lịch trình chuyến đi**:
    {schedule_info}

    Người dùng có thể hỏi về **tài chính** hoặc **lịch trình**. Trả lời rõ ràng, dễ hiểu.
    Người dùng hỏi: {question}
    """

    # Gửi câu hỏi vào mô hình AI
    response = chat_model.invoke([SystemMessage(content=prompt), HumanMessage(content=question)])
    return response.content

st.title("💬 Trợ lý AI - Đà Lạt Planning")

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập tin nhắn
user_input = st.chat_input("Hãy đặt câu hỏi về ngân sách & lịch trình của bạn:")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = ask_ai(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
