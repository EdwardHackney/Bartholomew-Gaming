import pygame
import time

from pygame.constants import BUTTON_LEFT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = pygame.Color(173,216,230)
FPS = 60
GRAVITY = .2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
breadPic = pygame.image.load("Bartholomew gaming/Bartholomew Bread.png").convert_alpha()
grassPic = pygame.image.load("Bartholomew gaming/Bart grass.png").convert_alpha()

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() > 0 :
    gamepad = pygame.joystick.Joystick(0)
    gamepad_control = True
else :
    print("No gamepad detected.")
    gamepad_control = False

images = []
def loadImages():
    global images
    images.append(pygame.image.load("Bartholomew gaming/Bartholomew Bread.png").convert_alpha())
    images.append(pygame.image.load("Bartholomew gaming/Bart grass.png").convert_alpha())

running = True

gameObjects = []

loadImages()

def applyPhysics(obj):
    obj.yVel += GRAVITY
    obj.yPos += obj.yVel
    obj.xPos += obj.xVel

class Collider:
    def __init__(self, pos, width, height):
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.width = width
        self.height = height


class Bartholomew:
    def __init__(self):
        self.xPos = 100
        self.yPos = 100
        self.xVel = 0
        self.yVel = 0
        self.image = images[0]
        self.collider = Collider((4,6), 14, 16) #x14 y16/ 4 6

    def update(self):
        applyPhysics(self)

    def render(self):
        screen.blit(self.image, (self.xPos, self.yPos))

    def handleCollision(self, obj):
        if isinstance(obj, Grass):
            self.yVel = 0
            self.yPos = obj.yPos - self.collider.height - self.collider.yPos
            


class Grass:
    def __init__(self, pos):
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.image = images[1]
        self.collider = Collider ((0,0), 32, 32)

    def update(self):
        pass

    def render(self):
        screen.blit(self.image, (self.xPos, self.yPos))

def generateLevel():
    for i in range(int(SCREEN_WIDTH / 32)):
        x = i*32
        y = 450
        block = Grass((x,y))
        gameObjects.append(block)

def colliding(obj1, obj2):
    right1 = obj1.xPos + obj1.collider.xPos + obj1.collider.width
    left2 = obj2.xPos + obj1.collider.xPos
    if right1 < left2:
        return False

    left1 = obj1.xPos + obj1.collider.xPos
    right2 = obj2.xPos + obj2.collider.xPos + obj2.collider.width

    if left1 > right2:
        return False

    bottom1 = obj1.yPos + obj1.collider.yPos + obj1.collider.height
    top2 = obj2.yPos + obj2.collider.yPos

    if bottom1 < top2:
        return False

    top1 = obj1.yPos + obj1.collider.yPos + obj1.collider.height
    bottom2 = obj2.yPos + obj2.collider.yPos + obj2.collider.height
    
    if bottom2 < top1:
        return False

    return True

def checkCollisions():
    for gameObject in gameObjects:
        if gameObject != bartholomew:
            if colliding(bartholomew, gameObject):
                bartholomew.handleCollision(gameObject )

#Create Game Objects
bartholomew = Bartholomew()
gameObjects.append(bartholomew) 
generateLevel()


def handle_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update():
    for gameObject in gameObjects:
        gameObject.update()

    checkCollisions()

def render():
    screen.fill(LIGHT_BLUE)
    for gameObject in gameObjects:
        gameObject.render()
    pygame.display.flip()

lastLoopTime = time.time()
secondsPerLoop = 1/FPS 

def wait():
    global lastLoopTime
    elapsedTime = time.time() - lastLoopTime
    extraTime = secondsPerLoop - elapsedTime
    if extraTime > 0:
        time.sleep(extraTime)
    lastLoopTime = time.time()

while running:
    handle_input()
    update()
    render()
    wait()
    generateLevel()


pygame.QUIT()
