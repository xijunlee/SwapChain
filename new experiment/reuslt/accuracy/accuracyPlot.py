import numpy as na

from matplotlib.pyplot import *

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%.2f' % float(height+3098),
                ha='center', va='bottom')

xlabels = ["LPSolver","EDA", "GA", "TS"]

font = {'family' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)

data =  na.array([3100,3100,3109.11,3113.28])
data = data - 3098
ylocations = na.arange(0,16,2)
ylabels = [str(x) for x in na.arange(3098,3116,2)]
color = ['xkcd:grey', 'xkcd:cyan', 'xkcd:violet', 'xkcd:orange']

xlocations = na.array(range(len(data)))+1
width = 0.4
#bar(xlocations, data, width=width, color = color)
#yticks(ylocations,ylabel)
#xticks(xlocations, xlabels)
#xlim(0, xlocations[-1]+width*2)
fig, ax = subplots()
rects = ax.bar(xlocations, data, width, color=color)
ax.set_ylabel('Cost')
ax.set_xlabel('Algorithm')
ax.set_xticks(xlocations)
ax.set_xticklabels(xlabels)
ax.set_yticklabels(ylabels)

autolabel(rects)

tight_layout()
show()