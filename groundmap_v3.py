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
      self.DisplayHeight = 200
      self.routelength = route.GetLength()
      self.map =route 

      length = route.GetLength()
      self.factor = 2000/self.DisplayWidth

      
   def GetHeight(self,position):
      return self.map[position*self.factor]

   def Draw(self, screen, x, y, width, height, playerBike, computerBikes, bDisplayBikes):

      pygame.draw.rect(screen, red, (x, y, width, 4))

      wscale = float(width) / self.DisplayWidth
      hscale = float(height) / self.DisplayHeight

      # calc the left and right edge of the 2km map:
      leftedge = playerBike.GetDistance()*1000-1000
      rightedge = playerBike.GetDistance()*1000+1000

      if leftedge<0:
         leftedge=0
         rightedge=2000


      # draw the ground elevation
      position = 0

      while position<self.DisplayWidth:
         xpos = int(position*wscale)*self.factor+leftedge
         barlength = int(self.map[xpos]*hscale)
         barwidth = int(wscale)
         pygame.draw.rect(screen, dgreen, (x+xpos,y-barlength, barwidth, barlength))
         position = position + 1


      # draw kilometre tick marks
      #rpos = 0
      #while (rpos<=self.DisplayWidth):
      #   xpos = int(rpos/self.factor*wscale)
      #   pygame.draw.rect(screen, grey, (x+xpos, y, 2, 7))
      #   rpos = rpos + 1000
         

      if (bDisplayBikes==True):

         # draw the bikes
         for cb in computerBikes:
            dist = cb.GetDistance() * 1000

            if dist > leftedge or dist < rightedge
               dist = cb.GetDistance() * 1000
               dist = dist - leftedge
               dist = int(dist/self.factor*wscale)

            height = int(y-(cb.GetHeight()/15)*hscale)
            pygame.draw.circle(screen, blue, (dist, height), 3)

         playerdist = int(x+(playerBike.GetDistance()*1000/self.factor)*wscale)
         playerheight = int(y-(playerBike.GetHeight()/15)*hscale)
         pygame.draw.circle(screen, red, (playerdist, playerheight), 3)

