#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import pygame
import random
import math
import sys
from bike_v7 import Bike
from route_v7 import Route


pulse_count = 0
currtm = time.time()
lastinterval=0
race_started=False
zoom=25

white = 255, 255, 255
green = (0, 255, 0)
dgreen = (19, 121, 19)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
# light shade of the button 
color_light = (170,170,170) 
# dark shade of the button 
color_dark = (100,100,100)

def InitDisplay():

  # initialisation
   pygame.init()

   screen = pygame.display.set_mode((800,450)) # Set screen size of pygame window
   background = pygame.Surface(screen.get_size())  # Create empty pygame surface
   background.fill((255,255,255))     # Fill the background white color (red,green,blue)
   background = background.convert()  # Convert Surface to make blitting faster

   screen.blit(background, (0, 0))

   # Print in titlebar
   text = "Cycling"
   pygame.display.set_caption(text)

   return screen

def write(msg="pygame is cool", size=24, color=(0,0,0)):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext


def bike_pulse(channel):
    global currtm
    global lastinterval
    global race_started

    newtm = time.time()
    interval = newtm - currtm

    #print ("pulse " + str(interval))

    race_started = True

    currtm = newtm
    if (interval>0.2 and interval<3.0):
       lastinterval=interval
    else:
       lastinterval=0


def left_button(channel):
    print ('left')

def right_button(channel):
    print ('right')


def GetFinalLeaderboard(playerBike, computerBikes):   
   # unlike the race leaderboard, the final finishing positions are determined by the finish times
    racePosition = []
    for b in computerBikes:
       racePosition.append(b)

    racePosition.append(playerBike)
    racePosition.sort(key=sortFuncTime, reverse=False)

    return racePosition

def sortFuncTime(b):
   if b.GetFinishTime()==0:
      return 999999999999
   else:
      return b.GetFinishTime()


def GetLeaderboard(playerBike, computerBikes):   
    racePosition = []
    racePosition.append(playerBike)

    for b in computerBikes:
       racePosition.append(b)

    racePosition.sort(key=sortFuncDist, reverse=True)

    return racePosition

def sortFuncDist(b):
   return b.GetDistance()

def GetRaceLength(screen):
   #lengthchoice = pygame.image.load("/home/pi/bike/racelength.gif").convert()

   screen.fill(white)
   #screen.blit(racelength, (0,0)) 

   screen.blit(write("Choose Distance:", size=48), (160,100))

   pygame.display.flip()

   nochoice = True

   while nochoice==True: 
      # stores the (x,y) coordinates into 
      # the variable as a tuple 
      mouse = pygame.mouse.get_pos()  


      for ev in pygame.event.get(): 
         #checks if a mouse is clicked 
         if ev.type == pygame.MOUSEBUTTONDOWN: 
            #print (mouse[0], mouse [1])
            if 360 <= mouse[0] <= 520 and 200 <= mouse[1] <= 230: 
               choice = 2000
               nochoice = False 

            if 360 <= mouse[0] <= 520 and 250 <= mouse[1] <= 280: 
               choice = 10000
               nochoice = False 

            if 360 <= mouse[0] <= 520 and 300 <= mouse[1] <= 330: 
               choice = 15000
               nochoice = False 

            if 360 <= mouse[0] <= 520 and 350 <= mouse[1] <= 380: 
               choice = 20000
               nochoice = False 

            if 360 <= mouse[0] <= 520 and 400 <= mouse[1] <= 430: 
               choice = 25000
               nochoice = False 

         if 360 <= mouse[0] <= 520 and 200 <= mouse[1] <= 230:
            pygame.draw.rect(screen,color_light,[360,200,160,30])
         else:
            pygame.draw.rect(screen,color_dark,[360,200,160,30])

         if 360 <= mouse[0] <= 520 and 250 <= mouse[1] <= 280:
            pygame.draw.rect(screen,color_light,[360,250,160,30])
         else:
            pygame.draw.rect(screen,color_dark,[360,250,160,30])

         if 360 <= mouse[0] <= 520 and 300 <= mouse[1] <= 330:
            pygame.draw.rect(screen,color_light,[360,300,160,30])
         else:
            pygame.draw.rect(screen,color_dark,[360,300,160,30])

         if 360 <= mouse[0] <= 520 and 350 <= mouse[1] <= 380:
            pygame.draw.rect(screen,color_light,[360,350,160,30])
         else:
            pygame.draw.rect(screen,color_dark,[360,350,160,30])

         if 360 <= mouse[0] <= 520 and 400 <= mouse[1] <= 430:
            pygame.draw.rect(screen,color_light,[360,400,160,30])
         else:
            pygame.draw.rect(screen,color_dark,[360,400,160,30])

      screen.blit(write("2 km", size=48), (400,200))
      screen.blit(write("10 km", size=48), (400,250))
      screen.blit(write("15 km", size=48), (400,300))
      screen.blit(write("20 km", size=48), (400,350))
      screen.blit(write("25 km", size=48), (400,400))
     
      pygame.display.update() 
   
   
   screen.fill(white)
   screen.blit(write( str(choice/1000) + "km", size=48), (300,200))
   pygame.display.update() 
   time.sleep(5)


   return choice

def DisplayPodium(screen, playerBike, computerBikes, raceStartTime):
   podium = pygame.image.load("/home/pi/bike/podium.gif").convert()

   screen.fill(white)
   screen.blit(podium, (0,0)) 

   screen.blit(write("Winner", size=48), (160,400))

   racePosition = GetFinalLeaderboard(playerBike, computerBikes)

   txt = racePosition[0].GetName()
   screen.blit(write(txt, size=48), (500,400))

   pygame.display.flip()

   time.sleep(7)

   screen.fill(white)

   winningTime = racePosition[0].GetFinishTime()
   raceElapsedTime = winningTime - raceStartTime
   m, s = divmod(raceElapsedTime, 60)
   h, m = divmod(m, 60)

   strRaceTime = '{:.0f}h:{:.0f}m:{:.3f}s'.format(h, m, s)

   screen.blit(write("Position:            Rider:           Time:"), (145, 65))
   position = 0  
   for b in racePosition:
      if (position%2)==0:
         pygame.draw.rect(screen, grey, (0, 100+position*30, 800, 30)) 
         
      screen.blit(write(str(position+1), size=24), (180, 100 + position*30))
      screen.blit(write(b.GetName(), size=24), (200, 100 + position*30)) 

      finishTime = b.GetFinishTime()
      if finishTime==0:
         displayTime = "DNF"
      else:
         gap = round(finishTime - winningTime,3)
         displayTime = str(gap) 

      if position>0:
         screen.blit(write("+" + displayTime, size=24), (400, 100 + position*30)) 
      else:
         screen.blit(write(strRaceTime, size=24), (400, 100 + position*30)) 

      position = position + 1

   pygame.display.flip()

   time.sleep(10)
   


def bikeRotation (height_diff, dist_diff):
   if height_diff==0 or dist_diff==0:
      return 0

   rot =  math.atan(height_diff/(dist_diff*1000))*180/3.14
   rot = rot * -0.1

   return rot

def DrawLeaderboard(screen, leaderboard, x, y):
   race_pos=1
   leaderDist = leaderboard[0].GetDistance()

   for b in leaderboard:
      bikedist = b.GetDistance() * 1000
      distdiff = int( round( ((leaderDist - b.GetDistance()) * 1000), 0) )
      nametxt = str(race_pos) + " " + b.GetName()
      postxt = "+" + str(distdiff) + "m"
      #txt = "{:.2f}"
      #postxt = txt.format(bikedist)
      recoverytxt = str(b.GetRecoveryPower())
      screen.blit(write(nametxt), (x, y + race_pos*15))
      screen.blit(write(postxt), (x+150, y + race_pos*15))
      screen.blit(write(recoverytxt), (x+230, y + race_pos*15))
      race_pos = race_pos + 1

def plotX(groundpos):
   global zoom
   #print (groundpos, groundpos*zoom)
   return groundpos*zoom


def plotBike(screen, bike, leftedge, bikepic, route):
 
   dist = bike.GetDistance()*1000
   height = route.GetHeight(int(dist))
   bikeX = plotX(dist-leftedge)
   bikeY = 300 - height/4  + bike.GetId()*3
   #print (dist, height, bikeY)

   scalefactor = zoom/40.0
   width = int(scalefactor*113)
   height = int(scalefactor*80)
   #print (scalefactor, width, height)
   scaled_bike = pygame.transform.scale(bikepic, (width,height) )
   rotated_bike = pygame.transform.rotate(scaled_bike, bike.GetRotation() )
   screen.blit(rotated_bike, (bikeX,bikeY)) 


def plotScenery(screen, dist, leftedge, pic, picwidth, picheight, route):

   global zoom 
   height = route.GetHeight(int(dist))
   sceneX = plotX(dist-leftedge)

   scalefactor = zoom/40.0
   scalewidth = int(scalefactor*picwidth)
   scaleheight = int(scalefactor*picheight)
   sceneY = 300 - height/4 - scaleheight
   scaled_pic = pygame.transform.scale(pic, (scalewidth,scaleheight) )
   screen.blit(scaled_pic, (sceneX,sceneY)) 


def calculateZoom(computerbikes, playerbike, racelength):

   behind = 0.0
   infront = 999
   playerdist = playerbike.GetDistance()

   # find the nearest rider in front and nearest rider behind the player
   for b in computerbikes:
      compdist = b.GetDistance()
      if compdist<playerdist and compdist>behind:
         behind = compdist
      if compdist>playerdist and compdist<infront:
         infront = compdist

   if infront==999: # player must be in the lead!
      infront = playerdist+0.01

   range = (infront - behind)*1000  # in meters
   if range<20:
      spanzoom = 40
   else:
      if range>70:
         spanzoom = 20
      else:
         spanzoom = (20- ((range-20)/50)*20)+20

   return spanzoom


def calculateZoomOld(leaderboard, playerdist, racelength):

   # if we're nearing the end of the race, then zoom in!
   racepercent = playerdist / racelength 
   if racepercent>1.0:
      racepercent = 1.0

   finalzoom = (racepercent*40)

   # take the difference between the leader and the person in last place:
   leader = leaderboard[0].GetDistance()*1000 # in meters
   lastplace = len(leaderboard) - 1
   loser = leaderboard[lastplace].GetDistance() * 1000 # in meters

   race_span = leader - loser

   if race_span<20:
      spanzoom = 40
   else:
      if race_span > 100:
         spanzoom = 20
      else:
         spanzoom = (20 - ((race_span-20)/80)*20) + 20

   if finalzoom>spanzoom:
      return finalzoom
   else:
      return spanzoom 
 
def run(screen, playerBike, computerBikes, Race_Length):

   global lastinterval
   global race_started
   global zoom
    
   route = Route(Race_Length)

   bluebike = pygame.image.load("/home/pi/bike/bikebluesmall.gif").convert()
   redbike = pygame.image.load("/home/pi/bike/bikeredsmall.gif").convert()
   greybike = pygame.image.load("/home/pi/bike/bikegreysmall.gif").convert()
   tree = pygame.image.load("/home/pi/bike/tree.gif").convert()
   giftshop = pygame.image.load("/home/pi/bike/giftshop.gif").convert()
   cafe = pygame.image.load("/home/pi/bike/cafe.gif").convert()
   bookshop = pygame.image.load("/home/pi/bike/bookshop.gif").convert()
   finish = pygame.image.load("/home/pi/bike/finish.gif").convert()
   flamerouge = pygame.image.load("/home/pi/bike/flamerouge.gif").convert()
   crowd = pygame.image.load("/home/pi/bike/crowd.gif").convert()
   WHITE = (255, 255, 255)
   bluebike.set_colorkey(WHITE)  # White colors will not be blit.
   redbike.set_colorkey(WHITE)  # White colors will not be blit.
   greybike.set_colorkey(WHITE)  # White colors will not be blit.
   tree.set_colorkey(WHITE)  # White colors will not be blit.
   bookshop.set_colorkey(WHITE)  # White colors will not be blit.
   cafe.set_colorkey(WHITE)  # White colors will not be blit.
   giftshop.set_colorkey(WHITE)  # White colors will not be blit.
   finish.set_colorkey(WHITE)  # White colors will not be blit.
   flamerouge.set_colorkey(WHITE)  # White colors will not be blit.
   crowd.set_colorkey(WHITE)  # White colors will not be blit.

   running = True
   currtime = time.time()
   lastinterval = 0

   race_started = False

   while running:
      newtm = time.time()
      timediff = newtm - currtime
      currtime = newtm

      #print (timediff, computerBikes[0].GetDistance(), computerBikes[0].GetSpeed(), computerBikes[0].GetEnergy())

      if (timediff<0.02):
         print (timediff,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
         timediff = 0.09

      leaderboard = GetLeaderboard(playerBike, computerBikes)

      #lines for auto-play:
      #race_started=True
      #lastinterval=7

      # add in energy from pedalling
      if lastinterval>0:
         cyclist_energy = playerBike.GetPower()/lastinterval
         lastinterval = 0
      else:
         cyclist_energy = 0

      playerBike.AddEnergy(cyclist_energy)

      if race_started==True:
         for b in computerBikes:
            if b.GetFinished()==False:
               b.AddEnergy(b.GetPower()*timediff)
  
               # computer bikes will start to sprint for the line in the final 10% of the race: 
               if b.GetDistance()*1000 > Race_Length * 0.9:
                  b.AddEnergy(b.GetSprint()*timediff)

            # if the bike is slipstreaming then he will gain recovery power
            if b.GetAeroFactor()<0.7 and b.GetUseRecovery()==False:
               b.IncreaseRecoveryPower(10)

            comp_dist = b.GetDistance()
            comp_height = route.GetHeight(int(comp_dist*1000))

            b.Update(leaderboard, timediff)

            comp_new_dist = b.GetDistance()
            comp_new_height = route.GetHeight(int(comp_new_dist*1000))
            comp_height_diff = comp_height - comp_new_height
            comp_dist_diff= comp_new_dist - comp_dist
            b.SetRotation(bikeRotation(comp_height_diff, comp_dist_diff))

            comp_pot_energy = b.GetMass() * comp_height_diff * 3
            b.AddEnergy(comp_pot_energy)

      player_dist = playerBike.GetDistance()
      player_height = route.GetHeight(int(player_dist*1000))

      playerBike.Update(leaderboard, timediff)
      
      player_new_dist = playerBike.GetDistance()
      player_new_height = route.GetHeight(int(player_new_dist*1000))
      player_height_diff = player_height - player_new_height
      player_dist_diff = player_new_dist - player_dist
      playerBike.SetRotation(bikeRotation(player_height_diff,player_dist_diff))

      player_pot_energy = playerBike.GetMass() * player_height_diff * 3
      playerBike.AddEnergy(player_pot_energy)
 
      lastinterval=0
      
      for event in pygame.event.get():

         if event.type == pygame.QUIT:
            #
            print ("quit detected")
            #running = False

      zoom = calculateZoom(computerBikes, playerBike, route.GetLength())

      screenwidth = (800 / zoom) # meters
      screen.fill(white)

      txt = "Zoom {:.2f}"
      displayStr = txt.format(zoom)
      screen.blit(write(displayStr), (50,20))

      txt = "screenwidth {:.2f}"
      displayStr = txt.format(screenwidth)
      screen.blit(write(displayStr), (150,20))

      txt = "Speed {:.2f} km/h"
      displayStr = txt.format(playerBike.GetSpeed())
      screen.blit(write(displayStr), (100,390))

      txt = "Height {:.2f}"
      displayStr = txt.format(round(player_new_height,1))+"m"
      screen.blit(write(displayStr), (100,410))

      txt = "Distance : {:.2f}"
      displayStr = txt.format(player_new_dist) + "km"
      screen.blit(write(displayStr), (100,430))

      leaderboard = GetLeaderboard(playerBike, computerBikes)
      DrawLeaderboard(screen, leaderboard, 500, 350)

      leftedge = player_dist

      for b in computerBikes:
         if leftedge>b.GetDistance():
            leftedge = b.GetDistance()

      # if the computer falls more than 60% of the screen behind the player then he will fall off the screen:
      dropoff = screenwidth * 0.6  # in meters 
      dropoff = dropoff / 1000  # in km
      
      if leftedge < player_dist - dropoff:
         leftedge = player_dist - dropoff

      left = leftedge * 1000
      
      routelen = route.GetLength()

      # Draw the scenery:
      groundpos =left-(screenwidth/4)                 # start from just off the left edge
      while groundpos < left + (screenwidth* 1.1):     # continue to just off the right edge

         intgroundpos = int(groundpos)
         groundheight = route.GetHeight(intgroundpos)

         # check for scenery
         item = route.GetScenery(intgroundpos)

         if item == "tree":
            plotScenery(screen, intgroundpos, left, tree, 84, 95, route)

         if item == "cafe":
            plotScenery(screen, intgroundpos, left, cafe, 113, 118, route)

         if item == "bookshop":
            plotScenery(screen, intgroundpos, left, bookshop, 156, 130, route)

         if item == "giftshop":
            plotScenery(screen, intgroundpos, left, giftshop, 168, 132, route)
         
         if item == "finish":
            plotScenery(screen, intgroundpos, left, finish, 200, 180, route)
         
         if item == "flamerouge":
            plotScenery(screen, intgroundpos, left, flamerouge, 158, 197, route)
         
         if item == "crowd":
            plotScenery(screen, intgroundpos, left, crowd, 355, 103, route)
         
         groundpos = groundpos + 1

      # Draw the ground:
      groundpos =left
      while groundpos < left + screenwidth:
         
         groundheight = route.GetHeight(int(groundpos))

         # Draw the ground green with a red line at the finish
         if int(groundpos) == route.GetLength():
            pygame.draw.rect(screen, red, (plotX(groundpos-left), 300-(groundheight/4), 40, 20)) 
         else:
            pygame.draw.rect(screen, green, (plotX(groundpos-left), 300-(groundheight/4), 40, 20)) 
        
         groundpos = groundpos + 1

      # Draw the bikes:
      for b in computerBikes:
         plotBike(screen, b, leftedge*1000, bluebike, route)
         #pygame.draw.rect(screen, red, (computerbikeX, computerbikeY, 5, 5))

      if playerBike.GetFinished()==True: 
         plotBike(screen, playerBike, leftedge*1000, greybike, route)
      else:
         plotBike(screen, playerBike, leftedge*1000, redbike, route)

      aero = playerBike.GetAeroFactor()
      aerobarlength = aero * 100
      
      pygame.draw.rect(screen, black, (197, 38, 106, 24)) 
      pygame.draw.rect(screen, green, (200, 40, aerobarlength, 20)) 
      
      pygame.display.flip()

      # record finish time for each rider:
      if (playerBike.GetDistance()*1000)>= route.GetLength():
         playerBike.SetFinishTime(currtime)
         #print ("Player Finished " + str(currtime))
      for b in computerBikes:
         if (b.GetDistance()*1000)>= route.GetLength():
            b.SetFinishTime(currtime)

      # race finishes when all riders reach the end
      allFinished = True
      if (playerBike.GetDistance()*1000)<= route.GetLength():
         allFinished = False
      else:
         # player has finished, allow any bikes within a few meters to finish too
         for b in computerBikes:
            if b.GetDistance()*1000<= route.GetLength() and b.GetDistance()*1000> route.GetLength()-400:
               allFinished = False
         
        
      if allFinished:
         running = False



def main():
   # Setup GPIO input
   try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 7
      GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 8
      GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 10
      GPIO.add_event_detect(4, GPIO.FALLING, callback=bike_pulse, bouncetime=200)
      GPIO.add_event_detect(14, GPIO.FALLING, callback=left_button, bouncetime=200)
      GPIO.add_event_detect(15, GPIO.FALLING, callback=right_button, bouncetime=200)
   except Exception as e:
      print('exception thrown by GPIO'.format(e))
      return

   screen = InitDisplay()
   raceLength = GetRaceLength(screen)

   while True:
      # id, name, power, sprint, rotation, attackdist, attackpower, attacklength
      computerBike1 = Bike(1, "Chris Frome", 7500, 2000, 0, random.randint(0, raceLength), 5000, 1000)
      computerBike2 = Bike(2, "Peter Sagan", 7000, 3000, 0, random.randint(0, raceLength), 5000, 1000)
      computerBike3 = Bike(3, "Geraint Thomas", 6700, 1000, 0, random.randint(0, raceLength), 5000, 1000)
      computerBike4 = Bike(4, "Vincenzo Nibali", 8000, 1000, 0, random.randint(0, raceLength), 5000, 1000)
      playerBike = Bike(5, "Player", 7000, 0, 0, 0, 0, 0)

      computerBikes = [ computerBike1, computerBike2, computerBike3, computerBike4 ]

      raceStartTime = time.time()
      run(screen, playerBike, computerBikes, raceLength)

      DisplayPodium(screen, playerBike, computerBikes, raceStartTime)

      raceLength = GetRaceLength(screen)
  
if __name__=="__main__":
   main()

 
