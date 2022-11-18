import time
import math

class Bike:
   def __init__(self, id, name, power, sprint, rotation):

      self.Mass=100
      self.Energy=0
      self.Distance=0
      self.id = id
      self.name = name
      self.power = power
      self.sprint = sprint
      self.rotation = rotation
      self.aerofactor = 0.0
      self.AirResistForce=0.01

   def GetName(self):
      return self.name

   def GetId(self):
      return self.id

   def GetRotation(self):
      return self.rotation;

   def GetAeroFactor(self):
      return self.aerofactor

   def SetRotation(self, r):
      if r>self.rotation:
         self.rotation = self.rotation + 1
      if r<self.rotation:
         self.rotation = self.rotation - 1

   def AddEnergy(self, e):
      self.Energy = self.Energy + e
      if self.Energy < 0:
         self.Energy = 0

   def SubtractEnergy(self, e):
      if self.Energy < e:
         self.Energy=0
      else:
         self.Energy = self.Energy - e

   def GetEnergy(self):
      return self.Energy

   def GetMass(self):
      return self.Mass

   def GetSpeed(self):

      speed = math.sqrt(2*self.Energy/self.Mass) *0.7
      return speed

   def GetDistance(self):
      return self.Distance

   def GetPower(self):
      return self.power

   def GetSprint(self):
      return self.sprint

   def Update(self, Bikes, timediff):

      bikespeed = self.GetSpeed()

      air_resistance = bikespeed * bikespeed * self.AirResistForce

      # find the bike immediately in front of this one:
      position=0
      for b in Bikes:
         if b.GetId()==self.id:
            leader = position - 1
         position = position + 1
           
      if leader!=-1: # if this is -1 then this bike is in the lead!
         otherBike = Bikes[leader]

         # reduce the air resistance by up to 75% if the other bike is within 100m
         # the bike 'position' is actually at the back of the image
         # the image is actually 113 pixels wide (113m long!)

         #frontofbike = self.GetDistance()*1000 + 113  
         #backofotherbike = other.GetDistance() * 1000

         #otherbikegap = backofotherbike - frontofbike

         #if (otherbikegap<100 and otherbikegap>0):
            
         #   factor = 1-(otherbikegap/100)
         #   self.aerofactor = factor
         #   air_resistance = 0 # air_resistance * factor
         #   #print (otherBikeGap, factor)
         #else:
         #   self.aerofactor=0.0
         
      air_resist_energy = air_resistance/timediff

      self.SubtractEnergy(air_resist_energy)

      bikespeed = self.GetSpeed()
      self.Distance = self.Distance + (bikespeed*timediff)/1000

