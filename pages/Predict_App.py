import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd

# Cấu hình tiêu đề tab và icon
st.set_page_config(
    page_title="App Dự đoán Churn - Telco",
    page_icon="D:\\DA\\Tự học\\Customer Churn Prediction\\public\\img\\Logo.png",
    layout="centered"
)

st.title("Ứng dụng dự báo khách hàng rời bỏ của Telco")
st.markdown("<h2 style='text-align: center; font-size:20px;'><b>Nhập thông tin khách hàng để dự đoán họ có rời bỏ dịch vụ hay không</b></h2><br>", unsafe_allow_html=True)

# Load mô hình, scaler và danh sách cột đã lưu
# Xác định thư mục gốc của project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # …/pages
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # project root

# Build đường dẫn tuyệt đối đến model và feature_names
model_path = os.path.join(PROJECT_ROOT, "Model", "Churn_Model.pkl")
feature_names_path = os.path.join(PROJECT_ROOT, "Model", "Feature_Names.pkl")

# Load chúng
model = joblib.load(model_path)
feature_names = joblib.load(feature_names_path)

# ——— Định nghĩa callbacks để đẩy giá trị vào session_state ———
def on_internet_change():
    if st.session_state.InternetService == "No":
        # Bắt buộc PhoneService = Yes
        st.session_state.PhoneService = "Yes"
        # Các dịch vụ Internet phụ thuộc
        for field in [
            "OnlineBackup", "StreamingTV", "StreamingMovies",
            "DeviceProtection", "TechSupport", "OnlineSecurity"
        ]:
            st.session_state[field] = "No internet service"

def on_phone_change():
    if st.session_state.PhoneService == "No":
        st.session_state.MultipleLines = "No phone service"
        st.session_state.InternetService = "DSL" 

# Khởi tạo session_state keys với giá trị mặc định nếu chưa có
defaults = {
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "Yes",
    "DeviceProtection": "Yes",
    "TechSupport": "Yes",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Tạo bố cục 3 cột
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='text-align: center; font-size:17px;'><b>Nhân khẩu học</b></h3>", unsafe_allow_html=True)
    gender = st.selectbox("Giới tính", ["Male", "Female"])
    SeniorCitizen = st.selectbox("Khách hàng cao tuổi", ["No", "Yes"])
    Partner = st.selectbox("Có người thân", ["No", "Yes"])
    Dependents = st.selectbox("Có người phụ thuộc", ["No", "Yes"])
    
with col2:
    st.markdown("<h3 style='text-align: center; font-size:17px;'><b>Thông tin dịch vụ</b></h3>", unsafe_allow_html=True)
    InternetService = st.selectbox("Loại Internet", ["DSL", "Fiber optic", "No"], key="InternetService", on_change=on_internet_change)
    PhoneService = st.selectbox("Có dịch vụ điện thoại", ["No", "Yes"], key="PhoneService", on_change=on_phone_change)
    
    #Tạo dynamic options cho MultipleLines
    if InternetService == "No" or InternetService == "Fiber optic" or PhoneService == "Yes":
        ml_options = ["Yes", "No"]            # Khi không có Internet chỉ cần Yes/No
    else:   
        ml_options = ["Yes", "No", "No phone service"]  # Bình thường có 3 lựa chọn
    MultipleLines = st.selectbox("Dịch vụ nhiều đường dây", ml_options, key="MultipleLines")

with col3:
    st.markdown("<h3 style='text-align: center; font-size:17px;'><b>Dịch vụ liên quan Internet</b></h3>", unsafe_allow_html=True)
    OnlineSecurity = st.selectbox("Bảo mật trực tuyến", ["No", "Yes", "No internet service"], key="OnlineSecurity")
    OnlineBackup = st.selectbox("Sao lưu trực tuyến", ["No", "Yes", "No internet service"], key="OnlineBackup")
    DeviceProtection = st.selectbox("Bảo vệ thiết bị", ["No", "Yes", "No internet service"], key="DeviceProtection")
    TechSupport = st.selectbox("Hỗ trợ kỹ thuật", ["No", "Yes", "No internet service"], key="TechSupport")
    StreamingMovies = st.selectbox("Dịch vụ phim trực tuyến", ["No", "Yes", "No internet service"], key="StreamingMovies")
    StreamingTV = st.selectbox("Dịch vụ TV trực tuyến", ["No", "Yes", "No internet service"], key="StreamingTV")


st.markdown("<h3 style='text-align: center; font-size:17px;'><b>Thông tin thanh toán</b></h3>", unsafe_allow_html=True)
Contract = st.selectbox("Loại hợp đồng", ["Month-to-month", "One year", "Two year"])
tenure = st.slider("Tenure (months)", min_value=1, max_value=72, value=0)
PaperlessBilling = st.selectbox("Hóa đơn điện tử", ["No", "Yes"])
PaymentMethod = st.selectbox("Phương thức thanh toán", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
MonthlyCharges = st.number_input("Cước phí hàng tháng", min_value=0.0, step=10.0)
TotalCharges = st.number_input("Cước phí hàng năm", min_value=0.0, step=10.0)


# Tạo DataFrame từ dữ liệu nhập
user_input = pd.DataFrame([{
    "gender": gender,
    "SeniorCitizen": SeniorCitizen,
    "Partner": Partner,
    "Dependents": Dependents,
    "tenure": tenure,
    "PhoneService": PhoneService,
    "MultipleLines": MultipleLines,
    "InternetService": InternetService,
    "OnlineSecurity": OnlineSecurity,
    "OnlineBackup": OnlineBackup,
    "DeviceProtection": DeviceProtection,
    "TechSupport": TechSupport,
    "StreamingTV": StreamingTV,
    "StreamingMovies": StreamingMovies,
    "Contract": Contract,
    "PaperlessBilling": PaperlessBilling,
    "PaymentMethod": PaymentMethod,
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges
}])

st.write("Dữ liệu nhập:", user_input)

# One-Hot Encoding giống như khi train (vd: sử dụng pd.get_dummies() với drop_first=True)
user_input_encoded = pd.get_dummies(user_input, drop_first=True)

# Đảm bảo dữ liệu có đầy đủ các cột như khi train
user_input_encoded = user_input_encoded.reindex(columns=feature_names, fill_value=0)

# Dự đoán kết quả
if st.button("Dự đoán"):
    missing = []
    if tenure is None or tenure <= 0:
        missing.append("Tenure")
    if MonthlyCharges is None or MonthlyCharges <= 0:
        missing.append("MonthlyCharges")
    if TotalCharges is None or TotalCharges <= 0:
        missing.append("TotalCharges")
    if missing:
        st.warning(f"👉 **Vui lòng nhập chỉ số cho: {', '.join(missing)}**")
    else:
        # 1. Dự đoán label
        pred_label = model.predict(user_input_encoded)[0]
    
        # 2. Lấy xác suất churn (giả sử class 1 = churn)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(user_input_encoded)[0][1]
        else:
            # Nếu model không hỗ trợ predict_proba, bạn có thể dùng decision_function()
            proba = None

        # 3. Hiển thị kết quả
        if pred_label == 1:
            st.error("👉 Kết quả dự đoán: **Khách hàng có khả năng rời bỏ**")
        else:
            st.success("👉 Kết quả dự đoán: **Khách hàng có khả năng ở lại**")

        # 4. Hiển thị xác suất
        if proba is not None:
            pct = round(proba * 100, 2)
            st.write(f"**Xác suất churn:** {pct}%")

            # 5. Lời khuyên dựa trên mức độ rủi ro
            if pct > 75:
                st.warning("⚠️ Rủi ro rất cao! Cân nhắc ngay chương trình khuyến mãi hoặc ưu đãi riêng.")
            elif pct > 50:
                st.info("ℹ️ Rủi ro trung bình. Bạn có thể liên hệ chăm sóc khách hàng để giữ chân.")
            else:
                st.success("✅ Rủi ro thấp. Khách hàng có xu hướng trung thành.")
        else:
            st.write("Không thể tính xác suất cho mô hình này.")


