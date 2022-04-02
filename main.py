import math
import random
import pygame
import os
from pygame import mixer
from dotenv import load_dotenv

load_dotenv(".env")

constants = ["ASSETS", "AUDIO", "FONTS", "IMAGES"]
for c in constants:
    locals().update({c: os.getenv(f"{c}_FOLDER")})

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1280, 720))

# Background
background = pygame.image.load(f"{IMAGES_FOLDER}/background.jpg")

# Caption and Icon
pygame.display.set_caption("The Last Pilot")
icon = pygame.image.load(f"{IMAGES_FOLDER}/icon.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load(f"{IMAGES_FOLDER}/player.png")
player_x = 50
player_y = 344
player_y_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(f"{IMAGES_FOLDER}/enemy.png"))
    enemy_x.append(random.randint(500, 1280))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(-50)
    enemy_y_change.append(2)

# Missile

# Ready - You can't see the missile on the screen
# Fire - The missile is currently moving

missile_img = pygame.image.load(f"{IMAGES_FOLDER}missile.png")
missile_x = 50
missile_y = 344
missile_x_change = 3
missile_y_change = 0
missile_state = "ready"

# Score
score_value = 0
font = pygame.font.Font(f"{FONTS_FOLDER}/font.TTF", 32)

test_x = 10
test_y = 10

# Game Over
over_font = pygame.font.Font(f"{FONTS_FOLDER}/font.TTF", 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (430, 360))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, missile_x, missile_y):
    distance = math.sqrt(math.pow(enemy_x - missile_x, 2) + (math.pow(enemy_y - missile_y, 2)))
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
                    missile_sound = mixer.Sound(f"{AUDIO_FOLDER}/laser.mp3")
                    missile_sound.set_volume(0.3)
                    missile_sound.play()
                    missile_y = player_y
                    fire_missile(missile_x, missile_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    player_y += player_y_change
    if player_y <= 0:
        player_y = 0
    elif player_y >= 656:
        player_y = 656

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_x[i] <= 100:
            player_y = 2000
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_y[i] += enemy_y_change[i]
        if enemy_y[i] <= 0:
            enemy_y_change[i] = 2
            enemy_x[i] += enemy_x_change[i]
        elif enemy_y[i] >= 656:
            enemy_y_change[i] = -2
            enemy_x[i] += enemy_x_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], missile_x, missile_y)
        if collision:
            explosion_sound = mixer.Sound(f"{AUDIO_FOLDER}/explosion.wav")
            explosion_sound.play()
            missile_x = 50
            missile_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(500, 1280)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Missile Movement
    if missile_x >= 1280:
        missile_x = 50
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missile_x, missile_y)
        missile_x += missile_x_change

    player(player_x, player_y)
    show_score(test_x, test_y)
    pygame.display.update()
