import pygame
from pygame import *
import sys
import random
import time

# window setup
win = pygame.Surface
WIDTH = 700
HEIGHT = 700
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))

# song setup
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('song.mp3')
mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# set variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66, 135, 245)

class Player(pygame.sprite.Sprite): # player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = win((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 70)


class Mob(pygame.sprite.Sprite): # enemy sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 2)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)

def text_objects(text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

def message_display(text):# allows you to show text to user using function
    largeText = pygame.font.Font('ROGFontsv1.6-Regular.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def crash(): # game over function
    running = False
    message_display('Game Over')

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blocky Dodge")
clock = pygame.time.Clock()
pygame.key.set_repeat(True)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    mixer.music.set_volume(0.3)
    # Process input
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # sprite controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == K_w:
                player.rect.centery -= 2
            if event.key == pygame.K_SPACE:
                running = True
            elif event.key == pygame.K_DOWN or event.key == K_s:
                player.rect.centery += 2
            elif event.key == pygame.K_LEFT or event.key == K_a:
                player.rect.left -= 2
            elif event.key == pygame.K_RIGHT or event.key == K_d:
                if player.rect.x + player.image.get_width() < WIDTH:
                    player.rect.right += 2

    # Update
    all_sprites.update()

    # hitboxes
    hits = pygame.sprite.spritecollide(player, mobs, False)

    if hits: # game over sequence
        crash()
        mixer.music.set_volume(0.1)
        time.sleep(1)


    # Draw / render
    screen.fill((18,18,18))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()
