#!/usr/bin/python
import random
import math

# v13 - read the route from a GPS file

class Route:

   def GenerateRoute(self,length):
      self.elevation = []
      self.time= []
      self.latitude = []
      self.longitude = []
      position = 0

      fgps = open("richmond30km.gps", "r")    

      while position < length:

         sLine = fgps.readline()

         # format of the GPS file is :
         #sLine = "lat=51.4472320634 lon=-0.339161424671 ele=5.88896350748"

         findLat = sLine.find("lat=")
         findLong = sLine.find("lon=")
         findelev = sLine.find("ele=")

         latitude = sLine[findLat+4:findLong-2]
         longitude = sLine[findLong+4:findelev-2]
         elevation = sLine[findelev+4:len(sLine)-1]

         #print("latitude ", latitude)
         #print("longitude ", longitude)
         #print("elevation ", elevation)
 
         self.elevation.append(int(float(elevation)))
         self.time.append(0)
         self.latitude.append(latitude)
         self.longitude.append(longitude)

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
         return self.elevation[self.length-1]
      else:
         return self.elevation[position]

   def GetLength(self):
      return self.length

   def GetScenery(self,position):
      if position in self.scenery:
         return self.scenery[position]
      else:
         return ""

   def GetTime(self, position):
      return self.time[position]

   def GetLatitude(self, position):
      if position>=self.length:
         return self.latitude[self.length-1]
      else:
         return self.latitude[position]

   def GetLongitude(self, position):
      if position>=self.length:
         return self.longitude[self.length-1]
      else:
         return self.longitude[position]

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

