import pygame
import numpy as np
import random
from projectile_class import Projectile
from pygame import mixer
from gun_class import Gun


pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space_background.jpg')

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)

class Character:
    def __init__(self, name, image_file, img_size, health, x, y, speed, state = 1):
        self.charImg = pygame.image.load(image_file)
        self.img_size = img_size

        #Movement tracker       
        self.speed = speed
        self.pos = np.array([x, y])
        self.char_move = np.array([0, 0])
        self.up = np.array([0, -1])
        self.down = np.array([0, 1])
        self.right = np.array([1, 0])
        self.left = np.array([-1, 0])

        #Health
        self.max_health = health
        self.health = health
        self.state = state

        #Name
        self.name=name


    def __repr__(self):
        return self.name

    #Shows character on screen
    def display_char(self):
        if self.state == 1:
            screen.blit(self.charImg, (self.pos[0] - (self.img_size[0]/2), self.pos[1] - (self.img_size[1]/2)))
    
    #Shows movement
    def update_pos(self):
        self.pos = self.pos + self.char_move

    #Discern between dead and alive, 0 dead, 1 alive
    def status_dead(self):
        self.state = 0

    def status_alive(self):
        self.state = 1


class Player(Character):

    #Scoring
    score = 0

    def __init__(self, name, image_file, img_size, health, x, y, speed, gun, state = 1):
        super().__init__(name, image_file, img_size, health, x, y, speed, state)
        self.gun = gun

    #General function for either left or right key
    def key_press(self, direction):
        self.char_move = self.char_move + (direction * self.speed)

    def key_release(self, direction):
        self.char_move = self.char_move - (direction * self.speed)

    def fire(self,enemy_list):
        self.gun.execute(self.pos[0], self.pos[1], enemy_list, self)

    def score_up(self, point):
        self.score+= point

    #Keeps player within boundaries
    def boundary_check(self):
        if self.pos[0] < 30:
            self.pos[0] = 30
        if self.pos[0] > 740:
            self.pos[0] = 740
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > 550:
            self.pos[1] = 550

    #Increase score

    #Show score on screen
    def show_score(self):
        score = font.render('Score: '+ str(self.score), True, (255,255,255))
        screen.blit(score, (10, 10))

    #Decrease health: Can be used when enemy projectiles is implemented
    def decrease_health(self, damage, enemy):
        self.health -= damage
        if self.health <= 0:
            self.status_dead()
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            print('You are killed by', enemy)
            self.pos = [-10, -10]

    #Check if an enemy has hit the spaceship
    def enemy_collision(self, enemy_list):
        collision = False
        for enemy in enemy_list:
            d2 = np.dot(enemy.pos - self.pos, enemy.pos - self.pos)
            if d2 < (enemy.img_size[0]/2)**2:
                self.decrease_health(1, enemy)


    def execute(self, monster_lst):
        self.display_char()
        self.update_pos()
        self.fire(monster_lst)
        self.boundary_check()
        self.enemy_collision(monster_lst)
        self.show_score()

class Enemy(Character):

    score = 0

    #Initialization
    def __init__(self, name, image_file, img_size,health, x, y, speed, state, score_value, gun):
        super().__init__(name, image_file,img_size,health, x, y, speed, state)
        self.char_move = np.array([speed, 0])
        self.move_down = np.array([0, 50])
        self.score_value = score_value
        self.gun = gun

    #Check for boundary. move horizontally, go down when it hits the side, and move horizontally in the opposite direction
    def boundary_check(self):
        if self.pos[0] < 30 or self.pos[0] > 740:
            self.char_move = -self.char_move
            self.pos += self.move_down
        if self.pos[1] > 600:
            self.respawn()

    def fire(self, player_list):
        self.gun.execute(self.pos[0], self.pos[1], player_list, self)

    #Decrease health, check if self is dead
    def decrease_health(self, damage, player):
        self.health -= damage
        if self.health <= 0:
            player.score_up(self.score_value)
            self.status_dead()
            self.respawn()

    #Shows health. Might implement health bar
    def show_health(self):
        health = health_font.render('Health: '+ str(self.health), True, (255,255,255))
        screen.blit(health, (self.pos[0]- 20, self.pos[1]-50))

    def score_up(self, point):
        self.score+= point

    #Respawning mechanics. Randomly chooses an x,y coordinate on the top half of the screen. Can be scrapped in favor of classic space invaders
    def respawn(self):
        #Chooses a new start point
        new_x = random.randint(0, 739)
        new_y = random.randint(1,150)
        self.pos = np.array([new_x,new_y])


        #Restore enemy health
        self.health = self.max_health

        #increase enemy speed
        self.speed += 0.1
        self.char_move = np.array([self.speed, 0])

        #Resurrect enemy
        self.status_alive()
