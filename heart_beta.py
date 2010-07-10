#!/usr/bin/env python

#heart.py

import threading
from datetime import datetime
import serial
import sys
import pygame

class FeederThread(threading.Thread):
    running = True
    addPoint = None
    average = 40
 
    def __init__(self, serial_device):
        threading.Thread.__init__(self)
        self.serial_device = serial_device
        self.running = True
        self.addPoint = None

    def getReading(self):
        x = self.s.readline()
        try:
            return int(x) 
        except ValueError:
            print 'Value Error!!!'
            print x
            return self.getReading()

    def run(self):
        self.s = serial.Serial(self.serial_device, 9600)
        self.s.readline()
    
        while self.running:
            k = self.getReading() 
      
            if self.addPoint:
                self.addPoint(k)

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
        if self.history and q > 0:
            self.history.pop(0)
            self.history.append(q)

    def __init__(self, feeder):
        self.size = self.width, self.height = 640,480
        self.max_y = self.height - 20
        self.min_y = 20
        self.feeder = feeder
        self.clearHistory()
        self.feeder.addPoint = self.addPoint

        #initialize pygame
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode(self.size)

        # set up feeder
        background = pygame.Surface(self.size).convert_alpha()
        background.fill(self.bgcolor)
         
        self.font = pygame.font.SysFont("Verdana", self.textsize)

    def calculateVerticalScale(self):
        self.top = max(max(self.history), 0)
        self.bot = min(min(self.history), 0)

        self.top = max(self.history)
        self.bot = min(self.history)

        actual_resolution = self.max_y - self.min_y
        actual_resolution = self.height
        data_range = self.top - self.bot


        if data_range != 0:
            self.vscale = actual_resolution / data_range
            print self.top, self.bot, self.vscale, data_range
            #self.vscale = data_range / actual_resolution
        else:
            self.vscale = 1
            print "foobar"

        
        #rg = (self.top - self.bot) * 1.2
    
        #if rg > 0:
        #    self.vscale = self.height / rg
        #    self.vzero = int(self.height * ((self.top - 0) / \
        #            (self.top - self.bot) + 0.1) / 1.2)
        #else:
        #    self.vscale = 1
        #    self.vzero = self.height / 2

    def verticalTransform(self, q):
        #return 320
       
        #print self.vscale * (q) 
        #return  self.vscale * (q) 

        output = 440 - 440 * (q - self.bot) / (self.top - self.bot) 

        #print output, self.vscale
        return output 

    def render_text(self):
        content = "Current reading: %.2f" % self.history[-1]
        text = self.font.render(content, True, self.textcolor)
        textsize0 = self.font.size(content)
        screen.blit(text, ((self.width - textsize0[0]) / 2, 10))

        content = "Peak reading: %.2f" % max(self.history)
        text = self.font.render(content, True, self.textcolor)
        textsize1 = self.font.size(content)
        screen.blit(text, ((self.width - textsize1[0]) / 2, 10 + textsize0[1] + 10))

        content = "Click anywhere to clear history!"
        text = self.font.render(content, True, self.textcolor)
        textsize2 = self.font.size(content)
        screen.blit(text, ((self.width - textsize2[0]) / 2, self.height-textsize2[1] - 10))
        
    ### Main loop
    def main(self):
        # set up display
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode(self.size)

        # set up feeder
        self.feeder.start()
        
        background = pygame.Surface(self.size).convert_alpha()
        background.fill(self.bgcolor)
         
        self.font = pygame.font.SysFont("Verdana", self.textsize)
        
        while True:
            # set up axes
            self.calculateVerticalScale()
            
            # draw stuff to screen
            #   background
            screen.blit(background, (0,0))
            #   data points
            pygame.draw.lines(screen, self.linecolor, False, self.generatePoints(), self.linewidth)

            #   render text
            self.render_text()
            
            # done drawing... doublebuffer!
            pygame.display.flip()
            
            self.handleEvents()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        serial_dev = sys.argv[1]

    else:
        serial_dev = "/dev/ttyUSB0"
    
    feeder = FeederThread(serial_dev)
    plotter = Plotter(feeder)
    plotter.main()
