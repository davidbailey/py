import pandas
import psycopg2
import sqlite3
from matplotlib import pyplot
from scipy.stats.kde import gaussian_kde
import rpy2.robjects as robjects
import numpy
import scipy.stats as stats
import statsmodels.api as sm
from math import sqrt
import datetime

from os import system
system('ls')
system('pwd')

df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/route19march07.csv")

pyplot.scatter(df.stop_time,df.est_load)
pyplot.scatter(df.index,df.est_load)
df.service_day.value_counts(sort=True,ascending=True).plot(kind='bar')
pyplot.scatter(df.x_coord,df.y_coord)

pyplot.show()

df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/wimaug10_14.csv")
df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/wimaug8.csv")

df[(df['type'] == 11) & (df['timestamp'] >= '2009-08-08') & (df['timestamp'] <= '2009-08-09')]
dataToExplore = df[(df['type'] == 11) & (df['timestamp'] >= '2009-08-08') & (df['timestamp'] <= '2009-08-09')]['spc2']
dataToExplore.mean()
dataToExplore.median()
dataToExplore.mode()
dataToExplore.std()
dataToExplore.var()
dataToExplore.skew()
dataToExplore.kurtosis()
dataToExplore.value_counts()
dataToExplore.describe()
pyplot.boxplot(dataToExplore)

df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/incidents.csv")
pyplot.scatter(df['Unnamed: 0'],df['incidenttypeid'])
df['incidenttypeid'].value_counts

for i in df:
 try:
  pyplot.close()
  pyplot.scatter(df['Unnamed: 0'],df[i])
  pyplot.savefig('figure-' + i + '.png')
 except:
  pass

df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/wimaug8.csv")

df['axl1'].value_counts()

x = numpy.linspace(0,20,1000)
pyplot.plot(x,gaussian_kde(df['axl1'])(x))
pyplot.hist(df['axl1'],normed=1,alpha=.3)

rvector = robjects.IntVector(np.array(df['axl1']))
rhist = robjects.r['hist']
r.X11()
rhist = robjects.r['hist']

x = numpy.arange(-10, 10, .01)
rv1 = stats.norm(loc = 0., scale = 2.0)
rv2 = stats.norm(loc = 1., scale = 2.0)
rv3 = stats.norm(loc = 1., scale = 1.0)
rv4 = stats.norm(loc = 0., scale = 1.0)
pyplot.plot(x,rv1.pdf(x))
pyplot.plot(x,rv2.pdf(x))
pyplot.plot(x,rv3.pdf(x))
pyplot.plot(x,rv4.pdf(x))
pyplot.plot(x,rv1.cdf(x))

qqdata = numpy.random.normal(0,1, 1000)
sm.qqplot(qqdata, line='s')

b = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/bicycle.csv")
set1 = pandas.Series(b[(b['grade'] == 0)]['avgspeed'].tolist())
set2 = pandas.Series(b[(b['grade'] == 1)]['avgspeed'].tolist())

summary = []
for set in [set1,set2]:
 summary.append((set.mean(),set.var(),set.std(),set.skew(),set.kurtosis()))

summaryDF = pandas.DataFrame(summary,index=['Grade','No Grade'],columns=['mean','var','std','skew','kurtosis'])

x = numpy.linspace(0,10,1000)
for (set, color) in zip([set1,set2],['red','blue']):
 pyplot.plot(x,stats.gaussian_kde(set)(x),color=color)
 pyplot.axvline(x=set.mean(),dashes=[10,10],color=color)

for (set, color) in zip([set1,set2],['red','blue']):
 ecdf = sm.distributions.ECDF(set)
 pyplot.plot(ecdf.x,ecdf.y,color=color)

pyplot.boxplot([set1,set2])

sm.qqplot(set1, line='s')
sm.qqplot(set2, line='s')

stat = stats.norm.ppf(.8)
error1 = stat*set1.std()/sqrt(len(set1))
error2 = stat*set2.std()/sqrt(len(set2))

pyplot.scatter(1,set1.mean(),color='blue')
pyplot.scatter(1,set1.mean()+error1,marker='2',color='blue',s=100)
pyplot.scatter(1,set1.mean()-error1,marker='1',color='blue',s=100)
pyplot.axhline(y=set1.mean()-error1,dashes=[10,10],color='blue')
pyplot.scatter(2,set2.mean(),color='red')
pyplot.scatter(2,set2.mean()+error2,marker='2',color='red',s=100)
pyplot.scatter(2,set2.mean()-error2,marker='1',color='red',s=100)
pyplot.axhline(y=set2.mean()+error2,dashes=[10,10],color='red')

stats.ttest_ind(set1,set2)
stats.ttest_ind(set1,set2,equal_var=False)

df = pandas.read_csv("http://web.cecs.pdx.edu/~monserec/t.data/resources/data/incidents.csv")
df['dur'] = df['duration'].map(lambda x: datetime.datetime.strptime(x, '%H:%M:%S')-datetime.datetime(1900,1,1))

nolane = df[(df['numlanesaffected'] == 0)]
onelane = df[(df['numlanesaffected'] == 1)]
twolane = df[(df['numlanesaffected'] == 2)]
morelane = df[(df['numlanesaffected'] >= 3)]

pyplot.boxplot([(nolane['dur']  / numpy.timedelta64(1, 's')).tolist(),(onelane['dur']  / numpy.timedelta64(1, 's')).tolist(),(twolane['dur']  / numpy.timedelta64(1, 's')).tolist(),(morelane['dur']  / numpy.timedelta64(1, 's')).tolist()])

stats.ttest_ind(nolane['dur']  / numpy.timedelta64(1, 's'),onelane['dur']  / numpy.timedelta64(1, 's'))
stats.ttest_ind(nolane['dur']  / numpy.timedelta64(1, 's'),twolane['dur']  / numpy.timedelta64(1, 's'))
stats.ttest_ind(nolane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))
stats.ttest_ind(onelane['dur']  / numpy.timedelta64(1, 's'),twolane['dur']  / numpy.timedelta64(1, 's'))
stats.ttest_ind(onelane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))
stats.ttest_ind(twolane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))

stats.f_oneway(nolane['dur']  / numpy.timedelta64(1, 's'),onelane['dur']  / numpy.timedelta64(1, 's'))
stats.f_oneway(nolane['dur']  / numpy.timedelta64(1, 's'),twolane['dur']  / numpy.timedelta64(1, 's'))
stats.f_oneway(nolane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))
stats.f_oneway(onelane['dur']  / numpy.timedelta64(1, 's'),twolane['dur']  / numpy.timedelta64(1, 's'))
stats.f_oneway(onelane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))
stats.f_oneway(twolane['dur']  / numpy.timedelta64(1, 's'),morelane['dur']  / numpy.timedelta64(1, 's'))

# big difference between 0 and 1 or 2 lanes affected. not a big differnece between 1,2,3+ lanes affected
