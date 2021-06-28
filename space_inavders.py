"""
File: snake_game.py
----------------
The Goal of the game is to keep the snake kill the enemy before it reaches you. Spacebar controls your bullet
"""
import pygame
import random
import math
from simpleimage import SimpleImage

# Importing Image module from PIL package

from PIL import Image

# mixer is used for all sounds and music
from pygame import mixer

# creating window of pygame

# initialise pygame to access methods and functions
# needed to run pygame
pygame.init()

# width and height
screen = pygame.display.set_mode((800, 600))

# Background Sound
mixer.music.load("background.wav")
# play continuously
mixer.music.play(-1)

# To keep the program running
running = True

# Set Title, Icon and Background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('player.png')
# to move left (-5) to move right (+5)
playerX = 370
# to move up (-5) to move down (+5)
playerY = 480

# variable to save the changes of X coordinates
playerX_change = 0

# Enemy
# create a list of all the parameters of enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    # to move left (-5) to move right (+5)
    enemyX.append(random.randint(0, 735))
    # to move up (-5) to move down (+5)
    enemyY.append(random.randint(50, 150))

    # variable to save the changes of coordinates
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready: You cant see the bullet on the screen
# Fire: The bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
# to move left (-5) to move right (+5)
bulletX = 0
# to move up (-5) to move down (+5)
bulletY = 480

# variable to save the changes of coordinates
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score
score_value = 0
# font for text font name and size (www.dafint.com) for more fonts
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# pass parameters for new coordinates
def player(x, y):
    # blit means draw on screen
    screen.blit(player_img, (x, y))


# pass parameters for new coordinates
def enemy(x, y, i):
    # blit means draw on screen
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # x, y coordinates to fix bullet to center mouthpiece of spaceship
    screen.blit(bullet_img, (x + 16, y + 10))


# using the distance formula to calculate how close both objects are
# D = Square root(x2 - x1)^2 + (y2 -y1)^2
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False



def background_colour(image):
    # image = SimpleImage(PATCH_NAME)
    for pixel in image:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        if pixel.red >= average * INTENSITY_THRESHOLD:
            pixel.red = 105
            pixel.green = 0
            pixel.blue = 0
        elif pixel.blue >= average * INTENSITY_THRESHOLD:
            pixel.red = 0
            pixel.green = 0
            pixel.blue = 105
        else:
            # for the grey background
            pixel.red = average
            pixel.blue = average
            pixel.green = average
    return image


WIDTH = 600
HEIGHT = 600
PATCH_NAME = 'background.png'
INTENSITY_THRESHOLD = 1.4
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# drawing a circle
# pygame.draw.circle(screen, YELLOW, (120, 120), 50)

# Background Image
image = SimpleImage(PATCH_NAME)

final_image = background_colour(image)

final_image.pil_image.save("new_background.png")

background_img = pygame.image.load('new_background.png')
counter = 0
while running:
    # fill the background (R,G,B)
    screen.fill((0, 0, 0))

    # below the screen.fill so the image is infront.
    # loading of image in while loop slow downs the process
    screen.blit(background_img, (0, 0))

    # gets and checks all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5

            # if Key Space is pressed
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()

                    # Get the current x coordinate of the spaceship
                    # saves the start position for bullet
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        # stop moving if player releases key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking boundaries so the spaceship doesnt go out of screen
    # add change to X
    playerX += playerX_change

    # sets wall boundaries
    if playerX <= 0:
        playerX = 0
    #    boundary of width - size of spaceship
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over if one of the enemy go below 440
        if enemyY[i] > 440:
            # move the enemies below the screen to 2000 at Y
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # enemyY += enemyY_change

        # when hit wall change direction
        if enemyX[i] <= 0:
            # change to right direction
            enemyX_change[i] = 5
            # Hit boundary and go down
            enemyY[i] += enemyY_change[i]
        # boundary of width - size of spaceship
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Collision Pass if the parameter ans states if collision True
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # To keep randomly change enemy position
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # add enemy to background
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    # if bullet hit top of wall, reset coordinates to spaceship mouthpiece
    if bulletY <= 0:
        # reset bulletY to start position
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        # set coordinates
        fire_bullet(bulletX, bulletY)
        # Move bullet up
        bulletY -= bulletY_change

    # add player to background
    player(playerX, playerY)

    # add text to screen
    show_score(textX, textY)

    # update game
    pygame.display.update()
