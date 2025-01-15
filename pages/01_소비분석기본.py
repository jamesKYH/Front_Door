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

# 세션 상태에서 데이터 가져오기
if "data" in st.session_state:
    df = st.session_state["data"]
    st.write("데이터 미리보기:")
    st.write(df.head())

    # 데이터 기본 통계
    st.write("데이터 통계 요약:")
    st.write(df.describe())
else:
    st.warning("메인 페이지에서 데이터를 먼저 로드하세요.")