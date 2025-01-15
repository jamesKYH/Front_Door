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

def load_csv_file(file_path):
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.write('에러 발생.',e)
            return None
    else:
        st.write("파일 x.")
        return None


def main():
    st.title("csv 표시")

    file_path = '/Users/james_kyh/Desktop/ITStudy/data_set/카드소비 데이터_202408/tbsh_gyeonggi_day_포천시_202408.csv'
    df = load_csv_file(file_path)
    
    
    if "data" not in st.session_state:
        if df is not None:
            st.session_state["data"] = df
            st.success("데이터 세션에 저장")
        else:
            st.error("데이터 못불러옴.")

    
    
    if df is not None:
        st.write('파일을 불러옴.',df)
        
    else:
        st.write("파일을 불러올 수 없음.")
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()