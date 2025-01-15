import streamlit as st
import pandas as pd
import FinanceDataReader as fdr 
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO 
import pandas as pd
import os
import plotly.express as px


st.title("데이터 보기")

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


if "data" not in st.session_state:
    file_path = 'https://woori-fisa-bucket.s3.ap-northeast-2.amazonaws.com/fisa04-card/tbsh_gyeonggi_day_202311_ansan.csv'
    st.session_state["data"] = load_data(file_path)

df = st.session_state["data"]
    
    
   
# 나이대별 소비 금액 분포
st.subheader("1. 나이대별 소비 금액 분포")
age_grouped = df.groupby('age')['amt'].sum().reset_index()
age_grouped['amt'] = age_grouped['amt'] / 1e6  # 금액 단위를 백만 원으로 변환

fig1 = px.bar(
    age_grouped,
    x='age',
    y='amt',
    title='나이대별 소비 금액 (백만 원 단위)',
    labels={'age': '나이대', 'amt': '소비 금액 (백만 원)'},
    text='amt'
)

# 숫자를 백만 원 단위로 표시
fig1.update_traces(
    texttemplate='%{text:.1f} 백만 원',  # 소수점 1자리
    textposition='outside'
)

# Hover 정보도 백만 원 단위로 표시
fig1.update_layout(
    xaxis=dict(tickmode='linear'),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial"
    )
)
fig1.update_yaxes(
    tickformat=",.1f",  # Y축의 숫자 포맷 (소수점 1자리)
    title="소비 금액 (백만 원)"
)

# 그래프 표시
st.plotly_chart(fig1)






# 나이대별 업종 선호도
st.subheader("2. 나이대별 업종 선호도")
top_industries = df.groupby(['age', 'card_tpbuz_nm_1'])['amt'].sum().reset_index()

fig2 = px.treemap(
    top_industries,
    path=['age', 'card_tpbuz_nm_1'],  
    values='amt', 
    title='나이대별 업종 선호도 (소비 금액 기준)',
    labels={'age': '나이대', 'card_tpbuz_nm_1': '업종', 'amt': '소비 금액'}
)
st.plotly_chart(fig2)

# 시간대별 소비 활동
st.subheader("3. 시간대별 소비 활동")
time_age_grouped = df.groupby(['hour', 'age'])['amt'].sum().reset_index()
fig3 = px.line(
    time_age_grouped,
    x='hour',
    y='amt',
    color='age',
    title='시간대별 나이대 소비 금액',
    labels={'hour': '시간대', 'amt': '소비 금액', 'age': '나이대'}
)
st.plotly_chart(fig3)

# 성별 및 나이대의 소비 차이
st.subheader("4. 성별 및 나이대의 소비 차이")
gender_age_grouped = df.groupby(['sex', 'age'])['amt'].sum().reset_index()
fig4 = px.bar(
    gender_age_grouped,
    x='age',
    y='amt',
    color='sex',
    barmode='group',
    title='성별 및 나이대별 소비 금액 비교',
    labels={'sex': '성별', 'age': '나이대', 'amt': '소비 금액'}
)
st.plotly_chart(fig4)