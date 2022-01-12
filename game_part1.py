import pygame,sys

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
dogImg = pygame.image.load("dog.png")
dogImg = pygame.transform.scale(dogImg,(dogImg.get_width()*scale,dogImg.get_height()*scale))
dogx = 500
dogy= 200
dogx_change = 0
dogy_change = 0

def display_dog(x,y):
    screen.blit(dogImg,(x,y))

running = True
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
    display_dog(dogx,dogy)

    clock.tick(FPS)
    pygame.display.update()