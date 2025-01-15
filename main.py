import streamlit as st
import pandas as pd
import FinanceDataReader as fdr # 삼성전자 -> 종목코드를 알려주지 않음. 
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO # 바이너리파일들을 읽고 쓸 때 사용하는 패키지
import plotly.graph_objects as go
import pandas as pd




test_input = st.text_input("텍스트를 입력하세요")

st.text(test_input)

