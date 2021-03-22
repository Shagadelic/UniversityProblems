import draw
import color
import math
#import tisch

class Kugel():
    fout=0.75
    hout=0.75
    def __init__(self, pos_x =0.5, pos_y=0.5, rad=0.01, dir_x=0.0, dir_y=0.0, speed=0,full=True, colour=color.WHITE, number=None,friction=0.981125,infield=True,power=0):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.dir_x=dir_x
        self.dir_y=dir_y
        self.speed=speed
        self.rad=rad
        self.friction=friction
        self.colour=colour
        self.full=full
        self.number=number
        self.infield=infield
        self.power=power
    def __str__(self):
        return "Pos_x :{}, Pos_y:{}, rad :{}, dir_x :{}, dir_y :{}, speed :{}, friction :{}, full :{}, colour :{}, number :{}".format(self.pos_x,self.pos_y,self.rad,self.dir_x,self.dir_y,self.speed,self.friction,self.full,self.colour,self.number)
    
    __repr__=__str__
    
    def __eq__(self, other):
        if self.number == other.number:
            return True
        return False
    
    def displ(self):

        draw.setPenColor(self.colour)
        if self.full:
            draw.filledCircle(self.pos_x, self.pos_y, self.rad) #rad/2
            draw.setPenColor(color.WHITE)
            draw.filledCircle(self.pos_x, self.pos_y, self.rad/1.6)#rad/4
            draw.setPenColor(color.BLACK)
            if self.number !="16":
                draw.text(self.pos_x, self.pos_y, self.number)
        else:
            draw.setPenColor(color.Color(245, 225, 170))
            draw.filledCircle(self.pos_x, self.pos_y, self.rad)#rad/2
            draw.setPenColor(self.colour)
            draw.filledRectangle(self.pos_x - self.rad+0.001, self.pos_y - self.rad/2, self.rad*1.775, self.rad)
            draw.setPenColor(color.WHITE)
            draw.filledCircle(self.pos_x, self.pos_y, self.rad / 1.6)
            draw.setPenColor(color.BLACK)
            draw.text(self.pos_x, self.pos_y, self.number)



    def nextPos(self):

        self.pos_x += self.dir_x
        self.pos_y += self.dir_y
        self.dir_x *= self.friction
        self.dir_y *= self.friction
        
        #Rechnet aus wann die Kugeln zum stoppen kommen.
        if (abs(self.dir_x)**2 + abs(self.dir_y)**2)**0.5 <= 0.00001:
            self.dir_x=0
            self.dir_y=0

    def kabstk2rad(self, other):#Kugelabstand < rad
        if math.sqrt((self.pos_x - other.pos_x)**2 + (self.pos_y - other.pos_y)**2) <= self.rad*1.5:
            self.pos_x = self.pos_x + (-self.dir_x)
            self.pos_y = self.pos_y + (-self.dir_y)
            other.pos_x = other.pos_x + (-other.dir_x)
            other.pos_y = other.pos_y + (-other.dir_y)
            
            return True
        return False
    
    def kukol(self, other):
        if self.infield==False or other.infield==False:
            return
        #Abstandsvektor berechnen
        #Der Abstandsvektor (dx,dy) ist der Vektor vom Mittelpunkt der Kugel 1
        #zum Mittelpunkt der Kugel 2
        dx = self.pos_x - other.pos_x
        dy = self.pos_y - other.pos_y
        
        normAbstandsVektorZumQuadrat = dx*dx + dy*dy
        #Skalarprodukt aus Richtungsvektor Kugel 1 und Abstandsvektor berechnen
        v1d = self.dir_x * dx + self.dir_y * dy
        #Skalarprodukt aus Richtungsvektor Kugel 2 und Abstandsvektor berechnen
        v2d = other.dir_x * dx + other.dir_y * dy
        #Fuer beide Kugeln nach der Formel die neue Richtung berechnen
        self.dir_x = self.dir_x - dx *(v1d-v2d)/normAbstandsVektorZumQuadrat
        self.dir_y = self.dir_y - dy *(v1d-v2d)/normAbstandsVektorZumQuadrat
        
        other.dir_x = other.dir_x - dx *(v2d-v1d)/normAbstandsVektorZumQuadrat
        other.dir_y = other.dir_y - dy *(v2d-v1d)/normAbstandsVektorZumQuadrat
        
        


    
