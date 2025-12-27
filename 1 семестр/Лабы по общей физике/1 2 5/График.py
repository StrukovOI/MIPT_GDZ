import numpy as np
import matplotlib.pyplot as plt
ax=plt.gca()
import matplotlib.ticker as ticker

x=[]
y=[]
for i in range(11):
    x.append(float(input()))
for i in range(11):
    y.append(float(input()))

plt.plot(x, y, color='black', marker='o', markersize=2)

plt.grid(True)
plt.xlabel(r'$\frac{t}{I_0}$, $\frac{\text{с}}{\text{кг}\cdot\text{м}^2}$')
plt.ylabel(r'$\ln(\frac{\nu_0}{\nu(t)})$')

ax.xaxis.set_minor_locator(ticker.MultipleLocator(100000)) 
ax.yaxis.set_minor_locator(ticker.MultipleLocator(10000))

plt.show()


0.39107565
0.39107565
0.3151953
0.3151953
0.25098885
0.25098885
0.20195847
0.20195847
0.16576938
0.16576938
0.13541724
0.13541724
0.08988903
0.08988903
0.210218096
0.20943951
0.169244049
0.168676116
0.134092369
0.133684794
0.10758879
0.107404877
0.088495568
0.088246985
0.072428649
0.072428649
0.04747999
0.047720395