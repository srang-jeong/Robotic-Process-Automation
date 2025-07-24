from plotly import graph_objects as go
import plotly.io as pio

# 브라우저 팝업으로 강제 설정
pio.renderers.default = "browser"

# 그룹화와 스택화 예제

branches = ['컴퓨터사이언스공학과', '기계공학과', '전기전자공학과']

fy=[23,17,35]
sy=[20,23,30]
ty=[30,20,15]

# x는 동일하되 y의 값은 다른 3개의 Bar객체 생성
trace1=go.Bar(
    x = branches,
    y = fy,
    name = 'FY')

trace2=go.Bar(
    x = branches,
    y = sy,
    name = 'SY')

trace3=go.Bar(
    x = branches,
    y = ty,
    name = 'TY')

data = [trace1,trace2,trace3]

# 그룹화 된 막대 차트를 표시하려면 레이아웃 개체의 막대 모드 속성을 그룹으로 설정해야함
layout = go.Layout(barmode='group',title='전공 분야')
fig = go.Figure(data=data,layout=layout)
fig.show()

# 스택형 막대 차트를 표시하려면 레이아웃 개체의 막대 모드 속성을 그룹으로 설정해야함
layout=go.Layout(barmode='stack', title='전공 분야')
fig = go.Figure(data=data, layout=layout)
fig.show()