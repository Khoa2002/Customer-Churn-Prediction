import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered"
) 

st.title("🏠 [VIE] Dự án khám phá và dự báo khách hàng rời bỏ")

url = "https://buisikhoa.notion.site/Customer-Churn-Prediction-Application-Deploy-1a798d2d62678020acf7c1cc7d5b24cf"
st.markdown("<h2 style='font-size:20px;'><b>Xem chi tiết dự án <a href = 'https://buisikhoa.notion.site/Customer-Churn-Prediction-Application-Deploy-1a798d2d62678020acf7c1cc7d5b24cf'> ở đây</a>", unsafe_allow_html=True)

st.markdown("<h2 style='font-size:30px;'><b>📰 1. Thông tin dự án</b></h2>", unsafe_allow_html=True)

st.write("Trong ngành viễn thông, giữ chân khách hàng là một thách thức lớn. Mọi doanh nghiệp đều muốn giữ chân khách hàng trong thời gian dài để tăng doanh thu. Tuy nhiên, nhiều khách hàng có xu hướng rời bỏ dịch vụ (churn) vì nhiều lý do khác nhau.")
st.write("Dự án này tập trung vào việc dự đoán liệu khách hàng có rời bỏ dịch vụ hay không dựa trên các biến dữ liệu như hành vi sử dụng dịch vụ, loại hợp đồng, phương thức thanh toán, v.v. Mục tiêu cuối cùng là giúp các doanh nghiệp xác định những khách hàng có nguy cơ rời bỏ cao để họ có thể đề xuất các chiến lược giữ chân hiệu quả.")

st.markdown("<h2 style='font-size:30px;'><b>🎯 2. Mục tiêu dự án</b></h2>", unsafe_allow_html=True)
st.write("**1. Xây dựng mô hình Machine Learning để dự đoán tỷ lệ churn của khách hàng và ưu tiên dự báo đúng những khách hàng sắp rời bỏ (không bỏ lỡ những khách hàng thực sự muốn rời đi).**")
st.write("**2. Xác định các yếu tố chính ảnh hưởng đến churn.**")
st.write("**3. Đề xuất các chiến lược để giảm tỷ lệ churn, tối ưu hóa doanh thu kinh doanh.**")
st.write("**4. Xây dựng ứng dụng để dự đoán tỷ lệ churn của khách hàng dựa trên các yếu tố liên quan.**")


st.markdown("<h2 style='font-size:30px;'><b>🔍 3. Tìm kiếm thông tin khách hàng</b></h2>", unsafe_allow_html=True)
data = pd.read_csv("Dataset/raw_data.csv")
st.write("Nhập **Customer ID** để tìm kiếm thông tin khách hàng trong hệ thống.")
customer_id = st.text_input("Nhập mã khách hàng (customerID):", "").strip()

if customer_id:
    # Lọc dữ liệu chứa customer_id (không phân biệt chữ hoa/thường)
    result = data[data["customerID"].astype(str).str.contains(customer_id, case=False, na=False)]

    if not result.empty:
        st.success(f"✅ Tìm thấy khách hàng: **{customer_id}**")
        st.dataframe(result)
    else:
        st.warning(f"🆘 Không tìm thấy khách hàng với mã **{customer_id}**.")