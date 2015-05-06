import math
import csv
import numpy
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.fftpack
import datetime
import pandas as pd
from scipy import stats

def pv(fv,r):
 return (fv/(1+r))

def pvSum(c,r): //PV as a sum of cash flows c w/ interest rate 
 sum=0
 for n, ck in enumerate(c):
  print n,ck,r
  sum += ck/((1+r)**n)
 return sum

def annuity(A,r): //Annuity pays A forever
 return A/r

def annuityEnd(A,r,n)Annuity that pays A until n
 return annuity(A,r)*(1-1/((1+r)**n)) 

def discountRate(spotRate,t): 
 return 1/((1+spotRate)**t)

def fv(pv,r):
 return (pv*(1+r))

def p(f,i,n):
 return (f/((1+i)**n))
vec_p = np.vectorize(p)
ptest = np.array([np.array([ 1.,  2.,  3.]), np.array(10), np.array(10)])
vec_p(ptest[0],ptest[1],ptest[2])

def f(p,i,n):
 return (p*((1+i)**n))

def fe(p,i,n):
 return (p*(math.e**(i*n)))

def pe(f,i,n):
 return (f/(math.e**(i*n)))

cpiv = []
cpid = []
with open('CPIAUCSL.csv', 'rb') as cpifile:
 cpi = csv.reader(cpifile)
 for row in cpi:
  cpiv.append(row[1])
  cpid.append(row[0])

cpiv.pop(0)
cpid.pop(0)

cpidd = []
for item in cpid:
 cpidd.append(mpl.dates.date2num(datetime.datetime.strptime(item, "%Y-%m-%d")))

plt.plot_date(x=cpidd,y=cpiv)
plt.show()

c = []
b = 0
for a in cpiv:
  if b: c.append((float(a)-b)/float(a))
  b = float(a)

numpy.mean(c)*12

x = np.poly1d([1,0])

cpif = scipy.fftpack.fft(cpim)

def ERi(Rf,Bi,ERm): //CAPM
 return (Rf+Bi*(ERm-Rf))

df = pd.read_csv('CPIAUCSL.csv')

x = [5.05, 6.75, 3.21, 2.66]
y = [1.65, 26.5, -5.93, 7.96]
gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
t = np.arange([0.0, 10.0, 0.1])
z = gradient*t+intercept
plt.plot(t,z)
plt.scatter(x,y)
plt.show()
