import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1280, 720))

# Background
background = pygame.image.load("background.jpg")

# Caption and Icon
pygame.display.set_caption("The Last Pilot")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 50
playerY = 344
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(500, 1280))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(-50)
    enemyY_change.append(2)

# Missile

# Ready - You can't see the missile on the screen
# Fire - The missile is currently moving

missileImg = pygame.image.load("missile.png")
missileX = 50
missileY = 344
missileX_change = 3
missileY_change = 0
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("04B_19__.TTF", 32)

testX = 10
testY = 10

# Game Over
over_font = pygame.font.Font("04B_19__.TTF", 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (430, 360))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(math.pow(enemyX - missileX, 2) + (math.pow(enemyY - missileY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -3
            if event.key == pygame.K_DOWN:
                playerY_change = 3
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missileSound = mixer.Sound("laser.mp3")
                    missileSound.set_volume(0.3)
                    missileSound.play()
                    missileY = playerY
                    fire_missile(missileX, missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 656:
        playerY = 656

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyX[i] <= 100:
            playerY = 2000
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 2
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 656:
            enemyY_change[i] = -2
            enemyX[i] += enemyX_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            missileX = 50
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(500, 1280)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Missile Movement
    if missileX >= 1280:
        missileX = 50
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileX += missileX_change

    player(playerX, playerY)
    show_score(testX, testY)
    pygame.display.update()
    