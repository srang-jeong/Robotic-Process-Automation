from plotly import graph_objects as go
import plotly.io as pio

# py -m pip install plotly

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# 일반적인 Bar Chart 예제

langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]

# x축과 y축에 해당하는 데이터를 각각 넣고 리스트로 감싸줌
data = [go.Bar(x = langs, y = students)]
# 만들어놓은 데이터 전달
fig = go.Figure(data = data)

# 그래프 출력
fig.show()