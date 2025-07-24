from plotly import graph_objects as go
import numpy as np
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

N = 100

# 0~1사이안에서 N개의 요소를 동일한 간격으로 나누어 놓은 1차원 넘파이 배열 반환
# 예를 들어 linspace(0,10,11)이면 [0,1,2,...,9,10]를 반환한다는 것
x_vals = np.linspace(0,1,N)

# 데이터 준비
# randn: 표준정규분포를 따르는 난수 발생
y1 = np.random.randn(N)+5
y2 = np.random.randn(N)
y3 = np.random.randn(N)-5

trace1 = go.Scatter(
    x=x_vals,
    y=y1,
    # mode는 데이터 포인트의 모양을 결정
    mode='markers',
    name='markers'
)

trace2 = go.Scatter(
    x=x_vals,
    y=y2,
    mode='lines+markers',
    name='lines+markers'
)

trace3 = go.Scatter(
    x=x_vals,
    y=y3,
    mode='lines',
    name='lines'
)

data=[trace1,trace2,trace3]
fig=go.Figure(data=data)
fig.show()
