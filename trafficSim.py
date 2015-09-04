from math import sqrt

People = []
class Person:
 def __init__(self,route):
  self.arrived = False
  self.travelTime = 0
  self.route = route
  self.currentRouteSegment = self.route.pop()
  self.positionOnCurrentRouteSegment = 0
  self.width = 2
  self.length = 2
 def Walk(self):
  self.travelTime += 1
  if isinstance(self.currentRouteSegment,FourWayStopSignIntersection):
   pass
  elif isinstance(self.currentRouteSegment,FourWaySignalIntersection):
   pass
  elif isinstance(self.currentRouteSegment,RoadSegment):
   self.positionOnCurrentRouteSegment += 3.7
   if self.positionOnCurrentRouteSegment >= self.currentRouteSegment.length: # we reached the end of the segment and are at a signal
    if self.currentRouteSegment.signal.color == 'green': # if green we go
     if self.route: # more routeSegments in our route
      self.routePosition = self.routePosition - self.routeSegment.length
      self.routeSegment = self.route.pop()
     else:
      self.arrived = True
    else: # red/yellow we stop
     self.routePosition = self.routeSegment.length
  elif isinstance(self.currentRouteSegment,Crosswalk):
   pass

class Vehicle:
 def __init__(self,driver):
  self.driver = driver
  self.speed = 0.0
  self.acceleration = 0.0
  self.deacceleraton = 0.0
 def Accelerate():
  self.speed += self.acceleration
 def Deaccelerate():
  self.speed += self.deacceleraton

class Bicycle(Vehicle):
 def __init__(self,driver):
  Vehicle.__init__(self,driver)
  self.width = 3
  self.lenght = 6

class Car(Vehicle):
 def __init__(self,driver):
  Vehicle.__init__(self,driver)

class Carpool(Car):
 def __init__(self,driver):
  Car.__init__(self,driver)

class Bus(Vehicle):
 pass

class Train:
 pass

class Ferry:
 pass

class Point:
 def __init__(self, x, y):
  self.x = x
  self.y = y

Signals = []
class Signal: # red = stop, yellow = stop if able, green = go
 def __init__(self,color,greenTime,redTime,yellowTime):
  Signals.append(self)
  self.color = color
  self.greenTime = greenTime
  self.redTime = redTime
  self.yellowTime = yellowTime
 def countdown(self):
  if self.color == 'red':
   if self.redTime:
    self.redTime -= 1
   else: self.color = 'green'
  elif self.color == 'green':
   if self.greenTime:
    self.greenTime -= 1
   else: self.color = 'yellow'
  elif self.color == 'yellow':
   if self.yellowTime:
    self.yellowTime -= 1
   else: self.color = 'red'

class FourWayStopSign: # this direction stop, then yeild, then go
 def __init__(self):
  pass

class FourWayStopSignIntersection:
 def __init__(self,nRoadSegment,sRoadSegment,eRoadSegment,wRoadSegment):
  self.stopSign = FourWayStopSign()
  self.nRoadSegment = nRoadSegment
  self.sRoadSegment = sRoadSegment
  self.eRoadSegment = eRoadSegment
  self.wRoadSegment = wRoadSegment
  nQueque = False
  sQueque = False
  eQueque = False
  wQueque = False

class TwoWayStopSign: # this direction stop, then yeild, then go
 def __init__(self):
  pass

class YeildSign: # yeild, thens go
 def __init__(self):
  pass

class = Crosswalk: #
 def __init__(self):
  pedestrianPresent = False

class FourWaySignal:
 def __init__(self,majorTime,minorTime,yellowTime):
  self.major = Signal('green',majorTime,minorTime+yellowTime,yellowTime)
  self.minor = Signal('red',minorTime,majorTime+yellowTime,yellowTime)

class FourWaySignalIntersection:
 def __init__(self)
  self.pedestrianSignal1 = FourWaySignal(13,3,12)
  self.trafficSignal = FourWaySignal(20,10,5)
  self.pedestrianSignal2 = FourWaySignal(13,3,12)

class RoadSegment:
 def __init__(self, origin, destination, signal, type):
  self.origin = origin
  self.destination = destination
  self.length = sqrt((self.origin.x+self.destination.x)**2+(self.origin.y+self.destination.y)**2)
  self.signal = signal
  self.type = type

class HalfTwoLaneRoad:
 def __init__(self,end1,end2):
  self.sidewalk1 = RoadSegment(end1,end2,'person')
  self.sidewalk2 = RoadSegment(end2,end1,'person')
  self.lane = RoadSegment(end1,end2,'vehicle')

class TwoLaneRoad:
 def __init__(self,end1,end2):
  self.half1 = HalfTwoLaneRoad(end1,end2)
  self.half2 = HalfTwoLaneRoad(end2,end1)

p1 = Point(0,0)
p2 = Point(10,10)
p3 = Point(20,20)

rs1 = RoadSegment(p1,p2,s1)
rs2 = RoadSegment(p2,p3,s2)

rs3 = RoadSegment(p3,p2,s1)
rs4 = RoadSegment(p2,p1,s2)

P1 = Person([rs2,rs1])
P2 = Person([rs4,rs3])

while P1.arrived == False:
 for S in Signals:
  print S.color
  S.countdown()
 for P in People:
  print str(P.arrived) + " " + str(P.travelTime) + " " + str(P.routeSegment) + " " + str(P.routePosition) + "\n"
  P.Walk()
