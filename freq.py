import pandas as pd
import matplotlib.pyplot as plt
freq = pd.read_csv('frequency.csv', sep=',')
freq['count'].plot()
plt.show()
