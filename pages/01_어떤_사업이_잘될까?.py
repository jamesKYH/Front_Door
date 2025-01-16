import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import get_combined_sampled_data  # 메인 코드에서 함수 가져오기

# 페이지 설정: 가장 처음에 위치
st.set_page_config(page_title="업종 대분류 분석", layout="wide")

# 페이지 제목 및 설명
st.title("📊 업종 대분류 분석")
st.markdown("""
    선택한 업종 대분류에 대한 소비 데이터와 트렌드를 시각적으로 분석합니다. 
    데이터는 월별, 성별, 연령대, 요일, 시간대별로 세분화하여 제공합니다.
""")
st.divider()

if "region_url" not in st.session_state:
    st.warning("지역을 먼저 선택하세요. 좌측 사이드바 main에서 지역을 선택해 주세요.")
    st.stop()  # 이후 코드를 실행하지 않음


region_url = st.session_state["region_url"]
sampled_df = get_combined_sampled_data(region_url)
if not sampled_df.empty:
    pass
else:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()
    
df = sampled_df.copy()



# 'ta_ymd' 열에서 월(month) 정보 추출
df['month'] = pd.to_datetime(df['ta_ymd'], format='%Y%m%d').dt.month
# 업종 대분류 선택
st.markdown("## 🔍 업종 대분류 선택")
unique_main_categories = df["card_tpbuz_nm_1"].dropna().unique()
selected_category = st.selectbox("관심 있는 업종 대분류를 선택하세요:", sorted(unique_main_categories))

# 데이터 필터링
filtered_df = df[df["card_tpbuz_nm_1"] == selected_category]
if filtered_df.empty:
    st.warning(f"선택한 대분류 업종 '{selected_category}'에 해당하는 데이터가 없습니다.")
    st.stop()

# 선택한 대분류 표시
st.markdown(f"**선택한 업종 대분류: {selected_category}**")
st.divider()

# 인사이트 제공 기능 추가
# 전체 업종 대분류와 선택된 업종 대분류 비교
st.markdown("### 📊 인사이트 제공")

# 전체 업종 평균 및 선택 업종 매출 데이터 계산
category_comparison = df.groupby("card_tpbuz_nm_1").agg(
    total_sales=("amt", "sum"),
    total_transactions=("cnt", "sum")
).reset_index()

# 선택된 업종의 데이터 추출
selected_category_data = category_comparison[
    category_comparison["card_tpbuz_nm_1"] == selected_category
]

if not selected_category_data.empty:
    selected_sales = selected_category_data["total_sales"].values[0]
    selected_transactions = selected_category_data["total_transactions"].values[0]

    # 전체 평균 계산
    average_sales = category_comparison["total_sales"].mean()
    average_transactions = category_comparison["total_transactions"].mean()

    # 인사이트 출력
    if selected_sales > average_sales:
        st.success(
            f"✅ **{selected_category}** 업종의 총 매출은 **다른 업종 대분류 평균보다 높습니다**."
        )
    else:
        st.warning(
            f"⚠️ **{selected_category}** 업종의 총 매출은 **다른 업종 대분류 평균보다 낮습니다**."
        )

    if selected_transactions > average_transactions:
        st.success(
            f"✅ **{selected_category}** 업종의 총 소비 건수는 **다른 업종 대분류 평균보다 높습니다**."
        )
    else:
        st.warning(
            f"⚠️ **{selected_category}** 업종의 총 소비 건수는 **다른 업종 대분류 평균보다 낮습니다**."
        )

    # 단가 분석
    selected_avg_unit_price = selected_sales / selected_transactions if selected_transactions > 0 else 0
    overall_avg_unit_price = average_sales / average_transactions if average_transactions > 0 else 0

    if selected_avg_unit_price > overall_avg_unit_price:
        st.info(
            f"💡 **{selected_category}** 업종은 단가가 높은 상품을 판매할 가능성이 있습니다. "
            "고객당 구매 금액이 다른 업종보다 높습니다."
        )
    else:
        st.info(
            f"💡 **{selected_category}** 업종은 단가가 낮은 상품을 판매할 가능성이 있습니다. "
            "고객당 구매 금액이 다른 업종보다 낮습니다."
        )
else:
    st.warning("선택된 업종 대분류에 대한 데이터를 찾을 수 없습니다.")

# 선택된 업종과 다른 업종 간 매출 비교 시각화
fig6 = px.bar(
    category_comparison,
    x="card_tpbuz_nm_1",
    y="total_sales",
    title=f"{selected_category} 업종과 다른 업종 간 매출 비교",
    labels={"card_tpbuz_nm_1": "업종 대분류", "total_sales": "총 매출 금액"},
    color="card_tpbuz_nm_1",
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig6.update_traces(marker_line_width=1.5, marker_line_color="black")
st.plotly_chart(fig6, use_container_width=True)
st.divider()




# 1. 월별 매출 금액 추이
st.markdown("#### 📈 월별 매출 금액 추이")
st.write("월별 매출 데이터를 통해 성수기와 비수기를 파악할 수 있습니다. 이를 활용하여 특정 달에 맞춘 마케팅 전략을 수립하세요.")
monthly_sales = filtered_df.groupby("month")["amt"].sum().reset_index()
fig1 = px.line(
    monthly_sales, x="month", y="amt",
    title="월별 총 매출 금액 추이",
    labels={"month": "월", "amt": "매출 금액"},
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)
st.divider()
# 2. 성별 매출 비율
st.markdown("#### 👫 성별 매출 비율")
st.write("성별에 따른 매출 비율을 확인하여 주요 소비층을 식별하고, 성별에 특화된 상품과 프로모션을 기획하세요.")
gender_sales = filtered_df.groupby("sex")["amt"].sum().reset_index()
fig2 = px.pie(
    gender_sales, values="amt", names="sex",
    title="성별 매출 비율",
    color_discrete_map={'M': 'blue', 'F': 'pink'}
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# 3. 성별 및 연령대별 매출 비교
st.markdown("#### 👥 성별 & 연령대별 매출 비교")
st.write("연령대와 성별 데이터를 조합하여 소비자 행동을 더 깊이 이해할 수 있습니다. 특정 연령층을 타겟으로 한 맞춤형 마케팅이 가능합니다.")
sales_by_gender_age = filtered_df.groupby(['sex', 'age'])['amt'].sum().reset_index()
fig3 = px.bar(
    sales_by_gender_age, x='age', y='amt', color='sex',
    barmode='group',
    labels={'amt': '매출 금액', 'age': '연령대', 'sex': '성별'},
    title='성별 및 연령대별 매출 비교',
    color_discrete_map={'M': 'blue', 'F': 'pink'}
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# 4. 요일별 소비 패턴 분석
st.markdown("#### 📅 요일별 소비 패턴 분석")
st.write("요일별 소비 금액과 건수를 분석하여 매출이 집중되는 요일을 파악하고, 특정 요일에 맞춘 프로모션을 계획하세요.")
day_mapping = {
    1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토', 7: '일'
}
filtered_df["day_name"] = filtered_df["day"].map(day_mapping)
weekday_data = filtered_df.groupby("day_name").agg(
    total_amount=("amt", "sum"),
    total_count=("cnt", "sum")
).reset_index()

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=weekday_data['day_name'], y=weekday_data['total_amount'],
    mode='lines+markers', name='소비 금액',
    line=dict(color='#1F77B4'), marker=dict(size=8)
))
fig4.add_trace(go.Scatter(
    x=weekday_data['day_name'], y=weekday_data['total_count'],
    mode='lines+markers', name='소비 건수',
    line=dict(color='#FF7F0E'), marker=dict(size=8), yaxis='y2'
))
fig4.update_layout(
    title="요일별 소비 금액 및 건수",
    xaxis=dict(title="요일"),
    yaxis=dict(title="소비 금액", titlefont=dict(color='#1F77B4')),
    yaxis2=dict(title="소비 건수", titlefont=dict(color='#FF7F0E'), overlaying='y', side='right'),
    legend=dict(orientation="h")
)
st.plotly_chart(fig4, use_container_width=True)
st.divider()


# 5. 시간대별 소비 패턴 분석
st.markdown("#### ⏰ 시간대별 소비 패턴 분석")
st.write("시간대별 소비 데이터를 통해 피크 타임을 식별하고, 특정 시간대에 맞춘 서비스를 제공하거나 할인 이벤트를 계획할 수 있습니다.")
hourly_data = filtered_df.groupby("hour")[["amt", "cnt"]].sum().reset_index()
fig5 = go.Figure()
fig5.add_trace(go.Bar(
    x=hourly_data['hour'], y=hourly_data['amt'],
    name='소비 금액', marker_color='#008080'
))
fig5.add_trace(go.Scatter(
    x=hourly_data['hour'], y=hourly_data['cnt'],
    name='소비 건수', mode='lines+markers', marker_color='#F4A261', yaxis='y2'
))
fig5.update_layout(
    title="시간대별 소비 금액 및 건수",
    xaxis=dict(title="시간대"),
    yaxis=dict(title="소비 금액", titlefont=dict(color='#008080')),
    yaxis2=dict(title="소비 건수", titlefont=dict(color='#F4A261'), overlaying='y', side='right'),
    legend=dict(orientation="h"),
    bargap=0.2
)
st.plotly_chart(fig5, use_container_width=True)