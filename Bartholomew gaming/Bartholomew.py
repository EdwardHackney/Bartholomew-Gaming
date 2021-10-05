import pygame
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = pygame.Color(173,216,230)
FPS = 60
GRAVITY = .2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
breadPic = pygame.image.load("Bartholomew gaming/Bartholomew Bread.png").convert_alpha()

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

running = True

gameObjects = []

loadImages()

def applyPhysics(obj):
    obj.yVel += GRAVITY
    obj.yPos += obj.yVel
    obj.xPos += obj.xVel


class Bartholomew:
    def __init__(self):
        self.xPos = 100
        self.yPos = 100
        self.xVel = 0
        self.yVel = 0
        self.image = images[0]

    def update(self):
        applyPhysics(self)

    def render(self):
        screen.blit(self.image, (self.xPos, self.yPos))

#Create Game Objects
bartholomew = Bartholomew()
gameObjects.append(bartholomew)

def handle_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update():
    for gameObject in gameObjects:
        gameObject.update()

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

pygame.QUIT()