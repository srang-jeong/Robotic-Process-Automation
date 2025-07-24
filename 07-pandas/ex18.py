from plotly import graph_objects as go
import numpy as np
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# 일반적인 Histogram 예제

np.random.seed(1)

# 표준 정규분포를 따르는 난수 500개를 ndarray로 반환
x = np.random.randn(500)
data=[go.Histogram(x=x)]

fig=go.Figure(data)
fig.show()

# ndarray : 넘파이(Numpy) 라이브러리에서 지원하는 다차원 배열 객체이다.
# 넘파이를 이용하여 판다스 라이브러리가 작성됨.