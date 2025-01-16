import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import get_combined_sampled_data  # 메인 코드에서 함수 가져오기

st.set_page_config(page_title="대분류 관련 그래프 출력", layout="wide")



st.title("어떤 분야가 좋을까?")
#페이지 설정

st.title(":막대_차트: 업종대분류 관련 정보")
st.markdown("이 페이지에서는 업종대분류에 관련된 다양한 내용을 제공합니다.")
# 캐시된 데이터 가져오기
sampled_df = get_combined_sampled_data()
if not sampled_df.empty:
    st.write("샘플링된 데이터 미리보기:")
    st.dataframe(sampled_df)
else:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()
df = sampled_df


# 'ta_ymd' 열에서 월(month) 정보 추출
df['month'] = pd.to_datetime(df['ta_ymd'], format='%Y%m%d').dt.month
# 업종대분류 목록 추출 및 선택
unique_main_categories = df["card_tpbuz_nm_1"].dropna().unique()
selected_category = st.selectbox("관심 있는 업종 대분류를 선택하세요:", sorted(unique_main_categories))
# 선택한 업종 대분류로 데이터 필터링
filtered_df = df[df["card_tpbuz_nm_1"] == selected_category]
st.subheader(f"선택한 업종: {selected_category}")
if not filtered_df.empty:
    # 1. 월별 총 매출 금액 추이 ->성수기,비수기 파악 ,시간 순서대로 연결되어 상승,하락 쉽게 식별 가능
    monthly_sales = filtered_df.groupby("month")["amt"].sum().reset_index()
    line_fig = px.line(
        monthly_sales,
        x="month",
        y="amt",
        title="월별 총 매출 금액 추이",
        labels={"month": "월", "amt": "매출 금액"},
        markers=True
    )
    st.plotly_chart(line_fig, use_container_width=True)
    # 2. 성별 매출 비율 ->남성과 여성 소비비율 한번에 보여줌
    gender_sales = filtered_df.groupby("sex")["amt"].sum().reset_index()
    pie_fig = px.pie(
        gender_sales,
        values="amt",
        names="sex",
        title="성별 매출 비율",
        color_discrete_map={'M': 'blue', 'F': 'pink'},
        category_orders={"sex": ["M", "F"]}  # 색상 순서를 강제
    )
    st.plotly_chart(pie_fig, use_container_width=True)
   # 3. 성별 및 연령대별 매출 집계 ->연령대별 성별에 따라 소비패턴 파악
    sales_by_gender_age = filtered_df.groupby(['sex', 'age']).agg({'amt': 'sum'}).reset_index()
    # 그래프 생성
    fig = px.bar(
        sales_by_gender_age,
        x='age',
        y='amt',
        color='sex',
        barmode='group',  # 그룹형 막대그래프
        labels={'amt': '매출 금액', 'age': '연령대', 'sex': '성별'},
        title='성별 & 연령대별 매출 비교',
        color_discrete_map={'M': 'lightblue', 'F': 'lightpink'}  # 성별 색상 지정
    )
    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    # 4. 요일별 매출 및 소비 건수 집계 -> 서로 다른 두개의 데이터 비교
    weekday_data = (
        filtered_df.groupby("day")
        .agg(total_amount=("amt", "sum"), total_count=("cnt", "sum"))
        .reset_index()
    )
    # 요일 매핑
    day_labels = {
        '01': '월', '02': '화', '03': '수', '04': '목', '05': '금', '06': '토', '07': '일',
        1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토', 7: '일',  # 숫자형 매핑
        '1': '월', '2': '화', '3': '수', '4': '목', '5': '금', '6': '토', '7': '일'  # 문자열 숫자형 매핑
    }
    weekday_data["day_name"] = weekday_data["day"].map(day_labels)
    # 이중 Y축 그래프 생성
    fig = go.Figure()
    #
    # 소비 금액 (첫 번째 Y축)
    fig.add_trace(
        go.Scatter(
            x=weekday_data['day_name'],
            y=weekday_data['total_amount'],
            mode='lines+markers',
            name='소비 금액',
            line=dict(color='#1F77B4'),
            marker=dict(size=8),
            yaxis='y1'
        )
    )
    # 소비 건수 (두 번째 Y축)
    fig.add_trace(
        go.Scatter(
            x=weekday_data['day_name'],
            y=weekday_data['total_count'],
            mode='lines+markers',
            name='소비 건수',
            line=dict(color='#FF7F0E'),
            marker=dict(size=8),
            yaxis='y2'
        )
    )
    # 레이아웃 설정
    fig.update_layout(
        title="요일별 소비 패턴 분석",
        xaxis=dict(title="요일"),
        yaxis=dict(
            title="소비 금액",
            titlefont=dict(color='#1F77B4'),
            tickfont=dict(color='#1F77B4')
        ),
        yaxis2=dict(
            title="소비 건수",
            titlefont=dict(color='#FF7F0E'),
            tickfont=dict(color='#FF7F0E'),
            overlaying='y',
            side='right'
        ),
        legend=dict(title="항목", x=0.8, y=1.2),
        template="plotly_white"
    )
    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    # 5. 시간대별 데이터 집계 (선과 막대) -> 서로 다른 두가지 데이터 비교
    hourly_data = (
        filtered_df.groupby("hour")[["amt", "cnt"]]
        .sum()
        .reset_index()
        .rename(columns={"amt": "total_amount", "cnt": "total_count"})
    )
    # 그래프 생성
    fig = go.Figure()
    # 소비 금액 (막대 그래프)
    fig.add_trace(
        go.Bar(
            x=hourly_data['hour'],
            y=hourly_data['total_amount'],
            name='소비 금액',
            marker_color='#008080',
            yaxis='y1'
        )
    )
    # 소비 건수 (라인 그래프)
    fig.add_trace(
        go.Scatter(
            x=hourly_data['hour'],
            y=hourly_data['total_count'],
            name='소비 건수',
            marker_color='#F4A261',
            yaxis='y2',
            mode='lines+markers'
        )
    )
    # 레이아웃 설정
    fig.update_layout(
        title="시간대별 소비 패턴 분석",
        xaxis=dict(title="시간대"),
        yaxis=dict(
            title="소비 금액",
            titlefont=dict(color='#008080'),
            tickfont=dict(color='#008080'),
        ),
        yaxis2=dict(
            title="소비 건수",
            titlefont=dict(color='#F4A261'),
            tickfont=dict(color='#F4A261'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.1, y=1.1, orientation="h"),
        bargap=0.2,
        template="plotly_white"
    )
    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("선택한 업종 대분류에 해당하는 데이터가 없습니다.")