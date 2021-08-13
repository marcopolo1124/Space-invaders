import pygame
import numpy as np
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)



#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

class Projectile:
    def __init__(self, image_file, name, speed, direction = 1):
        self.bullet_image = pygame.image.load(image_file)
        self.name = name
        self.movement = np.array([0, -speed])
        self.state = 'ready'
        self.available = 'yes'
        self.pos = np.array([0, 0])
        self.direction = direction
        self.collision = False

    def __repr__(self):
        return self.name

    def fire(self, x, y):

        if self.state == 'ready':
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            self.state = 'fire'
            self.available = 'yes'
            self.pos[0] = x
            self.pos[1] = y

    def update_pos(self):
        if self.state == 'fire':
            self.pos = self.pos + (self.movement*self.direction)

    def display_bullet(self):
        if self.state == 'fire' and self.available == 'yes':
            screen.blit(self.bullet_image, (self.pos[0], self.pos[1]))

    def boundary_check(self):
        if self.pos[1] < 0 or self.pos[1] > 600:
            self.not_ready()


    def enemy_collision(self, enemy_list, player):
        if self.available == 'yes':
            for i in range(len(enemy_list)):
                d2 = np.dot(enemy_list[i].pos - self.pos, enemy_list[i].pos - self.pos)
                if d2 < (enemy_list[i].img_size[0]/2)**2:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    enemy_list[i].decrease_health(1, player)
                    player.score_up(1)
                    self.available = 'no'



    def ready(self):
        self.state = 'ready'

    def not_ready(self):
        self.state = 'not ready'