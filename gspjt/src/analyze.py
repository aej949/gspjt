import pandas as pd
import sqlite3
import numpy as np
import os

def calculate_mdd(series):
    """최대 낙폭(MDD) 계산용 함수"""
    roll_max = series.cummax()
    daily_drawdown = series / roll_max - 1.0
    return daily_drawdown.min()

def analyze_crisis():
    db_path = os.path.join('gspjt', 'data', 'commodity_analysis.db')
    conn = sqlite3.connect(db_path)
    
    # 1. 데이터 로드
    df = pd.read_sql("SELECT * FROM raw_prices", conn)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(['Ticker', 'Date'], inplace=True)
    
    # 2. 위기 기간 정의
    crises = {
        'Brexit': ('2016-06-01', '2016-08-31'),
        'Tariff War': ('2018-03-01', '2019-12-31'),
        'Iran-US Conflict': ('2020-01-01', '2020-02-29'),
        'COVID-19': ('2020-03-01', '2020-12-31'),
        'Russia-Ukraine War': ('2022-02-01', '2022-06-30')
    }
    
    # 3. 일일 수익률 계산 (전체 기간)
    df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change()
    
    performance_results = []
    
    # 4. 위기별 분석
    for crisis_name, (start, end) in crises.items():
        print(f"위기 분석 중: {crisis_name} ({start} ~ {end})")
        
        # 해당 기간 필터링
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        crisis_df = df.loc[mask].copy()
        
        if crisis_df.empty:
            continue
            
        tickers = crisis_df['Ticker'].unique()
        
        for ticker in tickers:
            asset_data = crisis_df[crisis_df['Ticker'] == ticker].sort_values('Date')
            asset_name = asset_data['Asset'].iloc[0]
            
            if len(asset_data) < 2:
                continue
                
            # 지표 계산
            # 누적 수익률
            first_price = asset_data['Close'].iloc[0]
            last_price = asset_data['Close'].iloc[-1]
            cum_return = (last_price / first_price) - 1
            
            # MDD
            mdd = calculate_mdd(asset_data['Close'])
            
            # 변동성 (연화)
            volatility = asset_data['Daily_Return'].std() * np.sqrt(252)
            
            # 샤프 지수 (무위험 수익률 0 가정)
            avg_return = asset_data['Daily_Return'].mean() * 252
            sharpe_ratio = avg_return / volatility if volatility != 0 else 0
            
            # S&P 500과의 상관관계
            sp500_returns = crisis_df[crisis_df['Ticker'] == '^GSPC'].set_index('Date')['Daily_Return']
            correlation = asset_data.set_index('Date')['Daily_Return'].corr(sp500_returns)
            
            performance_results.append({
                'Crisis': crisis_name,
                'Ticker': ticker,
                'Asset': asset_name,
                'Cumulative_Return': cum_return,
                'MDD': mdd,
                'Volatility': volatility,
                'Sharpe_Ratio': sharpe_ratio,
                'Correlation_SP500': correlation
            })
            
    # 5. DB 저장
    perf_df = pd.DataFrame(performance_results)
    perf_df.to_sql('crisis_performance', conn, if_exists='replace', index=False)
    
    # 6. 추가: 금-은 비율 계산 (전체 기간용)
    gold_prices = df[df['Ticker'] == 'GC=F'][['Date', 'Close']].rename(columns={'Close': 'Gold'})
    silver_prices = df[df['Ticker'] == 'SI=F'][['Date', 'Close']].rename(columns={'Close': 'Silver'})
    
    ratio_df = pd.merge(gold_prices, silver_prices, on='Date')
    ratio_df['Ratio'] = ratio_df['Gold'] / ratio_df['Silver']
    ratio_df.to_sql('gold_silver_ratio', conn, if_exists='replace', index=False)
    
    conn.close()
    print("분석 실 및 결과 DB 저장 완료.")

if __name__ == "__main__":
    analyze_crisis()
