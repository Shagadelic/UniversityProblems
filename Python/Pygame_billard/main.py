import pygame
import sys 
from pygame.locals import *

import draw
import color
import tisch
import kugel

pygame.init()
    
draw.setCanvasSize(1200, 800)

rect_x = 0.1
rect_y = 0.3
rect_width = 0.8
rect_height = 0.4
const = 0.02

#Kugelliste
fullplayer="??? "
halfplayer="??? "

fullout=0
halfout=0

lfo=0
lho=0
kugeli=tisch.kugeln()

p=0


while True:
   
    tisch.table(rect_x, rect_y, rect_width, rect_height, const)
    
    fullout, halfout, fullplayer, halfplayer, p = tisch.ball_handling(kugeli, lfo, lho, fullplayer, halfplayer, p, rect_x, rect_y, rect_width, rect_height, const)
        
    tisch.game_standing(fullplayer, halfplayer, fullout, halfout, kugeli, p)

    draw.show(1/61)
    
    draw.clear()
