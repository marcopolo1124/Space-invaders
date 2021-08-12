import pygame
import numpy as np
import random
from pygame import mixer
from character_class import Player
from character_class import Enemy
from army_class import Army
from gun_class import Gun


# Initialize pygame 
pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space_background.jpg')

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


def game_over(player):
    over_text = over_font.render('GAME OVER', True, (255,0,0))
    if player.score >= 1000 or player.state == 0:
        screen.blit(over_text, (200,250))
        

# Initialize characters

Eyeball_monster1 = Enemy(name = 'Eyeball Monster1', image_file = 'eyeball.png', img_size = [80, 80], health = 3, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1)
Eyeball_monster2 = Enemy(name = 'Eyeball Monster2', image_file = 'eyeball.png', img_size = [80, 80], health = 3, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1)
Eyeball_monster3 = Enemy(name = 'Eyeball Monster3', image_file = 'eyeball.png', img_size = [80, 80], health = 3, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1)

enemy_list = [Eyeball_monster1, Eyeball_monster2, Eyeball_monster3]

Eyeball_army = Army(enemy_list)
player1 = Player(name = 'Marco',image_file = 'player.png',img_size = [30,30], x= 370, y = 480, health = 3, speed = 0.6)
pistol = Gun(magazine = 10, reload_time = 300, player = player1)

running = True
while running:
    screen.fill((0, 0, 34))
    screen.blit(background, (0, 0))

    #Show player on screen
    pistol.display_projectiles()
    player1.display_char()

    #Show all enemies on screen
    Eyeball_army.display_army()
    Eyeball_army.show_health()

    # event checker
    for event in pygame.event.get():

        # Check event for a key press
        if event.type == pygame.KEYDOWN:

            #Moving player
            if event.key == pygame.K_LEFT:
                player1.key_press(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_press(player1.right)
            # if event.key == pygame.K_UP:
            #     player1.key_press(player1.up)
            # if event.key == pygame.K_DOWN:
            #     player1.key_press(player1.down)
            
            #Firing
            if event.key == pygame.K_SPACE:
                pistol.space_press()



        # Check event for a key release
        if event.type == pygame.KEYUP:

            #Moving player
            if event.key == pygame.K_LEFT:
                player1.key_release(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_release(player1.right)
            # if event.key == pygame.K_UP:
            #     player1.key_release(player1.up)
            # if event.key == pygame.K_DOWN:
            #     player1.key_release(player1.down)
            if event.key == pygame.K_SPACE:
                pistol.space_release()



        # Quit checker
        if event.type == pygame.QUIT:
            running = False


    #position update
    player1.update_pos()
    Eyeball_army.update_pos()
    pistol.update_projectiles_pos()

    #firing
    pistol.fire()

    #check if position is out of bounds
    player1.boundary_check()
    Eyeball_army.boundary_check()
    pistol.check_projectiles_pos()

    #Check damage
    pistol.check_collisions(Eyeball_army.monster_lst)
    player1.enemy_collision(Eyeball_army.monster_lst)

    #Show score
    player1.show_score()

    #Increase reload time
    pistol.increment_time()

    #Check game over condition
    game_over(player1)
    pygame.display.update()
