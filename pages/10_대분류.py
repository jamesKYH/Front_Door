import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="대분류 관련 그래프 출력", layout="wide")
st.title("📊 업종대분류 관련 정보")
st.markdown("이 페이지에서는 업종대분류에 관련된 다양한 내용을 제공합니다.")
# 세션 상태에서 데이터 불러오기
if "data" in st.session_state:
    df = st.session_state["data"]
else:
    st.warning("메인 페이지에서 데이터를 먼저 로드하세요.")
    st.stop()

# 업종대분류 목록 추출 및 선택
unique_main_categories = df["card_tpbuz_nm_1"].dropna().unique()
selected_category = st.selectbox("관심 있는 업종 대분류를 선택하세요:", sorted(unique_main_categories))
# 선택한 업종중분류로 데이터 필터링
filtered_df = df[df["card_tpbuz_nm_1"] == selected_category]
st.subheader(f"선택한 업종: {selected_category}")
