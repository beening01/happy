import pandas as pd
import numpy as np
from pathlib import Path
import os


# -----------------------------
# 1. 데이터 로드
# -----------------------------
def load_data(file_name):
    WORK_DIR = Path(__file__).resolve().parent.parent
    IN_DIR = WORK_DIR / "data"
    file_path = IN_DIR / file_name
    # 확장자 추출
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif ext == '.csv':
        df = pd.read_csv(file_path, index_col=0)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다: " + ext)
    
    return df

# str -> float
def safe_to_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return val  # 숫자로 바꿀 수 없으면 원래 값 그대로

# 최초 데이터 -> 지역 데이터 추출
def extract_region_data(df):
    df.columns = [f"{a[:4]}_{b}" for a, b in zip(df.columns,  df.iloc[1])]
    df.drop('구분별(_구분별(1)', axis=1, inplace=True)
    df.rename(columns={"구분별(_구분별(2)": "구분"}, inplace=True)


    # 데이터프레임에서 지역명이 '--구'로 끝나는 행만 추출
    df_loc = df[df["구분"].str.endswith("구", na=False)]
    # 구분 열을 인덱스로 설정 (자치구 이름)
    df_loc.set_index('구분', inplace=True)

    df_loc = df_loc.applymap(safe_to_float)

    return df_loc

# 지역별 데이터 -> 총 평균 데이터
# 추출한 기간의 조건별로 평균을 구하는 함수
def group_and_average_by_conditions(df_loc, years):
    # 사용할 연도
    # years = [str(y) for y in range(2020, 2025)]

    # 원하는 항목만 추출하기 위한 키워드
    cols = ['소계', '자신의 건강상태', '자신의 재정상태',
             '주위 친지 친구와의 관계', '가정생활', '사회생활']

    districts = list(df_loc.index)


    df_mean = pd.DataFrame(index=df_loc.index, columns=cols)
    df_mean = df_mean.fillna(0)

    for dist in districts:
        cs = df_loc.loc[dist].index
        for col in cols:
            for c in cs:
                if col in c:
                    df_mean.loc[dist, col] += df_loc.loc[dist, c]

    df_mean = df_mean / len(years)
    return df_mean
