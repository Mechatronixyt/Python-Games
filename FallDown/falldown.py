import sys
import pygame
 
screenx = 500
screeny = 800
 
go = True
speed = 0
 
playerx = 40
playery = 540
 
#zuerst xanfang dann xende
gap = [100,300,220,400,40,200,150,300,260,400,164,300,268,400,122,250,76,200,300,420,200,316,260,372,370,478,90,194,200,300,350,448,168,264]
 
coordx = [0,300,0,400,0,200,0,300,0,400,0,300,0,400,0,250,0,200,0,420,0,316,0,372,0,478,0,194,0,300,0,448,0,264]
coordy = [-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250,-250]
length = [120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120]
width = [100,200,220,100,40,300,150,200,260,100,164,200,268,100,122,250,76,300,300,80,200,184,260,128,370,22,90,306,200,200,350,52,168,236]
 
loops = 0
z = 2
 
lastround = 0
little = 0
 
wallcount = 0
points = 0
 
pygame.init()
screen = pygame.display.set_mode([screenx,screeny])
screen.fill((0,0,0))
clock = pygame.time.Clock()
playerimg = pygame.image.load("player.png")
font = pygame.font.SysFont(None,60)
little = int(len(coordy)/2)-2
 
def punkte(punkte):
    text = font.render(punkte, True, (255,255,255))
    screen.blit(text, (255,50))
 
def drawer():
    for i in range(len(coordy)):
        pygame.draw.rect(screen, (255,0,60), (coordx[i],coordy[i],width[i],length[i]), 0)
 
def mover():
    global z,coordy,coordx,length,width,lastround,gap
    if loops % 300 == 0 and lastround <= little:
        z = z+2
    for x in range(z):
        if coordy[x] > screeny+20:
            z -= 2
            lastround = lastround+1
            coordy.pop(1)
            coordy.pop(0)
            coordx.pop(1)
            coordx.pop(0)
            gap.pop(1)
            gap.pop(0)
            width.pop(1)
            width.pop(0)
            length.pop(1)
            length.pop(0)
            break
        else:
            coordy[x] += 2
 
def collisiondetection():
    global go,wallcount,points
    #player is at the left or the right wall
    if playerx <= 0 or playerx+40 >= screenx:
        go = False
    #player hits an obstacle
    if len(coordy) > 0:
        if coordy[0] >= 420 and coordy[0] <= 640:
            wallcount += 1
            if wallcount > 109:
                points += 1
                wallcount = 0
            if playerx <= gap[0] or playerx+40 >= gap[1]:
                go = False
 
while go == True:
    loops += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = -2
            if event.key == pygame.K_RIGHT:
                speed = 2
            if event.key == pygame.K_q:
                sys.exit()
    screen.fill((0,0,0))
    playerx += speed
    screen.blit(playerimg, (playerx,playery))
    mover()
    pygame.draw.lines(screen, (0,0,255), False, [(0,640),(500,640)], 1)
    drawer()
    collisiondetection()
    punkte(str(points))
    pygame.display.flip()
    clock.tick(100)
 
print ("Dein Score Ist " + str(points))
pygame.time.wait(3000)