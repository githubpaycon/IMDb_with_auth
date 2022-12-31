from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from src.base.base import *

import pandas as pd
from io import BytesIO
import streamlit as st

def to_excel(df):
    if df.empty:
        return False
    else:
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data


rank_col = []
nome_filme_col = []
ano_col = []
imdb_rating_col = []


@st.cache
def faz_dataframe():
    df = pd.DataFrame({
        'RANK': rank_col,
        'NOME DO FILME': nome_filme_col,
        'ANO': ano_col,
        'IMDB RATING': imdb_rating_col,
    })
    return df
