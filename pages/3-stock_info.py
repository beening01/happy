# https://hello-yeonji-stock.streamlit.app/

# 표준 라이브러리
import datetime
from io import BytesIO

# 서드파티 라이브러리
import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib 
# import koreanize_matplotlib

# 캐싱: 인자가 바뀌지 않는 함수 실행 결과를 저장 후 재사용
@st.cache_data
def get_krx_company_list() -> pd.DataFrame:
    """
    KRX(한국거래소) 상장 기업의 회사명과 종목코드 정보를 DataFrame으로 반환합니다.

    Returns:
        pd.DataFrame: '회사명', '종목코드' 컬럼을 가진 DataFrame
    """
    krx_df = fdr.StockListing('KRX')
    company_df = krx_df[['Name', 'Code']].rename(columns={'Name': '회사명', 'Code': '종목코드'})
    return company_df


def get_stock_code_by_company(company_name: str) -> str:
    """
    회사명을 입력받아 해당 회사의 종목코드를 반환합니다.
    Args:
        company_name (str): 조회할 회사명
    Returns:
        str: 종목코드. 입력된 회사명이 없으면 ValueError 발생
    """
    company_df = get_krx_company_list()
    codes = company_df[company_df['회사명'] == company_name]['종목코드'].values
    if len(codes) > 0:
        return codes[0]
    else:
        raise ValueError(f"'{company_name}'에 해당하는 종목코드가 없습니다.")


def sidebar_inputs() -> tuple[str, tuple[datetime.date, datetime.date], bool]:
    """
    Streamlit 사이드바에 회사명 입력창, 날짜 선택 위젯, 확인 버튼을 생성하고 입력값을 반환합니다.

    Returns:
        tuple: (회사명(str), (시작일, 종료일)(tuple of date), 확인버튼 클릭여부(bool))
    """
    company_name = st.sidebar.text_input('회사 이름을 입력하세요: ')
    today = datetime.datetime.now()
    this_year = today.year
    jan_1 = datetime.date(this_year, 1, 1)
    selected_dates = st.sidebar.date_input(
        "시작일과 종료일을 입력하세요",
        (jan_1, today),
        None,
        today,
        format="MM.DD.YYYY",
    )
    st.sidebar.write(selected_dates)
    confirm_btn = st.sidebar.button('확인')
    return company_name, selected_dates, confirm_btn

company_name, selected_dates, confirm_btn = sidebar_inputs()

if confirm_btn:

    # 우리가 필요로하는 코드조각들

    stock_code = get_stock_code_by_company(company_name)
    start_date = selected_dates[0].strftime(r"%Y-%m-%d")
    end_date = (selected_dates[1] + datetime.timedelta(days=1)).strftime(r"%Y-%m-%d")
    price_df = fdr.DataReader(f'KRX:{stock_code}', start_date, end_date)

    st.header(f'{company_name}의 현재 주가')

    st.dataframe(price_df)

    fig = go.Figure(data=[go.Candlestick(x=price_df.index,
                            open=price_df['Open'],
                            high=price_df['High'],
                            low=price_df['Low'],
                            close=price_df['Close'])])
    st.plotly_chart(fig)

    excel_data = BytesIO()
    price_df.to_excel(excel_data)
    st.download_button("엑셀 파일 다운로드", excel_data, file_name='stock_data.xlsx')
