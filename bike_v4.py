import time
import math

class Bike:
   def __init__(self, id, name, power, sprint, rotation, attackdist, attackpower, attacklength):

      self.Mass=100
      self.Energy=0
      self.Distance=0
      self.id = id
      self.name = name
      self.power = power
      self.sprint = sprint
      self.rotation = rotation
      self.aerofactor = 0.0
      self.AirResistForce=0.08
      self.AttackDistance = attackdist
      self.AttackLength = attacklength
      self.AttackPower = attackpower
      self.FinishTime = 0
      self.Finished = False

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

   def SetFinishTime(self, timefin):
      # record the finish time - but only if it hasn't already been set. This allows us to call this repeatedly nce the rider passes the finish
      # without constantly updating the time.
      if self.FinishTime == 0:
         self.FinishTime = timefin
         self.Finished = True

   def GetFinishTime(self):
      return self.FinishTime

   def GetFinished(self):
      return self.Finished

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

      factor = 1.0

      # if the bike is in front of this one then it might give some shelter:
      for b in Bikes:
         if b.GetId()!=self.id:
           
            # the bike 'position' is actually at the back of the image
            # the image is actually 100 pixels wide (50m long!)
            # so we add a bit to the position of this bike to get a rough idea of where the front wheel is

            frontofbike = self.GetDistance()*1000 + 35
            backofotherbike = b.GetDistance() * 1000

            otherbikegap = backofotherbike - frontofbike

            if (otherbikegap<50 and otherbikegap>0):
               # multiply the aero factor from this bike with what we have so far - this will get us the cumulative effect of all the bikes in front
               # of this one...
               factor = factor * otherbikegap/50
        
      # finally multiply the air resistance by the calculated factor. If we have no bikes in front then this will still be 1.0 
      air_resistance = air_resistance * (factor*0.75+0.25)
      self.aerofactor = factor
      air_resist_energy = air_resistance/timediff

      self.SubtractEnergy(air_resist_energy)

      # ...and friction, which will be proportional to speed:
      friction = bikespeed * 0.1
      friction_energy = friction / timediff
      self.SubtractEnergy(friction_energy)

      bikespeed = self.GetSpeed()
      self.Distance = self.Distance + (bikespeed/3600)*timediff

      if ((self.Distance*1000)>self.AttackDistance and (self.Distance*1000)<(self.AttackDistance+self.AttackLength)):
         self.AddEnergy(self.AttackPower*timediff)
