import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered"
) 

data = pd.read_csv("Dataset/Data_Analysis.csv")
data_raw = pd.read_csv("Dataset/Data_Raw.csv")

# Title
st.title("[VIE] Dự án khám phá và dự báo khách hàng rời bỏ")
img = Image.open("D:\\DA\\Tự học\\Customer Churn Prediction\\public\\img\\Overview.png")
new_width = 800
new_height = 400
img = img.resize((new_width, new_height))
st.image(img)    

st.markdown("<b>Xem chi tiết dự án ở <a style='color: #ff5152;' " \
"href = 'https://buisikhoa.notion.site/Customer-Churn-Prediction-Application-Deploy-1a798d2d62678020acf7c1cc7d5b24cf'> Notion</a> và code ở <a style='color: grey;' href = 'https://github.com/Khoa2002/Customer_Churn_Prediction'> Github</a>", unsafe_allow_html=True)

### Overview
st.markdown("<h1 style='font-size:25px;'><b>📰 I. Thông tin dự án</b></h1>", unsafe_allow_html=True)
st.write(
    """
        - Trong ngành viễn thông, giữ chân khách hàng là một thách thức lớn. Mọi doanh nghiệp đều muốn giữ chân khách hàng trong thời gian dài để tăng doanh thu. Tuy nhiên, nhiều khách hàng có xu hướng rời bỏ dịch vụ (churn) vì nhiều lý do khác nhau. 
        - Dự án này tập trung vào việc dự đoán liệu khách hàng có rời bỏ dịch vụ hay không dựa trên các biến dữ liệu như hành vi sử dụng dịch vụ, loại hợp đồng, phương thức thanh toán, v.v. 
        - Mục tiêu cuối cùng là giúp các doanh nghiệp xác định những khách hàng có nguy cơ rời bỏ cao để họ có thể đề xuất các chiến lược giữ chân hiệu quả.
    """)

### Target
st.markdown("<h1 style='font-size:25px;'><b>🎯 II. Mục tiêu dự án</b></h1>", unsafe_allow_html=True)
st.write(
    """
    - Xây dựng mô hình Machine Learning để dự đoán tỷ lệ churn của khách hàng và ưu tiên dự báo đúng những khách hàng sắp rời bỏ (không bỏ lỡ những khách hàng thực sự muốn rời đi).
    - Xác định các yếu tố chính ảnh hưởng đến churn.
    - Đề xuất các chiến lược để giảm tỷ lệ churn, tối ưu hóa doanh thu kinh doanh.
    - Xây dựng ứng dụng để dự đoán tỷ lệ churn của khách hàng dựa trên các yếu tố liên quan.
    """)


### Skill Learned
st.markdown("<h1 style='font-size:25px;'><b>🥅 III. Kỹ năng học được</b></h1>", unsafe_allow_html=True)
st.write(
    """
    - Kiến thức trong lĩnh vực viễn thông (Telecom).
    - Kỹ năng làm sạch dữ liệu, Phân tích và khám phá dữ liệu.
    - Tiền xử lý dữ liệu, kỹ thuật Feature engineering, triển khai Machine Learning Model cùng các chỉ số đo lường hiệu suất Model. 
    - Triển khai và phát triển ứng dụng trên StreamlitApp.
    """)

### Domain Knowledge
st.markdown("<h1 style='font-size:25px;'><b>💡 IV. Kiến thức nền tảng</b></h1>", unsafe_allow_html=True)
img = Image.open("D:\\DA\\Tự học\\Customer Churn Prediction\\public\\img\\Logo.png")
new_width = 800
new_height = 400
img = img.resize((new_width, new_height))
st.image(img)    
st.markdown("<h2 style='font-size:20px;'><b>❓ 1. Customer Churn</b></h2>", unsafe_allow_html=True)
st.write(
    """
    - Customer Churn là tình trạng mất khách hàng hoặc người đăng ký vì bất kỳ lý do gì. 
    - Công thức: 
    """)
st.markdown(
    "<p style='text-align:center;'><strong>Churn Rate = (Số khách hàng rời đi / Tổng số khách hàng) * 100%</strong></p>",
    unsafe_allow_html=True
)
st.write(
    """
    - Các doanh nghiệp đo lường và theo dõi tỷ lệ bỏ đi dưới dạng phần trăm khách hàng đã mất so với tổng số khách hàng trong một khoảng thời gian nhất định. Số liệu này thường được theo dõi hàng tháng và báo cáo vào cuối tháng.
    - Ngành viễn thông là một trong những ngành có Churn rate cao do sự cạnh tranh khốc liệt giữa các nhà mạng. Khách hàng có thể dễ dàng chuyển từ nhà cung cấp này sang nhà cung cấp khác nếu họ thấy dịch vụ rẻ hơn, chất lượng tốt hơn hoặc chương trình khuyến mãi hấp dẫn hơn. Vì vậy việc hiểu rõ thị trường và tệp khách hàng của bạn là chìa khóa để giảm tỷ lệ bỏ đi chính xác hơn.
    - Customer Churn là thuật ngữ được sử dụng để mô tả số lượng khách hàng ngừng sử dụng sản phẩm hoặc dịch vụ của doanh nghiệp trong một khoảng thời gian nhất định.
    """)

st.markdown("<h2 style='font-size:20px;'><b>❓ 2. Customer Churn Prediction trong Machine Learning</b></h2>", unsafe_allow_html=True)
st.write(
    """
    - Điều quan trọng đối với bất kỳ tổ chức nào xử lý khách hàng thường xuyên là tìm cách giữ chân những khách hàng hiện tại. Customer Churn Prediction nói về việc dự đoán khả năng khách hàng hủy sản phẩm hoặc dịch vụ của công ty.
    - Việc tạo ra mô hình Cutomer Churn Prediction iên quan đến việc sử dụng dữ liệu khách hàng trong quá khứ để dự đoán khả năng khách hàng hiện tại rời bỏ hoặc tiếp tục sử dụng một dịch vụ/sản phẩm cụ thể.
    - Bên cạnh đó, các mô hình dự đoán xác định các xu hướng và mô hình khác nhau trong dữ liệu để dự báo tỷ lệ khách hàng rời bỏ.
    """)

st.info("Cảm ơn vì đã xem 👍")