import os
import pandas as pd
import torch
import streamlit as st
from transformers import AutoTokenizer
import sys
from io import StringIO


def predict_model():
    uploaded_file = st.file_uploader('데이터셋 파일을 업로드하세요', type=['csv'])

    if uploaded_file is not None:
    # 업로드된 파일을 데이터프레임으로 읽기
        data= uploaded_file.read().decode('euc-kr')
        data2 = pd.read_csv(StringIO(data))

    # 데이터셋 확인
    st.subheader('데이터셋 확인')
    st.write(data2)