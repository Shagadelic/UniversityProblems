import pygame
import time
import random
import color
import draw
import math
import kugel

def table(rect_x,rect_y,rect_width,rect_height,const):
    """
    Initialisiert/zeichnet den Tisch.
    """
    #Canvas size########################################################
    #draw.setCanvasSize(600,600)
    #Bounds#############################################################
    draw.setPenColor(color.Color(184, 134, 11))
    draw.filledRectangle(rect_x,rect_y,rect_width,rect_height)
    
    #Field##############################################################
    draw.setPenColor(color.GREEN)
    draw.filledRectangle(rect_x+const,rect_y+const,rect_width-2*const,rect_height-2*const)
    #Holes##############################################################
    draw.setPenColor(color.BLACK)
    #hole down left
    draw.filledPolygon([rect_x,rect_x+const*3,rect_x],[rect_y,rect_y,rect_y+const*3])
    #hole down right
    draw.filledPolygon([rect_x+rect_width,rect_x+rect_width-const*3,rect_x+rect_width],[rect_y,rect_y,rect_y+const*3])
    #hole up left
    draw.filledPolygon([rect_x,rect_x+const*3,rect_x],[rect_y+rect_height,rect_y+rect_height,rect_y+rect_height-const*3])
    #Hole up right
    draw.filledPolygon([rect_x+rect_width,rect_x+rect_width-const*3,rect_x+rect_width],[rect_y+rect_height,rect_y+rect_height,rect_y+rect_height-const*3])
    #hole mid down
    draw.filledRectangle(rect_x+(rect_width/2)-const, rect_y, const*2, const)
    #hole mid up
    draw.filledRectangle(rect_x+(rect_width/2)-const, rect_y+rect_height-const, const*2, const)
    #Markings###########################################################
    draw.setPenColor(color.LIGHT_GRAY)
    #left side
    leb=rect_y
    for i in range(3):
        leb+=rect_height/4
        draw.filledRaute(rect_x+const/2,leb,const/2)
    #right side
    rib=rect_y
    for i in range(3):
        rib+=rect_height/4
        draw.filledRaute(rect_x+rect_width-const/2,rib,const/2)
    #lower side
    lob=rect_x
    for i in range(7):
        lob+=rect_width/8
        if i!=3:
            draw.filledRaute(lob,rect_y+const/2,const/2)
    #upper side
    upb=rect_x
    for i in range(7):
        upb+=rect_width/8
        if i!=3:
            draw.filledRaute(upb,rect_y+rect_height-const/2,const/2)
    
    
def kugeln():
    """
    Initialisiert die Kugeln in Startaufstellung
    """
    kug1=kugel.Kugel()
    kug2=kugel.Kugel()
    kug3=kugel.Kugel()
    kug4=kugel.Kugel()
    kug5=kugel.Kugel()
    kug6=kugel.Kugel()
    kug7=kugel.Kugel()
    kug8=kugel.Kugel()
    kug9=kugel.Kugel()
    kug10=kugel.Kugel()
    kug11=kugel.Kugel()
    kug12=kugel.Kugel()
    kug13=kugel.Kugel()
    kug14=kugel.Kugel()
    kug15=kugel.Kugel()
    kug16=kugel.Kugel()
    
    kuli =   [kug1,kug2,kug3,kug4,kug5,kug6,kug7,kug13,kug9,kug10,kug11,kug12,kug8,kug14,kug15,kug16]
    kut  =   [True,True,True,True,True,True,True,False,False,False,False,False,True,False,False,True]
    kuf  =   [color.YELLOW,color.BLUE,color.RED,color.VIOLET,color.ORANGE,color.DARK_GREEN,color.DARK_RED,color.ORANGE,color.YELLOW,color.BLUE,color.RED,color.VIOLET,color.BLACK,color.DARK_GREEN,color.DARK_RED,color.WHITE]
    kun  =   ["1","2","3","4","5","6","7","13","9","10","11","12","8","14","15","16"]
    
    pos=0
    posxy=0.35
    for i in kuli:
        #i.pos_x=posxy
        #i.pos_y=posxy
        i.full=kut[pos]
        i.colour=kuf[pos]
        i.number=kun[pos]
        if pos < 15:
            pos+=1
            posxy+=0.01
    kuli[15].pos_x=0.68
    kuli[15].pos_y=0.5
    
    kuli[0].pos_x=kuli[15].pos_x-0.3
    kuli[0].pos_y=kuli[15].pos_y
    
    #posxn=kuli[0].pos_x
    #posyn=kuli[0].pos_y
    
    
    for i in range(1,15):
        if i <5:
            kuli[i].pos_x=kuli[i-1].pos_x-2*kuli[i].rad
            kuli[i].pos_y=kuli[i-1].pos_y+kuli[i].rad
                              
        elif i < 9:
            kuli[i].pos_x=kuli[i-1].pos_x
            kuli[i].pos_y=kuli[i-1].pos_y-2*kuli[i].rad
            
            
        elif i < 12:
            kuli[i].pos_x=kuli[i-1].pos_x+2*kuli[i].rad
            kuli[i].pos_y=kuli[i-1].pos_y+kuli[i].rad
        

        elif i < 14:
            kuli[i].pos_x=kuli[i-1].pos_x-2*kuli[i].rad
            kuli[i].pos_y=kuli[i-1].pos_y+kuli[i].rad
        
        else:
            kuli[i].pos_x=kuli[i-1].pos_x
            kuli[i].pos_y=kuli[i-1].pos_y-2*kuli[i].rad
        
    return kuli


        
    
def collision(Kugel, field_x, field_y, field_width, field_height, const):
    """
    Überprüft die Kollision der Kugel mit den Banden.
    """
    field_x = field_x + const
    field_y = field_y + const
    field_width = field_width -2 * const
    field_height = field_height -2 * const

    #Bound up
    if Kugel.pos_x + 2.4*Kugel.rad >= field_x + field_width:
        Kugel.pos_x = Kugel.pos_x + (-Kugel.dir_x)
        Kugel.pos_y = Kugel.pos_y + (-Kugel.dir_y)
        
        Kugel.dir_x = Kugel.dir_x * (-1)
        Kugel.speed = float(Kugel.speed) * 0.7
       
    #Bound right
    elif Kugel.pos_y + 2.4*Kugel.rad >= field_y + field_height:
        Kugel.pos_x = Kugel.pos_x + (-Kugel.dir_x)
        Kugel.pos_y = Kugel.pos_y + (-Kugel.dir_y)
        
        Kugel.dir_y = Kugel.dir_y * (-1)
        Kugel.speed = float(Kugel.speed) * 0.7
        
    #Bound down
    elif Kugel.pos_x - 2.4*Kugel.rad <= field_x:
        Kugel.pos_x = Kugel.pos_x + (-Kugel.dir_x)
        Kugel.pos_y = Kugel.pos_y + (-Kugel.dir_y)
        
        Kugel.dir_x = Kugel.dir_x * (-1)
        Kugel.speed = float(Kugel.speed) * 0.7

    #Bound left
    elif Kugel.pos_y - 2.4*Kugel.rad <= field_y:
        Kugel.pos_x = Kugel.pos_x + (-Kugel.dir_x)
        Kugel.pos_y = Kugel.pos_y + (-Kugel.dir_y)
        
        Kugel.dir_y = Kugel.dir_y *(-1)
        Kugel.speed = float(Kugel.speed) * 0.7




def powerbar():
    draw.rectangle(0,0.9,0.5,0.1)
    f=0
    r=True
    while True:
        if draw.mousePressed():
            return f
        draw.filledRectangle(0,0.9,f,0.1)
        draw.show(20)
        if r:
            #f+=random.uniform(0.0,0.2)
            f+=0.02
        elif  r==False :
            #f-=random.uniform(0.0,0.2)
            f-=0.02
        
        if f>=0.5:
            f=0
            draw.setPenColor(color.WHITE)
            draw.filledRectangle(0,0.9,0.5,0.1)
            draw.setPenColor(color.BLACK)
            draw.rectangle(0,0.9,0.5,0.1)
     
        

def move(Kugel, fxpos, fypos, fwidth, fheight, const):
    """
    Zuständig für die bewegung der Kugel.
    """
    fxpos = fxpos + const
    fypos = fypos + const
    #midf = (fxpos + fwidth/2, fypos + fheight/2)
    kupo = (Kugel.pos_x, Kugel.pos_y)
    dirx = 1
    diry = 1
    px=0
    py=0
    
    if draw.mousePressed():
        
       mopo = draw.mousePosition()
       #print(kupo, mopo)
       
       #Direction
       if mopo[0] > kupo[0]:
           pass
       elif mopo[0] < kupo[0]:
           dirx *= -1
           
       if mopo[1] > kupo[1]:
           pass
       elif mopo[1] < kupo[1]:
           diry *= -1
       
       #Strength
       px = abs(kupo[0] - mopo[0])/10
       py = abs(kupo[1] - mopo[1])/10
       if px > 0.021:
           px=0.021
       if py > 0.021:
           py=0.021
       #px=0.001
       #py=0.001
       #print(dirx,diry)
       Kugel.dir_x = dirx * px * (Kugel.power)
       Kugel.dir_y = diry * py * (Kugel.power)

def hocol(Kugel, field_x, field_y, field_width, field_height, const):
    
    """
    Überprüft ob die Kugel das Feld verlässt.
    """
    
    
    holed=False
    field_x = field_x + const
    field_y = field_y + const
    field_width = field_width -2 * const
    field_height = field_height -2 * const
    """
    #hole down left
    draw.filledPolygon([field_x+const*3,field_x],[field_y,field_y+const*3])
    #hole down right
    draw.filledPolygon([field_x+field_width-const*3,field_x+field_width],[field_y,field_y+const*3])
    #hole up left
    draw.filledPolygon([field_x+const*3,field_x],[field_y+field_height,field_y+field_height-const*3])
    #Hole up right
    draw.filledPolygon([field_x+field_width-const*3,field_x+field_width],[field_y+field_height,field_y+field_height-const*3])
    """
    #hole mid up
    if Kugel.pos_y + Kugel.rad >= field_y + field_height and Kugel.pos_x-Kugel.rad > field_x + (field_width/2) - const and Kugel.pos_x+Kugel.rad < field_x + (field_width/2) + const:
        #print("UP")
        if Kugel.number!="16":
            Kugel.infield=False
        holed=True
        
        
    #hole mid down
    elif Kugel.pos_y - Kugel.rad <= field_y and Kugel.pos_x-Kugel.rad > field_x + (field_width/2) - const and Kugel.pos_x+Kugel.rad < field_x + (field_width/2) + const:
        #print("DOWN")
        if Kugel.number!="16":
            Kugel.infield=False
        holed=True
    
    #hole left up
    kx=Kugel.pos_x-Kugel.rad
    ky=Kugel.pos_y+Kugel.rad
    
    linex=0.13#field_x+const #(fx + const*3 + fx )/2
    liney=0.67#field_y + field_height - const #(fy+field_height-const*3 + fy+field_height)**2
    if kx < linex and ky > liney:
            #print("LEFT UP")
            if Kugel.number!="16":
                Kugel.infield=False
            holed=True

    #hole right up
    kx=Kugel.pos_x+Kugel.rad
    ky=Kugel.pos_y+Kugel.rad
    
    linex=0.87
    liney=0.67
    if kx > linex and ky > liney:
            #print("RIGHT UP")
            if Kugel.number!="16":
                Kugel.infield=False
            holed=True
            
    #hole left down
    kx=Kugel.pos_x-Kugel.rad
    ky=Kugel.pos_y-Kugel.rad
    
    linex=0.13
    liney=0.33
    if kx < linex and ky < liney:
            #print("LEFT DOWN")
            if Kugel.number!="16":
                Kugel.infield=False
            holed=True
            
    #hole right down
    kx=Kugel.pos_x+Kugel.rad
    ky=Kugel.pos_y-Kugel.rad
    
    linex=0.87
    liney=0.33
    if kx > linex and ky < liney:
            #print("RIGHT DOWN")
            if Kugel.number!="16":
                Kugel.infield=False
            holed=True
    
    #ball in hole
    if holed and Kugel.number!="16":
        
        if Kugel.full:
            Kugel.dir_x=0
            Kugel.dir_y=0
            Kugel.pos_x=0.2
            Kugel.pos_y=Kugel.fout
            kugel.Kugel.fout+=Kugel.rad*2
        else:
            Kugel.dir_x=0
            Kugel.dir_y=0
            Kugel.pos_x=0.8
            Kugel.pos_y=Kugel.hout
            kugel.Kugel.hout+=Kugel.rad*2
        #print(Kugel.fout, Kugel.hout)
            
    elif holed and Kugel.number=="16":
        
        Kugel.dir_x=0
        Kugel.dir_y=0
        Kugel.infield=False
        
        Kugel.pos_x=0.0
        Kugel.pos_y=0.0

        
        
def whipo(Kugel, field_y, field_height,const, kugelListe):
    """
    Setzt Position der weißen Kugel nachdem sie das Feld verlassen hat
    per Mausklick
    """
    #TODO: redraw stuff, background too. Set x as max btw 0.68 and ...
    
    x=0.68
    y=0

    waiting_for_mouse = True
    while waiting_for_mouse:
        x_=draw.mousePosition()[0]
        y=draw.mousePosition()[1]
        ######################################################################
        table(0.1, 0.3, 0.8, 0.4, 0.02)
        ######################################################################
        draw.filledCircle(x_, y, 0.005)
        for i in kugelListe:
            i.displ()
        #print(draw.mousePosition())
        
        draw.show(1/60)
        
        if draw.mousePressed():
            if draw.mousePosition()[1] > field_y+const and draw.mousePosition()[1] < field_y+field_height-const:
                Kugel.pos_x=max(x, draw.mousePosition()[0])
                Kugel.pos_y=y
                Kugel.infield=True
                waiting_for_mouse = False
    
        
def rest(li):
    """
    Überprüft ob die Kugeln in Ruhe sind
    """
    
    for i in li:
        if i.dir_x!=0 or i.dir_y!=0:
            return False
    return True

def queue(Kugel):
    """
    Zeigt die Aufladung des Schusses
    """
    f=0
    mx,my=draw.mousePosition()
    if mx < Kugel.pos_x:
        mx=Kugel.pos_x+(max(mx,Kugel.pos_x)-min(mx,Kugel.pos_x))
    else:
        mx=Kugel.pos_x-(max(mx,Kugel.pos_x)-min(mx,Kugel.pos_x))
        
    if my < Kugel.pos_y:
        my=Kugel.pos_y+(max(my,Kugel.pos_y)-min(my,Kugel.pos_y))
    else:
        my=Kugel.pos_y-(max(my,Kugel.pos_y)-min(my,Kugel.pos_y))
    draw.rectangle(0,0.98,0.21,0.02)
    draw.rectangle(0,0.98,0.07,0.02)
    draw.rectangle(0,0.98,0.14,0.02)
    ql= math.sqrt((Kugel.pos_x - mx)**2 + (Kugel.pos_y - my)**2)
    draw.setPenColor(color.DARK_GREEN)
    draw.setFontSize(20)
    if ql < 0.21:
        draw.text(0.1,0.95,"{}".format(ql))
    draw.setFontSize(10)
    if ql <0.21:
        
        draw.setPenColor(color.BLUE)
        draw.setPenRadius(0.003)
        draw.line(Kugel.pos_x, Kugel.pos_y, mx, my)
        draw.setPenColor(color.WHITE)
        draw.filledCircle(Kugel.pos_x, Kugel.pos_y,Kugel.rad)
        if ql<=0.07:
            draw.setPenColor(color.GREEN)
            f=2
        elif ql<=0.14:
            draw.setPenColor(color.YELLOW)
            f=4
        elif ql >0.14 and ql <=0.21:
            draw.setPenColor(color.RED)
            f=16
        else:
            f=0
        draw.filledRectangle(0,0.98,ql,0.02)
        draw.setPenColor(color.BLACK)
        draw.rectangle(0,0.98,0.21,0.02)
        draw.rectangle(0,0.98,0.07,0.02)
        draw.rectangle(0,0.98,0.14,0.02)
    if draw.hasNextKeyTyped():
        Kugel.power=ql*f
        #print(Kugel.power)
        if draw.mousePressed():
            draw.nextKeyTyped()

def game_standing(fullplayer, halfplayer, fullout, halfout, kugeli, p):
    """
    Gibt den Stand des Spiels aus.
    """
    print(p)
    if p == 0:
        draw.setFontSize(13)
        draw.text(0.5, 0.5, "PLAYER 1")
    elif p == 1:
        draw.setFontSize(13)
        draw.text(0.5, 0.5, "PLAYER 2")
    
    
    draw.text(0.2,0.72,"Player {} Full balls out: {}".format(fullplayer,fullout))
    draw.text(0.8,0.72,"Player {} Half balls out: {}".format(halfplayer,halfout))
    #print(fullplayer,p)
    #print(fullout,halfout)
    if kugeli[12].infield == False and fullout==7 and fullplayer%2 == p:
        #print("PLAYER full WINS")
        draw.text(0.5,0.75,"PLAYER {} WINS".format(p if p ==1 else 2))
        #draw.text(0.5,0.75,"WINNER: ")
    elif kugeli[12].infield == False and halfout==7 and halfplayer%2 == p:
        #draw.text(0.5,0.75,"WINNER: ")
        draw.text(0.5,0.75,"PLAYER {} WINS".format(p if p ==1 else 2))
        #print("PLAYER half WINS")
    elif kugeli[12].infield == False:
            draw.text(0.5,0.75,"PLAYER {} LOSES".format(p if p ==1 else 2))


def ball_handling(kugelListe, lfo, lho, fullplayer, halfplayer, p, rect_x, rect_y, rect_width, rect_height, const):
    
    for i in kugelListe:
        i.displ()
        i.nextPos()


        for j in kugelListe:
            if i!=j:
                if i.kabstk2rad(j):
                    i.kukol(j)
                    collision(i, 0.1, 0.3, 0.8, 0.4, 0.002)
        hocol(i, 0.1, 0.3, 0.8, 0.4, 0.02)
        collision(i, 0.1, 0.3, 0.8, 0.4, 0.002)
    #draw.show(1/61)
    if kugelListe[15].infield==False and rest(kugelListe):
        kugelListe[15].infield=True
        whipo(kugelListe[15],0.3,0.4,0.02, kugelListe)

    if rest(kugelListe):
        queue(kugelListe[15])
        #draw.show(1/61)
        move(kugelListe[15], rect_x, rect_y, rect_width, rect_height, const)
        #if kugelListe[12].infield == False:
         #       print("PLAYER{} LOSES").format(p+1)
        
        if kugelListe[15].dir_x !=0 or kugelListe[15].dir_y != 0:
            #if kugelListe[12].infield == False and player.type
            #TODO here?
            p = (p+1)%2
            #print(p)
        
    
    fullout=0
    halfout=0
    
    for i in kugelListe:
        if not i.infield and i.full:
            fullout+=1
            
        elif not i.infield and not i.full:
            halfout+=1
            
    if lfo==0 and fullout>0 and fullplayer=="??? ":
        fullplayer=p+2 if p%2==0 else p
        halfplayer=p+1%2
        
    elif lho==0 and halfout>0 and fullplayer=="??? ":
        halfplayer=p+2 if p%2==0 else p
        fullplayer=p+1%2
    
    if lho < halfout:
        lho=halfout
    if lfo < fullout:
        lfo=fullout
    
    return lfo, lho, fullplayer, halfplayer, p