import yfinance as yf
import pandas as pd
import sqlite3
import os

def collect_data():
    # 1. 설정 및 자산 정의
    assets = {
        'GC=F': 'Gold',
        'SI=F': 'Silver',
        '^GSPC': 'S&P500'
    }
    start_date = '2015-01-01'
    db_path = os.path.join('gspjt', 'data', 'commodity_analysis.db')
    
    print(f"데이터 수집 시작: {list(assets.keys())} (시작일: {start_date})")
    
    # 2. 데이터 다운로드
    data_list = []
    for ticker, name in assets.items():
        print(f"{name}({ticker}) 다운로드 중...")
        df = yf.download(ticker, start=start_date)
        if df.empty:
            print(f"경고: {ticker} 데이터를 가져오지 못했습니다.")
            continue
        
        # 컬럼 정리 (yfinance 버전에 따라 다를 수 있음)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        columns_to_keep = []
        for col in ['Close', 'Adj Close']:
            if col in df.columns:
                columns_to_keep.append(col)
        
        if not columns_to_keep:
            print(f"경고: {ticker}에서 필요한 컬럼을 찾지 못했습니다. (있는 컬럼: {df.columns.tolist()})")
            continue
            
        df = df[columns_to_keep].copy()
        df['Ticker'] = ticker
        df['Asset'] = name
        df.reset_index(inplace=True)
        data_list.append(df)
    
    if not data_list:
        print("수집된 데이터가 없습니다.")
        return

    # 3. 데이터 통합
    full_df = pd.concat(data_list, axis=0)
    
    # Date를 문자열 포맷으로 변경 (SQLite 저장용)
    full_df['Date'] = full_df['Date'].dt.strftime('%Y-%m-%d')
    
    # 4. SQLite DB 저장
    print(f"DB 저장 중: {db_path}")
    conn = sqlite3.connect(db_path)
    
    # 원본 데이터 저장 (기존 데이터 있을 경우 교체)
    full_df.to_sql('raw_prices', conn, if_exists='replace', index=False)
    
    # 인덱스 생성 (조회 최적화)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date_ticker ON raw_prices (Date, Ticker)")
    
    conn.close()
    print("데이터 수집 및 DB 저장 완료.")

if __name__ == "__main__":
    collect_data()
