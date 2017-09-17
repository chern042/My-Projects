import time, random, pygame

class Enemies(pygame.sprite.Sprite): #Class for the spaceships.
    def __init__(self,imageName):
        super().__init__()
        shipIcon = pygame.image.load(imageName)
        shipTransform = pygame.transform.rotate(shipIcon,180) #Rotate that ship 180 degrees.
        shipTransform = pygame.transform.scale(shipTransform,(60,45)) #Transform that ship to be 50 pixels wide, 35 pixels long.
        self.image = shipTransform.convert_alpha() #IDK I think you're supposed to do this.
        self.rect = self.image.get_rect() #Get sprite rect dimensions.
        self.moveTick = 0
        self.moveTickAdjust = 20
    def moveInRight(self):
        self.moveTick += 1
        if self.moveTick >= self.moveTickAdjust:
            self.rect.x += 10
            self.moveTick = 0

    def moveInLeft(self): #Same as above only moving left.
        self.moveTick += 1
        if self.moveTick >= self.moveTickAdjust:
            self.rect.x -= 10
            self.moveTick = 0

    def moveEnemies(self,groupName,left,right,down):#This function will set the ship in motion, switching from moving left to right, and intervals which it goes down from global variables passed into it.
            if right == True:
                if down == False:
                    self.moveInRight()
                else:
                    self.rect.y += 15
                    self.moveTickAdjust *= 0.9
            if left == True:
                if down == False:
                    self.moveInLeft()
                else:
                    self.moveTickAdjust *= 0.9
                    self.rect.y += 15



class Bullet(pygame.sprite.Sprite):
    def __init__(self,twist):
        super().__init__()
        bulletIcon = pygame.image.load("Bullet.png")
        bulletTransform = pygame.transform.rotate(bulletIcon,twist)
        bulletTransform = pygame.transform.scale(bulletTransform,(7,12))
        self.image = bulletTransform.convert_alpha()
        self.rect = self.image.get_rect()
    def enemShoot(self):
        if self.rect.y <= 600:
            self.rect.y += 5
        else:
            self.kill()



class Friendly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        shipIcon = pygame.image.load("Playership.png")
        shipResize = pygame.transform.scale(shipIcon,(50,50))
        self.image = shipResize.convert_alpha()
        self.rect = self.image.get_rect()



