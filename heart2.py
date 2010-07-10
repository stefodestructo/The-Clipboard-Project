#!/usr/bin/env python

#heart.py

import threading
import time
import serial
import sys
import pygame

class FeederThread(threading.Thread):
  running = True
  addPoint = None
  average = 40
  
  def getReading(self):
      x = self.s.readline()
      try:
          return int(x) 
      except ValueError:
          print 'Value Error!!!'
          print x
          return self.getReading()

  def averageReadings(self, average):
    sum = 0.0
    for i in xrange(average):
      sum += self.getReading()
    return sum / average

  def readingToPounds(self, x):
    return (x - self.zero)/self.slope

  def run(self):
    self.s = serial.Serial("/dev/ttyUSB0", 9600)
    self.s.readline()
    
    #print "Measuring zero..."
    #self.zero = self.averageReadings(1000)
    #print "OK, zero = ", self.zero
    
    while self.running:
      k = self.getReading() 
      
      if self.addPoint:
        self.addPoint(k)




    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.addPoint = None

    def getReading(self):
        return int(128)

    def run(self):
        while self.running:
            if self.addPoint:
                self.addPoint(self.getReading())

class Plotter:
    bgcolor = (255,255,255)
    linecolor = (0,0,255)
    linewidth = 3
    textcolor = (0,0,0)
    textsize = 30

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.feeder.running = False
                sys.exit()

            elif event.type is pygame.KEYUP:
                if event.key is pygame.K_SPACE:
                    self.clearHistory()

            elif event.type is pygame.MOUSEBUTTONDOWN:
                self.clearHistory()

    def clearHistory(self):
        self.history = [0.0 for x in xrange(self.width)]

    def generatePoints(self):
        history = self.history
        return [(i, self.verticalTransform(el))\
                for i, el in enumerate(history)]

    def addPoint(self, q):
        if self.history:
            self.history.pop(0)
            self.history.append(q)

    def __init__(self, feeder):
        self.size = self.width, self.height = 640,480
        self.feeder = feeder
        self.clearHistory()
        self.feeder.addPoint = self.addPoint

    def calculateVerticalScale(self):
        self.top = max(max(self.history), 0)
        self.bot = min(min(self.history), 0)
        rg = (self.top - self.bot) * 1.2
    
        if rg > 0:
            self.vscale = self.height / rg
            self.vzero = int(self.height * ((self.top - 0) / \
                    (self.top - self.bot) + 0.1) / 1.2)
            print self.vzero
        else:
            self.vscale = 1
            self.vzero = self.height / 2
            print "foobar"


    def verticalTransform(self, q):
        return self.vzero - self.vscale * q

    ### Main init code
    def main(self):
        # set up display
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode(self.size)

        # set up feeder
        self.feeder.start()
        
        background = pygame.Surface(self.size).convert_alpha()
        background.fill(self.bgcolor)
        #background = pygame.image.load("background.jpg").convert_alpha()
         
        font = pygame.font.SysFont("Verdana", self.textsize)
        
        k = 0
        while True:
            # set up axes
            self.calculateVerticalScale()
            
            # draw stuff to screen
            #   background
            screen.blit(background, (0,0))
            #   data points
            pygame.draw.lines(screen, self.linecolor, False, self.generatePoints(), self.linewidth)
            #   text
            content = "Current reading: %.2f" % self.history[-1]
            text = font.render(content, True, self.textcolor)
            textsize0 = font.size(content)
            screen.blit(text, ((self.width - textsize0[0])/2,10))

            content = "Peak reading: %.2f" % max(self.history)
            text = font.render(content, True, self.textcolor)
            textsize1 = font.size(content)
            screen.blit(text, ((self.width - textsize1[0])/2,10 + textsize0[1] + 10))

            content = "Click anywhere to clear history!"
            text = font.render(content, True, self.textcolor)
            textsize2 = font.size(content)
            screen.blit(text, ((self.width - textsize2[0])/2,self.height-textsize2[1]-10))
            
            # done drawing... doublebuffer!
            pygame.display.flip()
            
            self.handleEvents()




    
if __name__ == "__main__":
    #feeder = PiFeederThread()
    feeder = FeederThread()
    if len(sys.argv)>1:
        feeder.average = int(sys.argv[1])
    plotter = Plotter(feeder)
    plotter.main()
