import numpy as np
import matplotlib.pyplot as plt
ax=plt.gca()
import matplotlib.ticker as ticker

x=[]
y=[]
for i in range(17):
    x.append(float(input())*100)
for i in range(17):
    y.append(float(input()))

plt.plot(x, y, color='black', marker='o', markersize=2)

plt.grid(True)
plt.xlabel('x, мм\u00B2')
plt.ylabel('I, кг*м\u00B2*10\u00B3')

ax.xaxis.set_minor_locator(ticker.MultipleLocator(200)) 
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

plt.show()