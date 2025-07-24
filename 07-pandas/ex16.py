from plotly import graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# Pie Chart의 여러 옵션 및 subplots 활용 예제

countries = ["US", "China", "European Union", "Russian Federation", "Brazil", "India", "Rest of World"]
ghg = [16, 15, 12, 6, 5, 4, 42] 
co2 = [27, 11, 25, 8, 1, 3, 25]

fig = make_subplots(rows=1,cols=2, 
                    specs=[[{'type':'domain'},{'type':'domain'}]]) # 1x2형식의 subplot 생성
fig.add_trace(go.Pie(labels=countries,
                    values=ghg,
                    name="GHG Emissions"),
             # 1행 1열에 위치
             row=1,col=1)

fig.add_trace(go.Pie(labels=countries,
                    values=co2,
                    name="CO2 Emissions"),
             # 1행 2열에 위치
             row=1,col=2)

# hole은 파이차트 가운데 구멍의 크기를 설정
# hoverinfo는 마우스 커서를 갖다 댔을때 띄워질 정보 설정
fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="Global Emissions 1990-2011", # 타이틀 설정
    # annotations은 주석에 대한 정보를 딕셔너리형태로 표현하고 리스트에 넣어서 전달 받음.
    # showarrow가 True면 해당좌표를 화살표로 가리킴.
    annotations=[dict(text='GHG',x=0.19, y=0.5, font_size=20, showarrow=False),
                 dict(text='CO2',x=0.8, y=0.5, font_size=20, showarrow=False)])

fig.show()