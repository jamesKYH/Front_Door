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


@st.cache_data
def load_csv_file(file_path):
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.write('에러가 발생했습니다.',e)
            return None
    else:
        st.write("파일이 존재하지 않습니다.")
        return None


def main():
    st.title("csv 표시")

    file_path = '/Users/james_kyh/Desktop/ITStudy/data_set/카드소비 데이터_202408/tbsh_gyeonggi_day_포천시_202408.csv'
    df = load_csv_file(file_path)

    if df is not None:
        st.write(df)
    else:
        st.write("파일을 불러올 수 없습니다.")
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()