import pandas
from scipy import optimize
from sklearn import linear_model
from math import exp, factorial
from scipy.stats import poisson
from statsmodels.api import OLS
from statsmodels.discrete.discrete_model import Poisson
from statsmodels.tools import add_constant

df = pandas.read_csv('datasetRegressionExample.csv')
exposure = lambda row: row['AADT'] * row['L'] * 365
crash_rate = lambda row: row['Crashes'] / row['exposure'] * 1000000

yes_shoulder = df[df['shoulder'] == 1].sum()
no_shoulder = df[df['shoulder'] == 0].sum()

# df = df.append(yes_shoulder, ignore_index=True)
# df = df.append(no_shoulder, ignore_index=True)

df['exposure'] = df.apply(exposure, axis=1)
df['crash_rate'] = df.apply(crash_rate, axis=1)

def estimator(x, row_in='Crashes'):
  estimated = lambda row: x[0] + x[1] * row['AADT'] + x[2] * row['L']
  df['estimated'] = df.apply(estimated, axis=1)
  difference = lambda row: row[row_in] - row['estimated']
  df['difference'] = df.apply(difference, axis=1)
  square = lambda row: row**2
  sum_of_squares = df['difference'].apply(square).sum()
  return(sum_of_squares)

x0 = [-20, .0008, 1.1]
estimator(x0)
optimize.minimize(estimator, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})

clf = linear_model.LinearRegression()
x = df[['AADT', 'L']].as_matrix()
y = df['Crashes']
clf.fit(x, y)
clf.coef_
clf.intercept_

model = OLS(y, add_constant(x))
model_fit = model.fit()
model_fit.summary()

def estimator(x, row_in='Crashes'):
  estimated = lambda row: exp(x[0] + x[1] * row['AADT'] + x[2] * row['L'])
  df['estimated'] = df.apply(estimated, axis=1)
  #probability = lambda row: (row['estimated']**row[row_in] * exp(-row['estimated'])) / factorial(row[row_in])
  probability = lambda row: poisson.pmf(row[row_in], row['estimated'])
  df['probability'] = df.apply(probability, axis=1)
  product = df['probability'].product()
  return(-product)

x0 = [1.6, .0000026, .032]
estimator(x0)
optimize.minimize(estimator, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})

model = Poisson(y.as_matrix().transpose(), add_constant(x))
model_fit = model.fit(start_params=x0)
model_fit.summary()
