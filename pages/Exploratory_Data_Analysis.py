import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px # chart động
#function
from Data_Function import stacked_plot, stacked_table, get_color_palettes

st.set_page_config(
    page_title="Exploratory Data Analysis",
    page_icon="D:\\DA\\Tự học\\Customer Churn Prediction\\public\\img\\EDA.png",
    layout="centered"
)

st.title("Khám phá & Phân tích dữ liệu")

data = pd.read_csv("Dataset/Data_Analysis.csv")
churn_1, churn_2, churn_5, churn_10 = get_color_palettes()

st.markdown("<h1 style='font-size:25px;'><b>📄 I. Tìm hiểu dữ liệu</b></h1>", unsafe_allow_html=True)
st.dataframe(data.head(5))


st.markdown("<h2 style='font-size:22px;'><b>🔍 Tìm kiếm thông tin khách hàng (nếu muốn tìm khách hàng)</b></h2>", unsafe_allow_html=True)
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

st.markdown("<h2 style='font-size:25px;'><b>📈 II. Khám phá dữ liệu </b></h2>", unsafe_allow_html=True)

# Task 1
st.markdown("<h2 style='font-size:22px;'><b>1. Phân phối của các biến số được biểu diễn như thế nào?</b></h2>", unsafe_allow_html=True)
num_cols = ['TotalCharges', 'MonthlyCharges', 'tenure']
col = st.selectbox("Chọn biến số:", num_cols)
chart_type = st.radio("Chọn biểu đồ:", ["Histogram", "Boxplot"], horizontal=True)

# Cấu hình chung layout và axes
BASE_LAYOUT = dict(
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="sans-serif", size=14, color="black"),
    margin=dict(l=40, r=40, t=80, b=40)
)

AXIS_CONFIG = dict(
    title_font=dict(family="sans-serif", size=15, color="black"),
    tickfont=dict(family="sans-serif", size=12, color="black"), 
    zeroline=False,
    showgrid=True,
    gridcolor="lightgray",
    automargin=True
)

if chart_type == "Histogram":
    # tính padding 5%
    mn, mx = data[col].min(), data[col].max()
    pad = (mx - mn) * 0.05

    fig = px.histogram(data, x=col, nbins=30, color_discrete_sequence=["#F21616"])
    fig.update_layout(
        **BASE_LAYOUT,
        title_text=f"Histogram of {col}",
        title_x=0.5,               # căn giữa ngang
        title_xanchor='center',    # neo giữa
        title_font=dict(family="sans-serif", size=20, color="black")
    )
    fig.update_xaxes(title=col, range=[mn - pad, mx + pad], **AXIS_CONFIG)
    fig.update_yaxes(title="", **AXIS_CONFIG)

else:  # Boxplot
    fig = px.box(data, x=col, points="all", color_discrete_sequence=["#FF5152"])
    fig.update_layout(
        **BASE_LAYOUT,
        title_text=f"Boxplot of {col}",
        title_x=0.5,
        title_xanchor='center',
        title_font=dict(family="sans-serif", size=20, color="black")
    )
    fig.update_xaxes(title=col, **AXIS_CONFIG)
    fig.update_yaxes(title="", **AXIS_CONFIG)

st.plotly_chart(fig, use_container_width=True)
st.divider()

# Task 2
st.markdown("<h2 style='font-size:22px;'><b>2. Khách hàng có tenure thấp (<3 tháng) có churn cao hơn rõ rệt không?</b></h2>", unsafe_allow_html=True)
data['Churn_n'] = data['Churn'].map({'No': 0, 'Yes': 1})
data['NewCustomer'] = np.where(data['tenure'] < 3, 'Tenure < 3', 'Tenure ≥ 3')
churn_rate = (
    data.groupby('NewCustomer')['Churn_n']
      .mean()
      .reset_index()
)
churn_rate['Churn_n'] = churn_rate['Churn_n'] * 100
st.dataframe(churn_rate)
fig, ax = plt.subplots(figsize=(8, 6))
sb.barplot(data=churn_rate, x='NewCustomer', y='Churn_n', palette=churn_2)
st.pyplot(fig)
st.write("Trong 3 tháng đầu tiên, tỷ lệ rời cao xấp xỉ 60%, trong khi nó giảm còn 22%, từ 3 tháng về sau")
st.write("Điều này dễ hiểu bởi phần lớn khách hàng mới trong vài tháng đầu, khách hàng vẫn đang tìm hiểu dịch vụ, dễ đánh giá so sánh và sẵn sàng chuyển nhà mạng nếu chưa hài lòng.")
st.divider()

# Task 3
st.markdown("<h2 style='font-size:22px;'><b>3. Có phải khách hàng có Tổng phí thấp nhưng thời hạn sử dụng dài có xu hướng mất khách hàng nhiều?</b></h2>", unsafe_allow_html=True)
data_check = data.copy()
data_check['Churn'] = data_check['Churn'].map({'No': 0, 'Yes': 1})
# Xác định ngưỡng (median)
tenure_med = data_check['tenure'].median()
total_med  = data_check['TotalCharges'].median()
# Tạo phân đoạn: HighTenureLowTotal nếu tenure > median & TotalCharges < median
data_check['Segment'] = np.where(
    (data_check['tenure'] > tenure_med) & (data_check['TotalCharges'] < total_med),
    'KH Sử dụng lâu dài với chi phí thấp ',
    'KH còn lại'
)
# Tính churn rate theo phân đoạn
churn_rate = data_check.groupby('Segment')['Churn'].mean().rename("ChurnRate").reset_index()
churn_rate['ChurnRate'] = churn_rate['ChurnRate']*100
st.dataframe(churn_rate)
st.write("Chúng ta có thể thấy rằng tỷ lệ Churn của những khách hàng có Tổng phí thấp nhưng thời gian sử dụng dài thấp hơn những khách hàng còn lại.")
plt.figure(figsize=(8,6))
fig, ax = plt.subplots(figsize=(8, 6))
sb.scatterplot(
    data=data_check,
    x='tenure',
    y='TotalCharges',
    hue='Churn',
    alpha=0.5,
    palette=churn_2,
    ax=ax
)
st.pyplot(fig)
st.write("Khi quan sát biểu đồ, có thể thấy rằng hầu hết khách hàng churn đều ở trong tình trạng cả TotalCharges và Tenure đều tăng, và không có khách hàng churn nào khi TotalCharges từ [0,2000] và Tenure từ [50, 70].")  
st.write("  **Do đó, tuyên bố trên là sai**")
st.divider()

# Task 4
st.markdown("<h2 style='font-size:22px;'><b>4. Với Churn và Non-Churn, có sự khác biệt về số thời hạn hợp đồng (tenure) giữa hai nhóm không?</b></h2>", unsafe_allow_html=True)
churn = data[data["Churn"] == 'Yes']  
non_churn = data[data["Churn"] == 'No']      
st.write("- Trung bình thời hạn sử dụng cho KH rời bỏ:", churn["tenure"].mean())  
st.write("- Trung bình thời hạn sử dụng cho KH ở lại:", non_churn["tenure"].mean())  
st.write("Dễ dàng thấy trung bình, khách hàng Churn có thời gian sử dụng ngắn hơn đáng kể so với khách hàng Non-Churn. (trung bình 20 tháng)")  
st.write("Tiếp theo ta sẽ kiểm định 2 nhóm độc lập ")  
code = '''t_stat, p_value = ttest_ind(non_churn["tenure"], churn["tenure"],  equal_var=False)'''
st.code(code, language="python")
st.write("T-statistic: 34.97, P-value: 0.0000")
st.write("Vì P-value < 0.05 → Có sự khác biệt về số tháng sử dụng giữa hai nhóm.")
st.write("Tính khoảng tin cậy 95 cho 2 nhóm")
code = '''diff_mean = churn["tenure"].mean() - non_churn["tenure"].mean()  
    std_error = np.sqrt((churn["tenure"].var()/len(churn)) + (non_churn["tenure"].var()/len(non_churn)))     
    z_critical = norm.ppf(1 - (1 - 0.95)/2)     
    ci_lower = diff_mean - z_critical * std_error  
    ci_upper = diff_mean + z_critical * std_error
    '''
st.code(code, language="python")
st.write("Mean difference: -19.67 months - CI 95%: [-20.77 ; -18.57]")
st.divider()

# Task 5
st.markdown("<h2 style='font-size:22px;'><b>5. Liệu khách hàng ký hợp đồng ngắn hạn (hàng tháng) có tỷ lệ hủy hợp đồng cao hơn so với khách hàng ký hợp đồng dài hạn không?</b></h2>", unsafe_allow_html=True)
st.dataframe(pd.crosstab(data['Contract'], data['Churn'], dropna=False))
st.dataframe(stacked_table(data, 'Contract', 'Churn'))
fig, ax = plt.subplots(figsize=(8, 6))
stacked_plot(data, 'Contract', 'Churn', ax, colors=churn_2)
st.pyplot(fig)
st.write(
    """
    - Tỷ lệ phân chia gần 50:50 cho thấy khách hàng hợp đồng ngắn hạn (Tháng-Tháng) có tỷ lệ churn cao hơn so với khách hàng Một năm (11% churn) và Hai năm (3% churn)
    - Ngoài ra, khách hàng hợp đồng ngắn hạn có lượng khách hàng lớn hơn so với khách hàng hợp đồng dài hạn do lượng khách hàng mới đến trải nghiệm dịch vụ ngày càng tăng. Do đó, có thể hiểu được rằng khách hàng có nhiều khả năng rời đi trong năm đầu tiên
    """)
st.divider()

# Task 6
st.markdown("<h2 style='font-size:22px;'><b>6. Khách hàng sử dụng hình thức thanh toán thủ công (Séc điện tử, Séc thư) có khả năng rời bỏ dịch vụ cao hơn so với hình thức thanh toán tự động (Thẻ tín dụng, Chuyển khoản ngân hàng)?</b></h2>", unsafe_allow_html=True)
st.dataframe(pd.crosstab(data['PaymentMethod'], data['Churn'], dropna=False))
fig, ax = plt.subplots(figsize=(8, 6))
sb.barplot(data=data, x='PaymentMethod', y='TotalCharges', palette=churn_1)
st.pyplot(fig)
st.write("Có thể thấy rằng Tổng số lượng khách hàng và Tổng chi phí với Chuyển khoản ngân hàng (tự động) và Thẻ tín dụng (tự động) luôn cao hơn Séc điện tử và Séc gửi qua thư, nhưng điều này không khẳng định việc thanh toán thủ công có khả năng rời bỏ dịch vụ cao hơn (Có thể khách hàng nhiều dẫn đến tổng chi phí cao) nhưng điều này khẳng định việc khách hàng tin tưởng sử dụng dịch vụ")
data['Churn_n'] = data['Churn'].map({'No':0, 'Yes':1})
auto_pay   = ['Credit card (automatic)', 'Bank transfer (automatic)']
manual_pay = ['Electronic check', 'Mailed check']
data['PayGroup'] = np.where(
    data['PaymentMethod'].isin(auto_pay),
    'Auto‑Pay',
    'Manual‑Pay'
)
churn_rate = (
    data.groupby('PayGroup')['Churn_n']
      .mean()
      .reset_index()
)
churn_rate['Churn_n'] = (churn_rate['Churn_n'] * 100).round(2)
st.dataframe(churn_rate)
st.write("Có thể thấy rằng Tỉ lệ trung bình khách hàng rời bỏ của hình thức thanh toán thủ công (Séc điện tử, Séc thư) cao hơn")
st.write("**Do đó, tuyên bố trên là đúng**")
st.divider()

# Task 7
st.markdown("<h2 style='font-size:22px;'><b>7. Khách hàng đăng ký ≥ 2 dịch vụ (Điện thoại, Internet, Truyền hình) có tỷ lệ rời bỏ dịch vụ thấp hơn so với khách hàng chỉ đăng ký 1 dịch vụ</b></h2>", unsafe_allow_html=True)
data['HasInternet'] = np.where(data['InternetService'] == 'No', 0, 1)
data['HasTV'] = np.where(data['StreamingTV'] == 'Yes', 1, 0)
data['HasPhone'] = np.where(data['PhoneService'] == 'Yes', 1, 0)
data['Churn_n'] = data['Churn'].map({'No': 0, 'Yes': 1})
# Tính số dịch vụ mỗi khách hàng đăng ký
data['NumServices'] = data[['HasPhone','HasInternet','HasTV']].sum(axis=1)
# Phân nhóm: Single (1 dịch vụ) vs Multi (>=2 dịch vụ)
data['BundleGroup'] = np.where(data['NumServices'] >= 2, 'Multi-Service', 'Single-Service')
churn_rate = (
    data.groupby('BundleGroup')['Churn_n']
      .mean()
      .reset_index()
)
churn_rate['Churn_n'] = (churn_rate['Churn_n'] * 100).round(2)
st.dataframe(churn_rate)
st.write("Tỉ lệ rời bỏ của việc khách hàng đăng ký ≥ 2 dịch vụ khá cao so với khách hàng chỉ đăng ký 1 dịch vụ.")
code = '''ct = pd.crosstab(data_check['BundleGroup'], data_check['Churn'])
    chi2, p_value, dof, expected = chi2_contingency(ct)
    '''
st.code(code, language="python")
st.write("Chi-squared Statistic = 309.09 - P-value = 0.0000")
st.write("Vì P-value < 0.05 → Có sự khác biệt về số tháng sử dụng giữa hai nhóm.")
st.divider()

# Task 8
st.markdown("<h2 style='font-size:22px;'><b>8. Có phải Khách hàng có người phụ thuộc ít khách hàng rời bỏ hơn vì họ cần giữ liên lạc?</b></h2>", unsafe_allow_html=True)
churn_rate = (
    data_check
    .groupby('Dependents')['Churn']
    .mean()              # Trung bình 0/1 = tỷ lệ churn
    .reset_index()
)
churn_rate['Churn'] = churn_rate['Churn'] * 100
st.dataframe(churn_rate)
fig, ax = plt.subplots(figsize=(8, 6))
sb.barplot(data=churn_rate, x='Dependents', y='Churn', palette=churn_1)
plt.title("Churn Rate by Dependents")
plt.ylabel("% Churn")
st.pyplot(fig)
st.write("Dễ dàng thấy tỷ lệ khách hàng rời bỏ của khách hàng có người phụ thuộc bằng phân nửa của không có. Vì vậy giả định này đúng")
st.divider()
st.info("Cảm ơn vì đã xem 👍")







