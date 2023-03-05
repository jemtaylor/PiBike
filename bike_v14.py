import time
import math


# v13 - changed SetRotation to accept a gradient
# v14 - re-do the physics!

class Bike:
   def __init__(self, id, name, image, power, sprint, rotation, attackdist, attackpower, attacklength):

      self.Mass=100
      self.Speed=0
      self.Distance=0
      self.prevDistance=0
      self.Height=0
      self.id = id
      self.name = name
      self.image = image
      self.power = power
      self.sprint = sprint
      self.rotation = rotation
      self.aerofactor = 0.0
      self.AirResistForce=0.1
      self.AttackDistance = attackdist
      self.AttackLength = attacklength
      self.AttackPower = attackpower
      self.FinishTime = 0
      self.Finished = False
      self.RecoveryPower = 0
      self.UseRecovery = False
      self.BehindTime = 0
      self.Finished=False

   def GetName(self):
      return self.name

   def GetId(self):
      return self.id

   def GetImage(self):
      return self.image

   def GetRotation(self):
      return self.rotation;

   def GetRotationAngle(self):
     grad = self.rotation/100
     angle = math.atan(grad)*180/3.14
     angle = angle/2
     return angle


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
      self.rotation = r

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

   def SetBehindTime(self, tm):
      self.BehindTime = tm

   def GetBehindTime(self):
      return self.BehindTime

   def GetSpeed(self):
      return self.Speed

   def SetSpeed(self, s):
      self.Speed = s

   def GetMass(self):
      return self.Mass

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
         self.ReduceRecoveryPower(1)   
         return self.power+self.RecoveryPower
      else:
         return self.power

   def GetSprint(self):
      return self.sprint

   def Update(self, route, Bikes, timediff, isComputer, player_energy):

      self.Height = route.GetHeight(int(self.GetDistance()*1000))
      bikespeed = (self.GetSpeed()*1000)/3600   # in metre per second

      # the bike's current KE is given by 1/2mv^2
      kinecticEnergy = 0.5 * self.Mass * bikespeed * bikespeed

      if isComputer:
         # the rider adds energy by pedalling
         if self.GetFinished()==False:
            kinecticEnergy = kinecticEnergy + self.GetPower()*timediff

            # computer bikes will start to sprint for the line in the final 10% of the race:
            if self.GetDistance()*1000 > route.GetLength() * 0.9:
               kinecticEnergy = kinecticEnergy + self.GetSprint()*timediff
      else:
         # only add energy if the bike is going under 60km/h - above this you shouldn't be able to add energy with the pedals!
         if bikespeed < 16.66:
            kinecticEnergy = kinecticEnergy + player_energy


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

      kinecticEnergy = kinecticEnergy - air_resist_energy

      # ...and friction, which will be proportional to speed:
      friction = bikespeed * 0.15
      friction_energy = friction / timediff
      kinecticEnergy = kinecticEnergy - friction_energy

      if isComputer:
         if ((self.Distance*1000)>self.AttackDistance and (self.Distance*1000)<(self.AttackDistance+self.AttackLength)):
            kinecticEnergy = kinecticEnergy + (self.AttackPower*timediff)

      # calculate how much energy the bike loses up the hill
      # get the height from where the bike was last iteration:
      lastHeight = route.GetHeight(int(self.prevDistance*1000))
      heightDiff = self.Height - lastHeight
      hillEnergy = self.Mass * heightDiff * 30

      #if isComputer==False:
      #   print "last height=", lastHeight, " this height=", self.Height, " height diff=", heightDiff, " energy change=", hillEnergy, " tot energy=", kinecticEnergy

      kinecticEnergy = kinecticEnergy - hillEnergy

      if kinecticEnergy < 0:
         kinecticEnergy=0

      # the new speed can now be calculated:
      newspeed = math.sqrt((2 * kinecticEnergy)/self.Mass) # in metres per second

      # convert to km/h
      newspeed = (newspeed*3600)/1000
      self.SetSpeed(newspeed)

      # calc the new distance:
      self.prevDistance = self.Distance
      self.Distance = self.Distance + (newspeed/3600)*timediff

