import pygame,sys
import random

# initialize pygame
pygame.init()

# FPS 
FPS = 30
clock = pygame.time.Clock()

# constant variables
SCREENWIDTH = 800
SCREENHEIGHT = 600
RED = (255,0,0)

# screen
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

# title and icon
title = pygame.display.set_caption("Game cua hai")
icon = pygame.image.load("heart.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.png")

def display_background():
    screen.blit(background,(0,0))

# cat
scale = 0.2
catImg = pygame.image.load("cat.png")
catImg = pygame.transform.scale(catImg,(catImg.get_width()*scale,catImg.get_height()*scale))
catx = 400
caty= 500
catx_change = 0
caty_change = 0

def display_cat(x,y):
    screen.blit(catImg,(x,y))

# dog
scale = 0.2

dogImg = []
dogx = []
dogy = []
dogx_change = []
dogy_change = []
num_of_dogs = 5
image = pygame.image.load("dog.png")
img = pygame.transform.scale(image,(image.get_width()*scale,image.get_height()*scale))

for i in range(num_of_dogs):
    dogImg.append(img)
    dogx.append(random.randint(100,700))
    dogy.append(random.randint(50,100))
    dogx_change.append(5)
    dogy_change.append(40)

def display_dog(x,y,i):
    screen.blit(dogImg[i],(x,y))

# heart
heartImg = pygame.image.load("heart.png")
heart_rect = heartImg.get_rect()
heartx = catx
hearty= 500
heartx_change = 0
hearty_change = -7

ban = False

def display_heart(x,y):
    global ban
    ban = True
    screen.blit(heartImg,(x+16,y+10))

running = True
screen_y = 0

# Score value
score_value = 0
font = pygame.font.SysFont("Arial",30)
big_font = pygame.font.SysFont("Arial",70)

while running:
    screen.fill(RED)
    display_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                catx_change = -5
            if event.key == pygame.K_RIGHT:
                catx_change = 5
            if event.key == pygame.K_SPACE:
                if ban == False:
                    heartx = catx
                    display_heart(heartx,hearty)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                catx_change = 0
           
    # cat 
    if catx <= 0:
        catx = 0
    elif catx >= 716:
        catx = 716

    catx += catx_change
    display_cat(catx,caty)

    # dog 
    for i in range(num_of_dogs):

        # game over
        if dogy[i] >= 200:
            for j in range(num_of_dogs):
                dogy[j] = 2000
                catx_change = 0
            pygame.draw.rect(screen,(255,0,0),(0,0,SCREENWIDTH,screen_y))
            if screen_y <= SCREENHEIGHT:
                screen_y += 1

            lose_game_word = big_font.render("You Lose",True,(255,255,255))
            screen.blit(lose_game_word,(SCREENWIDTH//2 - 100,SCREENHEIGHT//2 - 70))

        if dogx[i] <= -10:
            dogx_change[i] = 5
            dogy[i] += dogy_change[i]
        if dogx[i] >= 740:
            dogx_change[i] = -5
            dogy[i] += dogy_change[i]
        dogx[i] += dogx_change[i]
        dog_rect = dogImg[i].get_rect()
        dog_rect.topleft = (dogx[i],dogy[i])
        display_dog(dogx[i],dogy[i],i)

        if heart_rect.colliderect(dog_rect):
            hearty = -100
            dogx[i] = random.randint(100,700)
            dogy[i] = random.randint(50,100)
            score_value += 1

    # heart
    heart_rect.topleft = (heartx,hearty)
    if ban:
        hearty += hearty_change
        display_heart(heartx,hearty)

    if hearty <= -30:
        hearty = caty
        ban = False

    # score
    score_word = font.render("SCORE x " + str(score_value),True,(255,255,255))
    screen.blit(score_word,(10,10))

    clock.tick(FPS)
    pygame.display.update()