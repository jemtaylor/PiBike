#!/usr/bin/python
import random
import math

# v13 - read the route from a GPS file
# v14 - record min and max lat for the map display
# v15 - changes for python3

class Route:

   def GenerateRoute(self,fname):
      self.elevation = []
      self.time= []
      self.latitude = []
      self.longitude = []
      self.maxLat = -90.0
      self.maxLong = -180.0
      self.minLat = 90.0
      self.minLong = 180.0
      self.minElev=9999.9
      self.maxElev=-9999.9

      position = 0

      fullfile = "/home/pi/bike/" + str(fname) + ".gps"
      fgps = open(fullfile, "r")    

      NotFinished = True

      while NotFinished:

         sLine = fgps.readline()

         findLength = sLine.find("RouteLength")
         if (findLength==-1):

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

            fLat = float(latitude)
            fLong = float(longitude)
            fElev = float(elevation)

            if (self.minLat>fLat) :
               self.minLat = fLat
            if (self.maxLat<fLat):
               self.maxLat = fLat
            if (self.minLong>fLong):
               self.minLong = fLong
            if (self.maxLong<fLong):
               self.maxLong = fLong
            if (self.minElev>fElev):
               self.minElev = fElev
            if (self.maxElev<fElev):
               self.maxElev = fElev


            self.elevation.append(fElev)
            self.time.append(0)
            self.latitude.append(latitude)
            self.longitude.append(longitude)

            position = position + 1
         else:
            NotFinished = False
            self.length = position
      
      
            


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
         return self.elevation[int(position)]

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


   def getMaxLat(self):
      return self.maxLat

   def getMinLat(self):
      return self.minLat

   def getMaxLong(self):
      return self.maxLong

   def getMinLong(self):
      return self.minLong

   def getMinElev(self):
      return self.minElev

   def getMaxElev(self):
      return self.maxElev


   def __init__(self, coursename):

      self.GenerateRoute(coursename)
      self.GenerateScenery(self.length)

