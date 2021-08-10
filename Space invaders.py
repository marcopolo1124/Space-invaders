import pygame
import numpy as np
import math

#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
#Default coordinates
playerX = 370
playerY = 480
playerX_r = 0
playerX_l = 0
def player(x, y):
    screen.blit(playerImg, (x,y))

running = True
color_x=0
color_y=0
color_z=0

while running:
    screen.fill((0,0,0))
    color_x+=0.001
    color_y+=0.001
    color_z+=0.001


    #event checker
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_l = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_r = 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_l = 0
            if event.key == pygame.K_RIGHT:
                playerX_r = 0
        #Quit checker
        if event.type == pygame.QUIT:
            running = False
    
    #RGB values
    
    playerX += (playerX_r + playerX_l)
    player(playerX,playerY)

    pygame.display.update()