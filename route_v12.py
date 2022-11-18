#!/usr/bin/python
import random
import math


class Route:

   def GenerateRoute(self,length):
      currentgradient = 0.0
      currentheight = 0.0
      self.route= []
      self.time= []
      position = 0

      while position < length:
         currentheight = currentheight + currentgradient
         if currentheight>1000:
            currentheight = 1000
            currentgradient = 0.0
         if currentheight<0:
            currentheight=0
            currentgradient = 0.0

         self.route.append(currentheight)
         self.time.append(0)

         #print (currentheight, currentgradient)

         if random.random()>0.8:
            # change the gradient
            # gradient can only be between -5 and 5
            currentgradient = currentgradient + random.random()*6.0-3.0
            if currentgradient>5.0:
               currentgradient = 5.0
            if currentgradient<-5.0:
               currentgradient = -5.0
      
         position = position + 1


   def GenerateScenery(self,length):
      self.scenery={}

      position = 0

      while position < self.length-1000:
         if random.random()<0.3:
            #put a tree here
            self.scenery[position]="tree"
         else:
            if random.random()<0.02:
               #put a cafe here
               self.scenery[position]="cafe"
               position = position + 120
            else:
               if random.random()<0.03:
                  #put a bookshop here
                  self.scenery[position]="bookshop"
                  position = position + 120
               else:
                  if random.random()<0.03:
                     #put a giftshop here
                     self.scenery[position]="giftshop"
                     position = position + 120

         position = position + 1

      # put the finish line
      self.scenery[length]="finish"

      self.scenery[length-1000] = "flamerouge"
      self.scenery[length-50] = "50m"
      self.scenery[length-100] = "100m"
      self.scenery[length-250] = "250m"
      self.scenery[length-500] = "500m"
      self.scenery[length-12] = "crowd"

   def GetHeight(self,position):

      if position>=self.length:
         return self.route[self.length-1]
      else:
         return self.route[position]

   def GetLength(self):
      return self.length

   def GetScenery(self,position):
      if position in self.scenery:
         return self.scenery[position]
      else:
         return ""

   def GetTime(self, position):
      return self.time[position]

   def SetTime(self, position, time):
      # record the leader's time in all positions back to the last recorded leader time
      # this will ensure that all positions up to the leader are populated with the time the leader passed that spot
      pos=int(position*1000)

      if pos<self.length:
         while (self.time[pos]==0 and pos>0):
            self.time[pos]=time
            pos=pos-1


   def __init__(self, len):

      self.length = len
      self.GenerateRoute(len)
      self.GenerateScenery(len)

