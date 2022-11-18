import pygame

white = 255, 255, 255
green = (0, 255, 0)
dgreen = (19, 121, 19)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
grey = (200, 200, 200)

class GroundMap:
   def __init__(self, route):
  
      self.DisplayWidth=200 
      self.map = []

      length = route.GetLength()
      self.factor = length/self.DisplayWidth

      i = 0
      position = 0
      while  (i<self.DisplayWidth):
         self.map.append(route.GetHeight(position)/15)
         i = i + 1
         position = length / self.DisplayWidth * i

      
   def GetHeight(self,position):
      return self.map[position]

   def Draw(self, screen, x, y, playerBike, computerBikes):

      pygame.draw.rect(screen, red, (x, y, self.DisplayWidth, 4))

      position = 0

      while position<self.DisplayWidth:
         pygame.draw.rect(screen, dgreen, (x+position,y-self.map[position],1,self.map[position]))
         position = position + 1

      for cb in computerBikes:
         dist = int(x+(cb.GetDistance()*1000/self.factor))
         height = int(y-cb.GetHeight()/15)
         pygame.draw.circle(screen, blue, (dist, height), 3)

      playerdist = int(x+(playerBike.GetDistance()*1000/self.factor))
      playerheight = int(y-playerBike.GetHeight()/15)
      pygame.draw.circle(screen, red, (playerdist, playerheight), 3)

