import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [5, 4, 3, 2, 1]
plt.plot(x, y)
plt.show()



import plotly.graph_objects as go

source = [0, 0]
target = [1, 2]
value =  [3, 1]

link = {'source': source, 'target': target, 'value': value}

sk = go.Sankey(link=link)
fig = go.Figure(sk)
fig.show()