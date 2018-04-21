import pandas as pd
import numpy as np
from bokeh.io import output_notebook
from bokeh.plotting import figure,show
from bokeh.layouts import column



def datatukuri(po_m = 9699, idx = 'tpf'):
    
    '''
    PO銘柄の価格データとインデックスの価格データを作る。
    '''
    
    # まずはPOデータベースの読み込み
    data = pd.read_excel('filename.xlsx', index_col='anounce-date')
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    
    # 次にPO銘柄の価格データを作成
    po_meigara = pd.read_csv('{}.csv'.format(po_m), index_col='日付', encoding='ANSI', thousands=',')
    po_meigara.index = pd.to_datetime(po_meigara.index)
    po_meigara = po_meigara.sort_index()
    po_meigara1 = po_meigara.iloc[:, :4]
    
    a = data.loc[data['CODE']==po_m]  # POデータベースからPO銘柄のデータを読み込む
    anounce_date = a.index[0]   # その銘柄のPO発表日
    deli_date = a['deli-day'][0]  # PO株の受け渡し日
    
    po_meigara2 = po_meigara1[anounce_date: deli_date]
    po_meigara3 = po_meigara2 / po_meigara2.iloc[1, 0] * 100  # PO銘柄データ完成
    
    # 次にインデックス
    
    market = pd.read_csv('{}.csv'.format(idx),index_col='日付',thousands=',', encoding='ANSI')
    market.index =  pd.to_datetime(market.index)
    market = market.sort_index()
    market1 = market.iloc[:, :4]
    market2 = market1[anounce_date: deli_date]
    market3 = market2 / market2.iloc[1, 0] * 100  # インデックスのデータ完成
    
    return po_meigara3, market3


def po_bunseki(po_Meigara='a', market='b'):
    
    '''
    PO銘柄ショート、インデックスロングのパフォーマンスを作る。
    入力データ、PO銘柄の四本値、インデックスの四本値
    '''
    
    performance =  market['終値'] - po_Meigara['終値']
    performance1 = performance.copy()
    performance1.index = [i for i in(range(-1, len(performance) - 1))]
    
    return performance, performance1

def chart_date(po_Meigara='a', market='b', spread='c', name='d'):
    '''
    日付ベースのPO銘柄のパフォーマンス、指数のパフォーマンス、
    そのロングショートのスプレッドの動きを示すグラフを作る。
    '''
    p = figure(width=700, height=300, x_axis_type='datetime', title='PO銘柄（緑）と指数（青）')
    p1 = figure(width=700, height = 200, x_axis_type='datetime', title='スプレッド')
    
    p.line(po_Meigara.index, po_Meigara['終値'], line_color='green', line_width=3)
    p.line(market.index, market['終値'], line_color='blue', line_width=3)
    
    p1.line(spread.index, spread, line_color='red', line_width=3)
    
    show(column(p, p1))
