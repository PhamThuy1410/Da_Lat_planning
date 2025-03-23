import streamlit as st
import requests
import datetime
from googletrans import Translator

def get_weather(api_key, city="Da Lat", country="VN"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Không thể lấy dữ liệu thời tiết. Hãy kiểm tra API Key!")
        return None

def translate_weather_description(description, translator):
    translated = translator.translate(description, src="en", dest="vi")
    return translated.text.capitalize()

def main():
    st.set_page_config(page_title="Thời tiết Đà Lạt", page_icon="🌤")
    st.title("☀️ Dự báo thời tiết Đà Lạt")
    
    api_key = "07db7577392d373d86074f5841de297e"  # Thay bằng API Key của bạn
    data = get_weather(api_key)
    
    if data:
        translator = Translator()
        st.sidebar.header("📅 Chọn ngày:")
        available_dates = sorted(set(item["dt_txt"].split(" ")[0] for item in data["list"]))
        selected_date = st.sidebar.selectbox("Chọn ngày dự báo:", available_dates)
        
        st.header(f"🌦 Dự báo thời tiết cho ngày {selected_date}")
        
        forecast_data = [item for item in data["list"] if item["dt_txt"].startswith(selected_date)]
        
        for entry in forecast_data:
            time = entry["dt_txt"].split(" ")[1]
            temp = entry["main"]["temp"]
            humidity = entry["main"]["humidity"]
            weather_desc = entry["weather"][0]["description"]
            weather_desc_vi = translate_weather_description(weather_desc, translator)
            
            st.subheader(f"⏰ {time}")
            st.write(f"🌡 Nhiệt độ: {temp}°C")
            st.write(f"💧 Độ ẩm: {humidity}%")
            st.write(f"☁️ Thời tiết: {weather_desc_vi}")
            st.write("---")

if __name__ == "__main__":
    main()