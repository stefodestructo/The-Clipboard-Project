#!/usr/bin/env python

#heart.py

import threading
from datetime import datetime, timedelta
import serial
import sys
import pygame

from databuffer import databuffer

class FeederThread(threading.Thread):
    running = True
    addPoint = None
 
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
        self.s = serial.Serial(self.serial_device, 9600, timeout=0.1)
        self.s.readline()
    
        while self.running:
            k = self.getReading() 
      
            if self.addPoint and k != None:
                self.addPoint(int(k))

class Plotter:
    bgcolor = (255,255,255)
    linecolor = (0,0,255)
    linewidth = 3
    textcolor = (0,0,0)
    textsize = 30

    def __init__(self, feeder):
        self.size = self.width, self.height = 800, 600
        self.margin = 60 

        
        
        max_time = timedelta(seconds=12) 
        self.buf = databuffer(max_time)

        # set up feeder
        self.feeder = feeder

        #self.clearHistory()
        self.feeder.addPoint = self.addPoint

        #initialize pygame
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode(self.size)

        background = pygame.Surface(self.size).convert_alpha()
        background.fill(self.bgcolor)
         
        self.font = pygame.font.SysFont("Verdana", self.textsize)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.feeder.running = False
                sys.exit()

            elif event.type is pygame.KEYUP:
                if event.key is pygame.K_SPACE:
                    pygame.display.toggle_fullscreen()
                    #self.clearHistory()

            elif event.type is pygame.MOUSEBUTTONDOWN:
                self.clearHistory()

    def clearHistory(self):
        pass

    def generatePoints(self):
        return [(x, self.verticalTransform(y))\
                for x, y in self.data]

    def addPoint(self, q):
        self.buf.addpoint(q)

    def calculateVerticalScale(self):
        data = [i[1] for i in self.data]
        if len(self.data) != 0:
            self.top = max(data)
            self.bot = min(data)
        else:
            self.top = 0 
            self.bot = 0


    def verticalTransform(self, q):
        graph_height = self.height - 2 * self.margin
        if self.top != self.bot:
            output = graph_height - graph_height * (q - self.bot) / (self.top - self.bot) + self.margin 
        else:
            output = 0
        return output 

    def render_text(self):
        content = "Current reading: %.2f" % self.data[-1][1]
        text = self.font.render(content, True, self.textcolor)
        textsize0 = self.font.size(content)
        self.screen.blit(text, ((self.width - textsize0[0]) / 2, 10))

        content = "Peak reading: %.2f" % self.top
        text = self.font.render(content, True, self.textcolor)
        textsize1 = self.font.size(content)
        self.screen.blit(text, ((self.width - textsize1[0]) / 2, 10 + textsize0[1] + 10))

        #content = "Click anywhere to clear history!"
        #text = self.font.render(content, True, self.textcolor)
        #textsize2 = self.font.size(content)
        #self.screen.blit(text, ((self.width - textsize2[0]) / 2, self.height-textsize2[1] - 10))
        
    ### Main loop
    def main(self):
        # set up display
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)

        # set up feeder
        self.feeder.start()
        
        background = pygame.Surface(self.size).convert_alpha()
        background.fill(self.bgcolor)
         
        self.font = pygame.font.SysFont("Verdana", self.textsize)
        
        while True:
            # update date
            self.data = [(x * self.width, y) \
                    for x, y in self.buf.get_buffer()]
            # set up axes
            print 'Number of points: ', len(self.data)
            self.calculateVerticalScale()

            
            # draw stuff to screen()
            #   background
            self.screen.blit(background, (0,0))
            #   data points
            if len(self.data) > 2:
                pygame.draw.lines(self.screen, self.linecolor, False, self.generatePoints(), self.linewidth)

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
