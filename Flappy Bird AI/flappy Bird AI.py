import pygame
import sys
import numpy as np
import random
import matplotlib.pyplot as plt
from math import sqrt
 
#Parameter Anfang
#Eingabeneuronen, fix
iN = 3
#versteckte Neuronen
hN = 2
#Ausgabeneuronen, fix
oN = 1
mutationsChance = 10
mutationsAbweichung = 0.25
populationSize = 100
lvl_lenght = 20000
fps = 60
#Ob alle 20 Generationen ein Diagramm angezeigt werden soll
Graph = True
#Parameter Ende
 
screenX = 1100
screenY = 900
 
pygame.init()
screen = pygame.display.set_mode([screenX,screenY])
pygame.display.set_caption('Flappy AI')
screen.fill((0,0,0))
clock = pygame.time.Clock()
vogel = pygame.image.load("flappyduck2.png")
 
go = True
gravity = 13.7
obstacles = []
obstaclesX = []
dicke = 60
currentIndex = 0
plotList = []
plotList2 = []
plotCounter = 0
passedX = 0
games = []
population = []
birds = []
average = 0
 
class Netz:
    def __init__(self,iN,hN,oN):
        self.inputNodes = iN
        self.hiddenNodes = hN
        self.outputNodes = oN
 
        self.bias = np.zeros(self.hiddenNodes)
        self.wHin = np.zeros((self.inputNodes,self.hiddenNodes))
        self.wHout = np.zeros((self.hiddenNodes,self.outputNodes))
        self.randomizer()
 
    def randomizer(self):
        #wHin
        for n in range(0,self.inputNodes):
            for j in range(0,self.hiddenNodes):
                self.wHin[n][j] = random.uniform(-1,1)
        #wHout
        for n in range(0,self.hiddenNodes):
            for j in range(0,self.outputNodes):
                self.wHout[n][j] = random.uniform(-1,1)
        #bias
        for x in range(0,self.hiddenNodes):
            self.bias[x] = 0.0
 
    def sigmoid_array(self,x):
        return 1 / (1 + np.exp(-x))
 
    def weight_Multiply(self,w,a):
        return w*a
 
    def arraySum(self,x):
        return x.sum(axis=0)
 
    def rounder(self,x):
        return np.around(x,5)
 
    def wHinGeben(self):
        return self.wHin
 
    def wHinSetzen(self,neu):
        self.wHin = neu
 
    def wHoutGeben(self):
        return self.wHout
 
    def wHoutSetzen(self,neu):
        self.wHout = neu
 
    def biasGeben(self):
        return self.bias
 
    def biasSetzen(self,neu):
        self.bias = neu
 
    def go(self,distances):
        inputOutput = np.array(self.rounder(self.sigmoid_array(self.arraySum(self.weight_Multiply(self.wHin,distances))+self.bias)))
        #Dimensionskonvertierung
        inputOutputRD = np.reshape(inputOutput,(-1,1))
        #letzte Schicht
        outputOutput = np.array(self.rounder(self.sigmoid_array(self.arraySum(self.weight_Multiply(self.wHout,inputOutputRD)))))
        if outputOutput[0] >= 0.5:
            return True
        else:
            return False
 
 
 
class bird:
    def __init__(self,startX,startY,netI):
        self.x = startX
        self.y = startY
        self.sizeX = 40
        self.sizeY = 30
        self.jumpPower = 42
        self.jumpVal = 0
        self.alive = True
        self.fitness = 0.0
        self.netInd = netI
    def move(self):
        global passedX
        if self.alive:
            self.y += gravity
            self.y -= self.jumpVal
            if self.jumpVal > 0:
                self.jumpVal -= 3
            if self.y < 50:
                self.y = 51
                self.jumpVal = 0
            elif self.y+self.sizeY > screenY-50:
                self.y = screenY-50-self.sizeY-1
            self.fitness = passedX
    def jump(self):
        self.jumpVal = self.jumpPower
    def draw(self):
        screen.blit(vogel,(self.x,self.y))
    def positionGeben(self):
        return [self.x,self.y,self.sizeX,self.sizeY]
    def neuralInputGeben(self):
        nI = []
        nI.append(self.y+(self.sizeY/2))
        mitteRechtsX = self.x+self.sizeX
        mitteRechtsY = self.y+(self.sizeY/2)
        dist = sqrt((obstaclesX[currentIndex]-mitteRechtsX)**2+(obstacles[currentIndex][0]-mitteRechtsY)**2)
        dist2 = sqrt((obstaclesX[currentIndex]-mitteRechtsX)**2+(obstacles[currentIndex][1]-mitteRechtsY)**2)
        nI.append(dist)
        nI.append(dist2)
        return np.array([[nI[0]],[nI[1]],[nI[2]]])
 
 
 
 
def hindernisGenerator(length):
    global obstacles,obstaclesX
    luecke = 254
    for i in range(0,length):
        rand = random.randint(175,screenY-175-50-luecke)
        unten = rand+luecke
        obstacles.append([rand,unten])
    x = 500
    for i in range(0,len(obstacles)):
        obstaclesX.append(x)
        x += 280
 
def hindernisManager():
    global obstacles,obstaclesX,currentIndex,passedX
    for n in range(0,len(obstaclesX)):
        if obstaclesX[n]>=-4:
            obstaclesX[n] -= 5
        if n == 1:
            passedX += 5
    for o in range(0,len(obstacles)):
        if obstaclesX[o] < 650 and obstaclesX[o] > 50:
            if obstaclesX[o] < 650-dicke:
                pygame.draw.rect(screen, (255,0,0), (obstaclesX[o],51,dicke,obstacles[o][0]-51), 0)
                pygame.draw.rect(screen, (255,0,0), (obstaclesX[o],obstacles[o][1],dicke,screenY-51-obstacles[o][1]), 0)
            else:
                pygame.draw.rect(screen, (255,0,0), (obstaclesX[o],51,650-obstaclesX[o],obstacles[o][0]-51), 0)
                pygame.draw.rect(screen, (255,0,0), (obstaclesX[o],obstacles[o][1],650-obstaclesX[o],screenY-51-obstacles[o][1]), 0)
            if obstaclesX[o] >= 240 and obstaclesX[o] <= 460:
                currentIndex = o
        elif obstaclesX[o] <= 50 and obstaclesX[o]>-4:
            pygame.draw.rect(screen, (255,0,0), (51,51,obstaclesX[o],obstacles[o][0]-51), 0)
            pygame.draw.rect(screen, (255,0,0), (51,obstacles[o][1],obstaclesX[o],screenY-51-obstacles[o][1]), 0)
 
def collision(b):
    a = [False,False]
    if b.x < obstaclesX[currentIndex] + dicke and b.x + b.sizeX > obstaclesX[currentIndex] and b.y < obstacles[currentIndex][0] and b.y + b.sizeY > 51:
        a[0] = True
    if b.x < obstaclesX[currentIndex] + dicke and b.x + b.sizeX > obstaclesX[currentIndex] and b.y < obstacles[currentIndex][1] + 851-obstacles[currentIndex][1] and b.y + b.sizeY > obstacles[currentIndex][1]:
        a[1] = True
    return a
 
 
 
def textObjekt(text,font):
    textFlaeche = font.render(text, True,(255,255,255))
    return textFlaeche,textFlaeche.get_rect()
 
def modelDrawer(mX,mY):
    #hN
    currentCircleY = 0
    parts = 0
    parts = int(120/(hN-1))
    if hN == 2:
        parts = 70
        currentCircleY = 25
    for i in range(0,hN):
        pygame.draw.aaline(screen, (0,0,255), (mX+20,mY+20), (mX+165,currentCircleY+20+mY))
        pygame.draw.aaline(screen, (0,0,255), (mX+20,mY+80), (mX+165,currentCircleY+20+mY))
        pygame.draw.aaline(screen, (0,0,255), (mX+20,mY+140), (mX+165,currentCircleY+20+mY))
        pygame.draw.aaline(screen, (0,0,255), (mX+165,currentCircleY+mY+20), (mX+310,mY+80))
        pygame.draw.circle(screen, (255,255,0), (mX+170,currentCircleY+20+mY), 12)
        currentCircleY += parts
    #iN
    pygame.draw.circle(screen, (255,255,0), (mX+20,mY+20), 12)
    pygame.draw.circle(screen, (255,255,0), (mX+20,mY+80), 12)
    pygame.draw.circle(screen, (255,255,0), (mX+20,mY+140), 12)
    #oN
    pygame.draw.circle(screen, (255,255,0), (mX+310,mY+80), 12)
 
 
 
 
def schriftzuege(gen,highscore,aliveOnes):
    font = pygame.font.SysFont('arialblack',38)
    textGrund,textKasten = textObjekt("Generation: "+str(gen),font)
    textKasten.center = ((875,55+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY = textKasten.height+55+5
    textGrund,textKasten = textObjekt("Lebend: "+str(aliveOnes) + "/" + str(populationSize),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Score: "+str(passedX),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    font = pygame.font.SysFont('arialblack',33)
    curTextY += textKasten.height+5
    if passedX > highscore:
        textGrund,textKasten = textObjekt("Highscore: "+str(passedX),font)
    else:
        textGrund,textKasten = textObjekt("Highscore: "+str(highscore),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Mittel: "+str(round(average)),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Mutationsrate: "+str(mutationsChance)+"%",font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Levellänge: "+str(lvl_lenght),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Inputneurons: "+str(iN),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Hiddenneurons: "+str(hN),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    textGrund,textKasten = textObjekt("Outputneurons: "+str(oN),font)
    textKasten.center = ((875,curTextY+(textKasten.height/2)))
    screen.blit(textGrund,textKasten)
    curTextY += textKasten.height+5
    modelDrawer(710,curTextY+10)
 
 
 
 
An = True
go = True
iterations = 0
highscore = 0
 
def gameloop(gen):
    global screen,birds,go,iterations,currentIndex
    aliveCount = 0
    currentIndex = 0
    while go and iterations>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,255,255), (50,50,600,screenY-100), 1)
        pygame.draw.rect(screen, (255,255,255), (700,50,350,screenY-100), 1)
        hindernisManager()
        schriftzuege(gen,highscore,aliveCount)
        aliveCount = 0
        
        for i in birds:
            col = collision(i)
            if col[0] or col[1]:
                i.x = -100
                i.y = -100
                i.alive = False
 
        testVar = False
        for x in range(0,len(birds)):
            if birds[x].alive:
                aliveCount+=1
                testVar = True
        if testVar == False:
            go = False
        
        for b in birds:
            if b.alive and go:
                pygame.draw.aaline(screen, (0,0,255), (b.x+b.sizeX,b.y), (obstaclesX[currentIndex],obstacles[currentIndex][0]))
                pygame.draw.aaline(screen, (0,0,255), (b.x+b.sizeX,b.y+b.sizeY), (obstaclesX[currentIndex],obstacles[currentIndex][1]))
                b.move()
                b.draw()
 
        
 
        for n in range(0,len(birds)):
            boolVar = population[n].go(birds[n].neuralInputGeben())
            if boolVar:
                birds[n].jump()
        if go:
            pygame.display.update()
        iterations -= 1
        clock.tick(fps)
 
 
def erzeugePopulation(anzahlIndividuen,iN,hN,oN):
    global population,birds
    for x in range(0,anzahlIndividuen):
        population.append(Netz(iN,hN,oN))
        birds.append(bird(240,400,x))
 
def maxAndInd(ueListe):
    maxVal = max(ueListe)
    index = 0
    finInd = 0
    for x in ueListe:
        if x == maxVal:
            finInd = index
            break
        index += 1
    return finInd
 
def sumUp(arrSc):
    valueSc = 0
    for x in arrSc:
        valueSc += x
    return valueSc
 
def fittestSelector(count):
    global plotList,plotList2,plotCounter,highscore,average
    fitness = []
    uebergabe = []
    for g in birds:
        fitness.append(g.fitness)
    maximum = max(fitness)
    if maximum > highscore:
        highscore = maximum
    average = sumUp(fitness)/populationSize
    plotList.append(sumUp(fitness))
    plotList2.append(sumUp(fitness))
    over = np.linspace(0,len(plotList),num=len(plotList))
    if len(plotList) % 20 == 0 and Graph:
        plt.plot(over, plotList)
        plt.axis([0, max(over), 0, max(plotList)])
        plt.show()
    while len(uebergabe) < count:
        maxInd = maxAndInd(fitness)
        uebergabe.append(population[maxInd])
        fitness[maxInd] = 0
    return uebergabe
 
 
def zufallsArray(count1,count2):
    zA = []
    for x in range(0,int((count1*count2))):
        zA.append(random.randint(0,1))
    return zA
 
def crossover(x,y):
    #x und y sind gleich große 2d numpy arrays
    neu = []
    shapeX = x.shape[0]
    shapeY = x.shape[1]
    zA = zufallsArray(shapeX,shapeY)
    index = 0
    for i in range(0,shapeX):
        for j in range(0,shapeY):
            if zA[index] == 0:
                neu.append(x[i][j])
            else:
                neu.append(y[i][j])
            index += 1
    retNeu = np.reshape(neu,(shapeX,shapeY))
    return retNeu
 
def biasCrossover(x,y):
    #x und y sind gleich große numpy arrays 1D
    neu = []
    length = x.size
    zA = zufallsArray(length,1)
    index = 0
    for i in range(0,length):
        if zA[index] == 0:
            neu.append(x[i])
        else:
            neu.append(y[i])
        index += 1
    retNeu = np.reshape(neu,(length))
    return retNeu
 
def zufallsArrayMutation(count):
    zA = []
    index = 0
    for x in range(0,count):
        randNr = random.randint(1,100)
        zA.append(randNr)
    return zA
 
def mutation(Array):
    neu = []
    zM = zufallsArrayMutation(Array.size)
    shapeX = Array.shape[0]
    shapeY = Array.shape[1]
    shape = Array.shape
    index = 0
    for i in range(0,shapeX):
        for j in range(0,shapeY):
            if zM[index] <= mutationsChance:
                rand = random.uniform(-mutationsAbweichung,mutationsAbweichung)
                neu.append(rand)
            else:
                neu.append(0.0)
            index += 1
    add1 = np.reshape(Array,(Array.size,1))
    add2 = np.reshape(neu,(Array.size,1))
    retA = add1+add2
    retAFinal = np.reshape(retA,shape)
    return retAFinal
 
def biasMutation(Array):
    neu = []
    zM = zufallsArrayMutation(Array.size)
    length = Array.size
    index = 0
    for i in range(0,length):
        if zM[index] <= mutationsChance:
            #rand = random.uniform(-mutationsAbweichung,mutationsAbweichung)
            neu.append(index)
        index += 1
    add1 = np.reshape(Array,(length))
    #add2 = np.reshape(neu,(Array.size,1))
    for z in neu:
        add1[z] = random.uniform(-1,1)
    #retA = add1+add2
    retAFinal = np.reshape(add1,(length))
    return retAFinal
 
def mutierterNachkomme(Vater,Mutter):
    wHinElternteil1 = Vater.wHinGeben()
    wHinElternteil2 = Mutter.wHinGeben()
    wHoutElternteil1 = Vater.wHoutGeben()
    wHoutElternteil2 = Mutter.wHoutGeben()
    biasElternteil1 = Vater.biasGeben()
    biasElternteil2 = Mutter.biasGeben()
 
    wHinNeu = crossover(wHinElternteil1,wHinElternteil2)
    wHoutNeu = crossover(wHoutElternteil1,wHoutElternteil2)
    biasNeu = biasCrossover(biasElternteil1,biasElternteil2)
 
    wHinNeu = mutation(wHinNeu)
    wHoutNeu = mutation(wHoutNeu)
    biasNeu = biasMutation(biasNeu)
 
    neuesNet = Netz(iN,hN,oN)
    neuesNet.wHinSetzen(wHinNeu)
    neuesNet.wHoutSetzen(wHoutNeu)
    neuesNet.biasSetzen(biasNeu)
    return neuesNet
 
def neuePopulation():
    fittest = []
    neuPopList = []
    ueData = fittestSelector(5)
    for x in ueData:
        fittest.append(x)
    while len(neuPopList) < populationSize:
        rand1 = random.randint(0,4)
        rand2 = random.randint(0,4)
        neuPopList.append(mutierterNachkomme(fittest[rand1],fittest[rand2]))
    return neuPopList
 
 
 
 
def trainProcess(its):
    global birds,population,go,iterations,obstacles,obstaclesX,passedX
    erzeugePopulation(populationSize,iN,hN,oN)
    indIt = 1
    while indIt < its:
        go = True
        obstacles = []
        obstaclesX = []
        passedX = 0
        iterations = 4000
        hindernisGenerator(200)
        gameloop(indIt)
        nPopUe = neuePopulation()
        population = []
        for u in nPopUe:
            population.append(u)
        birds = []
        for h in range(0,populationSize):
            birds.append(bird(240,400,h))
        indIt += 1
 
trainProcess(lvl_lenght)