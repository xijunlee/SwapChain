import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

font = {'family' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)

df = pd.read_csv('conv6.csv')

iter = df['iter'].values[:100]
y_stack = np.row_stack((df['ga'].values,df['eda'].values,df['tabu'].values))

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(iter, y_stack[0,:100], label='GA', color='xkcd:violet', marker='o')
ax1.plot(iter, y_stack[1,:100], label='EDA', color='xkcd:grey', marker='d')
#ax1.plot(iter, y_stack[2,:50], label='TS', color='r', marker='o')


#plt.xticks(iter, rotation=45)
plt.xlabel('Iteration numbers')
plt.ylabel('Cost')
handles, labels = ax1.get_legend_handles_labels()
lgd = ax1.legend(handles, labels, loc='upper right')

plt.tight_layout()
plt.show()

