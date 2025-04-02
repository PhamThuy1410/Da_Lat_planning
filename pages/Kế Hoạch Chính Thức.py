import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread
from gspread_dataframe import set_with_dataframe

# Kết nối Google Sheets
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)
SPREADSHEET_ID = "your_google_sheet_id"
sheet = client.open_by_key(SPREADSHEET_ID)

def load_data(sheet_name):
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def save_data(sheet_name, df):
    worksheet = sheet.worksheet(sheet_name)
    worksheet.clear()
    set_with_dataframe(worksheet, df)

# Tải dữ liệu từ Google Sheets
guests_df = load_data("Guests")
fixed_costs_df = load_data("Fixed Costs")
plan_df = load_data("Plan")

total_budget = guests_df["Ngân sách"].sum()
plan_df["Chi phí"] = plan_df["Chi phí"].fillna(0)

# Tính toán số dư theo ngày
plan_df["Ngày"] = pd.to_datetime(plan_df["Ngày"], format="%d.%m.%Y")
plan_df = plan_df.sort_values(by="Ngày")

daily_costs = plan_df.groupby("Ngày")["Chi phí"].sum().reset_index()
daily_costs["Số dư"] = total_budget  # Gán số dư ban đầu

# Tính số dư cho từng ngày
for i in range(1, len(daily_costs)):
    daily_costs.loc[i, "Số dư"] = daily_costs.loc[i - 1, "Số dư"] - daily_costs.loc[i - 1, "Chi phí"]

# Hiển thị trên giao diện
st.title("Quản lý ngân sách chuyến đi Đà Lạt")
selected_date = st.selectbox("Chọn ngày để xem lịch trình:", daily_costs["Ngày"].dt.strftime("%d.%m.%Y"))
selected_date = datetime.strptime(selected_date, "%d.%m.%Y")

filtered_data = daily_costs[daily_costs["Ngày"] == selected_date]
if not filtered_data.empty:
    st.metric(label="Số dư hiện tại", value=f"{filtered_data.iloc[0]['Số dư']:,} VNĐ")
    st.metric(label="Tổng chi phí", value=f"{filtered_data.iloc[0]['Chi phí']:,} VNĐ")
else:
    st.warning("Không có dữ liệu cho ngày này.")
