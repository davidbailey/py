import pandas
from matplotlib import pyplot
df = pandas.DataFrame([431,106])
df = df.transpose()
df.columns=['complete','incomplete']
df.plot(kind='bar', stacked=True, legend=False)
pyplot.show()
