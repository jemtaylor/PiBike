#!/usr/bin/python
import random
import math


class Route:

   def GenerateRoute(self,length):
      currentgradient = 0.0
      currentheight = 0.0
      self.route= []
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

         #print (currentheight, currentgradient)

         if random.random()>0.8:
            # change the gradient
            # gradient can only be between -1 and 1
            currentgradient = currentgradient + random.random()*0.1-0.05
            if currentgradient>1.0:
               currentgradient = 1.0
            if currentgradient<-1.0:
               currentgradient = -1.0
      
         position = position + 1


   def GenerateScenery(self,length):
      self.scenery={}

      position = 0

      while position < self.length-1000:
         if random.random()<0.007:
            #put a tree here
            self.scenery[position]="tree"
         else:
            if random.random()<0.0007:
               #put a cafe here
               self.scenery[position]="cafe"
               position = position + 120
            else:
               if random.random()<0.0007:
                  #put a bookshop here
                  self.scenery[position]="bookshop"
                  position = position + 120
               else:
                  if random.random()<0.0007:
                     #put a giftshop here
                     self.scenery[position]="giftshop"
                     position = position + 120

         position = position + 1

      # put the finish line
      self.scenery[length+50]="finish"

      self.scenery[length-900] = "flamerouge"
      self.scenery[length-200] = "crowd"

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

   def __init__(self, len):

      self.length = len
      self.GenerateRoute(len)
      self.GenerateScenery(len)

