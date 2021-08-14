import pygame
import random
from pygame import mixer
from character_class import Player
from character_class import Enemy
from army_class import Army
from gun_class import Player_Gun
from gun_class import Enemy_Gun


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

dick_gun = Player_Gun(img_file = 'penis.png', magazine = 20, reload_time = 50)
pistol = Player_Gun(img_file = 'bullet.png',magazine = 10, reload_time = 300)
eye1 = Enemy_Gun(img_file = 'tear.png', magazine = 10, reload_time = 200, direction = -1)
eye2 = Enemy_Gun(img_file = 'tear.png',magazine = 10, reload_time = 400, direction = -1)
eye3 = Enemy_Gun(img_file = 'tear.png',magazine = 10, reload_time = 50, direction = -1)

Eyeball_monster1 = Enemy(name = 'Eyeball Monster1', image_file = 'eyeball.png', img_size = [80, 80], health = 50, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1, score_value = 30, gun = eye1)
Eyeball_monster2 = Enemy(name = 'Eyeball Monster2', image_file = 'eyeball.png', img_size = [80, 80], health = 10, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1, score_value = 20, gun = eye2)
Eyeball_monster3 = Enemy(name = 'Eyeball Monster3', image_file = 'eyeball.png', img_size = [80, 80], health = 3, x = random.randint(0,739), y = random.randint(1,150), speed = 0.2, state = 1, score_value = 10, gun = eye3)

enemy_list = [Eyeball_monster1, Eyeball_monster2, Eyeball_monster3]

Eyeball_army = Army(enemy_list)
player1 = Player(name = 'Marco',image_file = 'player.png',img_size = [50,50], x= 370, y = 480, health = 5, speed = 0.6, gun = dick_gun)



running = True
while running:
    screen.fill((0, 0, 34))
    screen.blit(background, (0, 0))
    # event checker
    for event in pygame.event.get():
        # Check event for a key press
        if event.type == pygame.KEYDOWN:

            #Moving player
            if event.key == pygame.K_LEFT:
                player1.key_press(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_press(player1.right)
            
            #Firing
            if event.key == pygame.K_SPACE:
                player1.gun.firing_press()

        # Check event for a key release
        if event.type == pygame.KEYUP:

            #Moving player
            if event.key == pygame.K_LEFT:
                player1.key_release(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_release(player1.right)
            if event.key == pygame.K_SPACE:
                player1.gun.firing_release()
        # Quit checker
        if event.type == pygame.QUIT:
            running = False


    player1.execute(Eyeball_army.monster_lst)
    Eyeball_army.execute([player1])

    #Check game over condition
    game_over(player1)
    pygame.display.update()
