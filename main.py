import pygame
import time
import pyautogui
from functools import wraps
from pygame.locals import K_w,K_a,K_s,K_d

from spritesheet import SpriteSheet

# basic setup

clock = pygame.time.Clock()
pygame.init()

WIDTH = (pyautogui.size()[0]//32) * 28
HEIGHT = (pyautogui.size()[1]//32) * 28
FRAMERATE = 60
SPEED = 8 # m/s^2

vec = pygame.math.Vector2
font = pygame.font.SysFont("calibri",32)
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

METER = 32
robot_sheet = SpriteSheet("assets/graphics/robot/roboformerSpritesheet.png")
animation_cache = {
    "robot":robot_sheet.load_row((0,0,8,8), 3, 4)
}

# standard memoization function
memoization_cache = {}
def memoize(func):
    '''memoization decorator to optimize functions.
    functions must have a return value for this to apply.'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in memoization_cache:
            memoization_cache[key] = func(*args, **kwargs)
        return memoization_cache[key]
    return wrapper


class Robot(pygame.sprite.Sprite):
    def __init__(self, dimensions:tuple) -> None:
        super().__init__()
        self.rect = pygame.Rect((WIDTH/2, HEIGHT/2), (dimensions[0], dimensions[1]))
        self.img = animation_cache["robot"][0]
        
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)

    def move(self):
        '''basic movement operations for sprites'''
        
        pressed_keys = pygame.key.get_pressed()

        # vertical movement
        if pressed_keys[K_w]:
            self.vel.y = -SPEED
        elif pressed_keys[K_s]:
            self.vel.y = SPEED
        else:
            self.vel.y = 0

        # horizontal movement
        if pressed_keys[K_a]:
            self.vel.x = -SPEED
        elif pressed_keys[K_d]:
            self.vel.x = SPEED
        else:
            self.vel.x = 0


        if self.vel.x!=0 or self.vel.y!=0:
            self.vel.scale_to_length(SPEED)

        self.pos += self.vel

        if self.pos.x > WIDTH + self.rect.width: # Right wall detection
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width: # Left wall detection
            self.pos.x = WIDTH + self.rect.width/2
        if self.pos.y > HEIGHT + self.rect.height: # Bottom wall detection
            self.pos.y = 0 - self.rect.height/2
        if self.pos.y < 0 - self.rect.height: # Top wall detection
            self.pos.y = HEIGHT + self.rect.height/2

        self.rect.midbottom = self.pos

    def draw(self, s):
        s.blit(self.img)

char = Robot((1*METER, 3*METER))


print(animation_cache["robot"])

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            pass
    
    screen.fill((0,0,0))

    char.move()
    screen.blit(char.img, screen)

    pygame.draw.rect(screen, (255,255,255), char.rect)
    pygame.display.flip()
    pygame.display.update()

    clock.tick(FRAMERATE)

pygame.quit()