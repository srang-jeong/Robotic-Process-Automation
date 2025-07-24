import plotly.graph_objects as go
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# Box plot
# Box Plots은 주로 데이터에서 이상치를 탐지하는데 사용한다.
# q1은 하위 25%를 의미하고 q3는 상위 25%를 의미한다.

yaxis = [1140,1460,489,594,502,508,370,200] 
data = go.Box(y = yaxis) 
fig = go.Figure(data) 
fig.show()