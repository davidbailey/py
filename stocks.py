import datetime
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from pandas.io.data import DataReader

stock = DataReader("IVV", "yahoo", start=datetime.datetime(1950, 1, 1))   

regression = sm.OLS(stock['Adj Close'], sm.add_constant(range(len(stock.index)), prepend=True)).fit()
stock['regression'] = regression.fittedvalues
m = regression.params.x1
b = regression.params.const

def y(x,m,b):
 return m*x+b

yv = np.vectorize(y)

def v(x):
 return (stock['Adj Close'][x]-stock['Adj Close'][x-1])/stock['Adj Close'][x-1]

delta = []
for x in range(1, len(stock.index)): delta.append(v(x))

plt.plot(stock.index, stock['Adj Close'], 'b-', stock.index, stock['regression'], 'r-', stock.index, yv(range(len(stock.index)),np.array(delta).mean()*100,65.54), 'g-')

plt.show()


np.random.normal(size=200)

value=65.54
values=[]
for x in range(0,2000):
 value = value + np.array(delta).mean() * 100 * np.random.normal() + np.random.normal()
 values.append(value)

plt.plot(range(0,2000),values)
plt.show()

plt.plot(stats.binom.cdf(range(0,20),50,.2))

x = numpy.arange(-10, 10, .01)
from scipy.stats import norm
rv1 = norm(loc = 0., scale = 2.0)
plt.plot(x,rv1.pdf(x))
plt.plot(numpy.fft.fft(rv1.pdf(x)))
a = [0,1,1,0]
plt.plot(numpy.convolve(a,rv1.pdf(x)))

import math
def g(t): return math.exp(-t**2/2)


