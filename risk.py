import numpy as np
//from pylab import *
import matplotlib.pyplot as plot
import math

top = np.array([[0,1,2],[2,2,1]])
mid = np.array([[0,1,2],[2,1,0]])
bot = np.array([[0,1,2],[2,0,0]])

plot.plot(top[0],top[1])
plot.plot(mid[0],mid[1])
plot.plot(bot[0],bot[1])

t = np.arange(0.0, 10.0, 0.1)
top2 = 10-np.arange(0.0, 1.0, 0.01)
top = 10-(.3*t)**2
mid = -t + 10
bot = 10-np.sqrt(t)
bot2 = 1/(t)

plot.plot(t,top2)
plot.plot(t,top)
plot.plot(t,mid)
plot.plot(t,bot)
plot.plot(t,bot2)

plot.scatter(2,6)
plot.scatter(2,5)
plot.scatter(9,1)

plot.xlabel('Cost')
plot.ylabel('Risk')
plot.title('Risk vs. Cost')
plot.grid(True)
plot.show()


\\Risk = Money * Time
\\ Time = constant * Money
\\ Outsource Time = constant1 * Time + constant2 * Money
