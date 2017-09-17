import time, random
from Classes import *
import pygame
pygame.init()


surface = pygame.display.set_mode((1400,600),0,32)
pygame.display.set_caption("Earth Invaders")
 
XMOVE = 100
 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)



#Sets a "Space Invaders" title for the window
myFont = pygame.font.SysFont("monospace", 20)
instruction = pygame.font.SysFont("monospace",20)
scoreFont = pygame.font.SysFont ("monospace",20)
endGameFont = pygame.font.SysFont ("monospace", 20)
title = myFont.render("Earth Invaders",1,BLACK)
endGameTitle = myFont.render("Game Over",1,BLACK)
closeGame = myFont.render ("Press Escape to close",1,BLACK)
 

enemsList1 = pygame.sprite.Group() #Creating 5 groups for 5 different tiered enemies.
enemsList2 = pygame.sprite.Group()
enemsList3 = pygame.sprite.Group()
enemsList4 = pygame.sprite.Group()
enemsList5 = pygame.sprite.Group()

enemBulletGroup = pygame.sprite.Group() #Group for the enemy bullets.
friendlyGroup = pygame.sprite.Group() #Group for the friendly spaceship.
bulletGroup = pygame.sprite.GroupSingle() #Single group for the friendly bullet.
livesGroup = pygame.sprite.Group()


badShipList = [] #List of groups of ships.

def mainMenu() : 
    class Option (object) :
        hovered = False

        def __init__(self, text, pos) :
            self.text = text
            self.pos = pos
            self.set_rect()
            self.draw()

        def draw(self) :
            self.set_rend()
            screen.blit(self.rend, self.rect)

        def set_rend(self) :
            self.rend = menu_font.render(self.text, True, self.get_colour())

        def get_colour(self) :
            if self.hovered :
                return (0, 255, 0)
            else :
                return (255, 255, 255)

        def set_rect(self) :
            self.set_rend()
            self.rect = self.rend.get_rect()
            self.rect.topleft = self.pos

        def is_clicked(self) :
            return self.text

    def menuClicked(userSel) :
        print (userSel)
        if userSel == "NEW GAME" :
            playGame()
        elif userSel == "HIGH SCORES" :
            highScores()
        elif userSel == "CONTROLS" :
            controls()
        elif userSel == "BACK" :
            return True
        else :
            print ("What the hell happened...")

    #Initial setting up
    screen = pygame.display.set_mode((450, 600))
    menu_font = pygame.font.Font(None, 40)
    options = [Option("NEW GAME", (150, 400)), Option("HIGH SCORES", (137, 450)), Option("CONTROLS", (145, 500))]
    bg = pygame.image.load("bgMenu.png")
    pygame.display.set_caption("Earth Invaders - Menu")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    myfont = pygame.font.Font(None, 50)


    #---------------- HIGH SCORES -------------------#

    def highScores() :
        #Setting up initial display variables
        userBack = False
        screen = pygame.display.set_mode((450, 600))
        menu_font = pygame.font.Font(None, 40)
        options = [Option("BACK", (187, 550))]
        bg = pygame.image.load("bgMenu.png")
        pygame.display.set_caption("Earth Invaders - High Scores")
        scoreFont = pygame.font.Font(None, 30)
        displayTitle = myfont.render("HIGH SCORES", 1, (255, 255, 255))

        #Importing highscores from file & Displaying
        highScoreFile = open("high_score.txt", "r")


        highScores = []
        while True :
            currentScore = str.strip(highScoreFile.readline())
            if currentScore == "" :
                break
            highScores.append(int(currentScore))
        highScores.sort(reverse=True)
        
        highScoresLeft = highScores[0:12]
        highScoresRight = highScores[12:24]
            
        #Loop to check if user wants to return & highlight text
        def displayScores() :
            counting = 0
            counting2 = 0
            for i in highScoresLeft :
                counting += 1
                displayScore = scoreFont.render(str(i), 1, (255, 255, 255))
                screen.blit(displayScore, (115, 75+(counting*35)))
            for i in highScoresRight :
                counting2 += 1
                displayScore = scoreFont.render(str(i), 1, (255, 255, 255))
                screen.blit(displayScore, (315, 75+(counting2*35)))
                
        while userBack == False :
            pygame.event.pump()
            screen.blit(bg, (0,0))
            screen.blit(displayTitle, (110, 50))
            displayScores()
            
            for option in options :
                if option.rect.collidepoint(pygame.mouse.get_pos()) :
                    option.hovered = True
                    if pygame.mouse.get_pressed() == (1,0,0):
                        userSel = option.is_clicked()
                        if menuClicked(userSel) == True :
                            userBack = True
                else :
                    option.hovered = False
                option.draw()    
            pygame.display.update()


    #----------- CONTROLS---------------#

    def controls() :
        #Setting up initial display variables
        userBack = False
        screen = pygame.display.set_mode((450, 600))
        menu_font = pygame.font.Font(None, 40)
        options = [Option("BACK", (187, 550))]
        bg = pygame.image.load("bgMenu.png")
        pygame.display.set_caption("Earth Invaders - Controls")
        scoreFont = pygame.font.Font(None, 30)
        displayTitle = myfont.render("CONTROLS", 1, (255, 255, 255))
        control1 = instruction.render("LEFT ARROW TO MOVE LEFT", 1, (255, 255, 255))
        control2 = instruction.render("RIGHT ARROW TO MOVE RIGHT", 1, (255, 255, 255))
        control3 = instruction.render("SPACE TO SHOOT", 1, (255, 255, 255))
        control1Rect = control1.get_rect(center=(225,200))
        control2Rect = control2.get_rect(center=(225,250))
        control3Rect = control3.get_rect(center=(225,350))
        while userBack == False :

            pygame.event.pump()
            screen.blit(bg, (0,0))
            screen.blit(control1,control1Rect)
            screen.blit(control2,control2Rect)
            screen.blit(control3,control3Rect)
            screen.blit(displayTitle, (110, 50))
            
            
            for option in options :
                if option.rect.collidepoint(pygame.mouse.get_pos()) :
                    option.hovered = True
                    if pygame.mouse.get_pressed() == (1,0,0):
                        userSel = option.is_clicked()
                        if menuClicked(userSel) == True :
                            userBack = True
                else :
                    option.hovered = False
                option.draw()    
            pygame.display.update()

    #---------------------- MENU ----------------------#
    def menu() : 
        #Setting the rest of the neccesary stuff up
        options = [Option("NEW GAME", (150, 400)), Option("HIGH SCORES", (137, 450)), Option("CONTROLS", (145, 500))]
        bg = pygame.image.load("bgMenu.png")
        pygame.display.set_caption("Earth Invaders - Menu")
        displayTitle = myfont.render("SPACE INVADERS", 1, (255, 255, 255))
        mob1 = pygame.image.load("redShip.png")
        mob1 = pygame.transform.scale(mob1, (42, 45))
        mob2 = pygame.image.load("blackShip.png")
        mob2 = pygame.transform.scale(mob2, (42, 45))
        mob3 = pygame.image.load("brownShip.png")
        mob3 = pygame.transform.scale(mob3, (42, 45))
        mob4 = pygame.image.load("darkship.png")
        mob4 = pygame.transform.scale(mob4, (42, 45))

        while True :
            pygame.event.pump()
            screen.blit(bg, (0,0))
            screen.blit(displayTitle, (70, 100))
            screen.blit(mob1, (105, 150))
            screen.blit(mob2, (105, 200))
            screen.blit(mob3, (105, 250))
            screen.blit(mob4, (105, 300))

            for option in options :
                if option.rect.collidepoint(pygame.mouse.get_pos()) :
                    option.hovered = True
                    if pygame.mouse.get_pressed() == (1,0,0):
                        userSel = option.is_clicked()
                        menuClicked(userSel)
                else :
                    option.hovered = False
                option.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quitGame = True
            pygame.display.update()

    menu ()



def enemyMoveTrigger(groupName):
    global moveLeft
    global moveRight
    global moveDown
    global moveDownCount
    if moveDown == True:
        moveDownCount += 1
    if moveDownCount == 5:
        moveDown = False
        moveDownCount = 0
    for i in groupName.sprites():
        if i.rect.right >= 1390:
            if moveLeft == False:
                moveDown = True
            moveLeft = True
            moveRight = False
        elif i.rect.left <= 10:
            if moveRight == False:
                moveDown = True
            moveLeft = False
            moveRight = True


def addToGroup(iconName,groupName,order):
    for i in range(0,12):
        enem = Enemies(iconName)
        groupName.add(enem)
        enem.rect.x = 50 + (i*100)
        enem.rect.y = ((order+1) * 50) - 50

def enemyGroupKill(groupHit,value):
    global score
    global counter
    global waveNum
    for i in groupHit:
        score += value
        counter += 1
    if counter == 60:
        waveNum += 1
        counter = 0
        setUpWave()

def endGameRun(shipHit):
    global badShipList
    global livesGroup
    global endGame
    global bgBig
    global score
    global lifeShipList
    for shot in shipHit:
        if len(livesGroup) > lives:
            lifeShipList[len(livesGroup)-1].kill()
            friendlyGroup.add(playerShip)
    if len(livesGroup) == 0:
        endGame = True
        playerShip.kill()

    if endGame == True:
        for group in badShipList:
            for enemy in group:
                enemy.kill()
                bullet.kill()
                enemBullet.kill()
        badShipList = []
        surface.blit(bgBig,(0,0))
        surface.blit (endGameTitle, endTitleRect)
        surface.blit (closeGame, closeGameRect)
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    highScore = open("High_Score.txt","a")
                    highScore.write(str.strip(str(score))+"\n")
                    highScore.close()
                    mainMenu()

def drawSurfaces():
    time.sleep(0.01)
    enemsList1.draw(surface)
    enemsList2.draw(surface)
    enemsList3.draw(surface)
    enemsList4.draw(surface)
    enemsList5.draw(surface)
    enemBulletGroup.draw(surface)
    bulletGroup.draw(surface)
    friendlyGroup.draw(surface)
    livesGroup.draw(surface)
    pygame.display.update()

def setUpWave():
    global bullet
    global playerShip
    addToGroup("redShip.png",enemsList1,5)
    addToGroup("blackShip.png",enemsList2,4)
    addToGroup("brownShip.png",enemsList3,3)
    addToGroup("darkShip.png",enemsList4,2)
    addToGroup("crazyShip.gif",enemsList5,1)
    bullet = Bullet(90)

def playGame() :
    global playerShip
    global enemBullet
    global counter
    global score
    global lives
    global endGame
    global moveDown
    global moveLeft
    global moveRight
    global moveDownCount
    global lifeShipList
    global endTitleRect
    global closeGameRect
    global bgBig
    global waveNum
    lifeShipList = []
    xMove = 100
    quitGame = False #Setting some local.
    movingBullet = False
    moveRight = True #Setting some global variables.
    moveLeft = False
    moveDown = False
    endGame = False
    moveDownCount = 0
    score = 0
    waveNum = 1
    counter = 0
    lives = 0

    surface = pygame.display.set_mode((1400,600),0,32)
    pygame.display.set_caption("Earth Invaders")
     
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
     
    #Sets a "Space Invaders" title for the window
    myFont = pygame.font.SysFont("monospace", 20)
    scoreFont = pygame.font.SysFont ("monospace",20)
    endGameFont = pygame.font.SysFont ("monospace", 20)
    title = myFont.render("Earth Invaders",1,BLACK)
    endGameTitle = myFont.render("Game Over",1,BLACK)
    endTitleRect = endGameTitle.get_rect(center=(700,380))
    closeGame = myFont.render ("Press Escape to close",1,BLACK)
    closeGameRect = closeGame.get_rect(center=(700,325))
    
    playerShip = Friendly()

    friendlyGroup.add(playerShip)


    for i in range(0,3):
        livesShip= Friendly()
        lifeShipList.append(livesShip)
        livesGroup.add(livesShip)
        livesShip.rect.right = 1400- (i*55)

    badShipList.append(enemsList1)
    badShipList.append(enemsList2)
    badShipList.append(enemsList3)
    badShipList.append(enemsList4)
    badShipList.append(enemsList5)

    bg = pygame.image.load("gameBg.jpg")
    bgBig = pygame.transform.scale(bg,(1400,600))
    setUpWave()

    while True:
        displayScore = scoreFont.render ("Score: "+str(score), 1, BLUE) #Player score
        displayWaveNum = scoreFont.render ("Wave: "+str(waveNum),1,RED) #Player wave number
        surface.fill(WHITE)
        pygame.draw.line (surface, BLACK, (0, 540), (1400,540)) #Renders everything
        surface.blit(bgBig,(0,0))

        surface.blit(title, (600,0))
        surface.blit (displayScore, (0,0))
        surface.blit (displayWaveNum, (12,20))

        playerShip.rect.bottomleft = (xMove,595)

        shipHit = pygame.sprite.groupcollide(bulletGroup,enemsList1,True,True)
        shipHit2 = pygame.sprite.groupcollide(bulletGroup,enemsList2,True,True)
        shipHit3 = pygame.sprite.groupcollide(bulletGroup,enemsList3,True,True)
        shipHit4 = pygame.sprite.groupcollide(bulletGroup,enemsList4,True,True)
        shipHit5 = pygame.sprite.groupcollide(bulletGroup,enemsList5,True,True)

        enemyGroupKill(shipHit,10)
        enemyGroupKill(shipHit2,20)
        enemyGroupKill(shipHit3,40)
        enemyGroupKill(shipHit4,60)
        enemyGroupKill(shipHit5,80)

        shipLost = pygame.sprite.groupcollide(friendlyGroup,enemBulletGroup,True,True)
        endGameRun(shipLost)



        for group in badShipList:
            for i in group:
                randNum = random.randint(0,1500)
                if randNum == 5:
                    enemBullet = Bullet(270)
                    enemBullet.rect.x = i.rect.left + ((i.rect.right - i.rect.left)/2)
                    enemBullet.rect.top = i.rect.bottom
                    enemBulletGroup.add(enemBullet)
                if i.rect.bottom > 540:
                    for x in livesGroup:
                        x.kill()
        for i in enemBulletGroup.sprites():
            i.enemShoot()


        for group in badShipList:
            enemyMoveTrigger(group)

        for group in badShipList:
            for i in group:
                i.moveEnemies(group,moveLeft,moveRight,moveDown)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quitGame = True

        if quitGame == True:
            break
     

        if bullet.rect.top <= 0:
            bullet.kill()
        else:
            bullet.rect.y -=10
     
        pressed = pygame.key.get_pressed()
        if len(friendlyGroup) > 0:
            if pressed[pygame.K_SPACE] == True:
                if len(bulletGroup) < 1:
                        if event.key == pygame.K_SPACE:
                            bulletGroup.add(bullet)
                            movingBullet = True
                            bullet.rect.x = (playerShip.rect.left+25)
                            bullet.rect.y = (playerShip.rect.top)
        if pressed[pygame.K_UP] == True:
            for group in badShipList:
                for enemy in group:
                    enemy.kill()
                    bullet.kill()
                    enemBullet.kill()
            counter = 60
        if pressed[pygame.K_LEFT] and playerShip.rect.x >= 5:
            xMove -= 5
        if pressed[pygame.K_RIGHT] and playerShip.rect.right <= 1390:
            xMove += 5
        drawSurfaces()
mainMenu()



