import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("bg.jpg")

pygame.display.set_caption("Mask the Corona")
icon = pygame.image.load('doctor.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

enemy_1_Img = []
enemy_1_X = []
enemy_1_Y = []
enemy_1_X_change = []
enemy_1_Y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemy_1_Img.append(pygame.image.load("enemy_2.png"))
    enemy_1_X.append(random.randint(0, 735))
    enemy_1_Y.append(random.randint(0, 100))
    enemy_1_X_change.append(1)
    enemy_1_Y_change.append(40)

maskImg = pygame.image.load("mask.png")
maskX = 0
maskY = 480
maskX_change = 0
maskY_change = 1
mask_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 390
textY = 10

gameover_font = pygame.font.Font('freesansbold.ttf', 32)

def gameover_text():
    over_text = gameover_font.render(
        "Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def score(x, y):
    score = font.render("Score: " + str(score_value),
                        True, (255, 255, 255))
    screen.blit(score, (x, y))

def fire(x, y):
    global mask_state
    mask_state = "fire"
    screen.blit(maskImg, (x+30, y + 20))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy_1(x, y, i):
    screen.blit(enemy_1_Img[i], (x, y))

def collision(enemy_1_X, enemy_1_Y, maskX, maskY):
    distance = math.sqrt((math.pow(enemy_1_X-maskX, 2)) +
                            (math.pow(enemy_1_Y-maskY, 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    screen.fill((255, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if mask_state is "ready":
                    maskX = playerX
                    fire(maskX, maskY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 700:
        playerX = 700

    for i in range(num_of_enemies):

        if enemy_1_Y[i] > 440:
            for j in range(num_of_enemies):
                enemy_1_Y[j] = 2000
            gameover_text()
            break

        enemy_1_X[i] += enemy_1_X_change[i]

        if enemy_1_X[i] <= 0:
            enemy_1_X_change[i] = 1
            enemy_1_Y[i] += enemy_1_Y_change[i]
        elif enemy_1_X[i] >= 736:
            enemy_1_X_change[i] = -1
            enemy_1_Y[i] += enemy_1_Y_change[i]

        iscollision = collision(enemy_1_X[i], enemy_1_Y[i], maskX, maskY)
        if iscollision:
            maskY = 480
            mask_state = "ready"
            score_value += 1
            enemy_1_X[i] = random.randint(0, 735)
            enemy_1_Y[i] = random.randint(0, 100)

        enemy_1(enemy_1_X[i], enemy_1_Y[i], i)

    if maskY <= 0:
        maskY = 480
        mask_state = "ready"

    if mask_state is "fire":
        fire(maskX, maskY)
        maskY -= maskY_change

    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()