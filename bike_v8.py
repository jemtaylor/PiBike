import time
import math

class Bike:
   def __init__(self, id, name, image, power, sprint, rotation, attackdist, attackpower, attacklength):

      self.Mass=100
      self.Energy=0
      self.Distance=0
      self.Height=0
      self.id = id
      self.name = name
      self.image = image
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
      self.RecoveryPower = 0
      self.UseRecovery = False

   def GetName(self):
      return self.name

   def GetId(self):
      return self.id

   def GetImage(self):
      return self.image

   def GetRotation(self):
      return self.rotation;

   def GetAeroFactor(self):
      return self.aerofactor

   def ReduceRecoveryPower(self, change):
      self.RecoveryPower = self.RecoveryPower - change
      if self.RecoveryPower < 0:
         self.RecoveryPower = 0
         self.UseRecovery = False

   def IncreaseRecoveryPower(self, change):
      self.RecoveryPower = self.RecoveryPower + change

   def GetRecoveryPower(self):
      return self.RecoveryPower

   def SetUseRecovery(self, state):
      self.UseRecovery = state

   def GetUseRecovery(self):
      return self.UseRecovery

   def SetRotation(self, r):
      if r>self.rotation:
         self.rotation = self.rotation + 1
      if r<self.rotation:
         self.rotation = self.rotation - 1

   def SetFinishTime(self, timefin):
      # record the finish time - but only if it hasn't already been set. This allows us to call this repeatedly 
      # once the rider passes the finish without constantly updating the time
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

      speed = math.sqrt(2*self.Energy/self.Mass) *0.5
      return speed

   def GetDistance(self):
      return self.Distance

   def SetHeight(self, h):
      self.Height = h

   def GetHeight(self):
      return self.Height

   def GetPower(self):
      if self.RecoveryPower>self.AttackPower:
         self.UseRecovery = True

      if self.UseRecovery==True:
         self.ReduceRecoveryPower(10)   
         return self.power+self.RecoveryPower
      else:
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
           
            thisbike = self.GetDistance()*1000
            backofotherbike = b.GetDistance()*1000

            otherbikegap = backofotherbike - thisbike

            # multiply the aero factor from this bike with what we have so far - this will get us the cumulative effect of all the bikes in front
            # of this one...
            if (otherbikegap<3 and otherbikegap>0):
               factor = factor * (1 - (otherbikegap/3))
            if (otherbikegap<10 and otherbikegap>3):
               factor = factor * ((otherbikegap-3)/17)

        
      # finally multiply the air resistance by the calculated factor. If we have no bikes in front then this will still be 1.0 
      air_resistance = air_resistance * (factor*0.5+0.5)
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
