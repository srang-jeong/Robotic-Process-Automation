from plotly import graph_objects as go
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# 일반적인 Pie Chart 예제

langs = ['C','C++','Java','Python','PHP']
students = [23,17,35,29,12]

data = [go.Pie(
    labels = langs,
    values = students,
    # 각각의 인덱스에 배정된 조각을 원점을 기준으로 얼마나 당길건지 설정
    pull=[0.1,0,0,0,0]
)]

fig = go.Figure(data=data)
fig.show()