import pygame
from projectile_class import Projectile


pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space_background.jpg')

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)

class Gun:
    
    rounds_fired = 0
    def __init__(self, magazine, reload_time, player):
        self.mag_size = magazine
        self.reload_time = reload_time
        self.time = reload_time
        self.space = False
        self.player = player

        #Dictionary that stores all available bullets. Auto initialization of projectile objects based on mag size
        self.magazine = {}
        for i in range(magazine):
            self.magazine[i] = Projectile('bullet.png', 'basic', 0.4)

    #lets players fire volleys
    def fire(self):
        #Checks if space is pressed and not released. Allows continuous press of space key
        if self.space:
            #delay shots when continuous firing.
            #Same bullets are used as to not define an infinite number of bullets
            #Bullets are 'reloaded' back in when they cross out of bounds and when reload time is up
            #shots can be changed to ready only if they are not ready, and if the reload time is up
            #shots can be changed to not ready only if they are in the ready state.
            if self.time < self.reload_time and self.magazine[self.rounds_fired % self.mag_size].state == 'ready':
                self.magazine[self.rounds_fired % self.mag_size].not_ready()
            elif self.time >= self.reload_time and self.magazine[self.rounds_fired % self.mag_size].state == 'not ready':
                self.magazine[self.rounds_fired % self.mag_size].ready()

            #Only fires when ready
            if self.magazine[self.rounds_fired % self.mag_size].state == 'ready':
                self.rounds_fired += 1
                self.reset_time()
                self.magazine[(self.rounds_fired-1) % self.mag_size].fire(self.player.pos[0], self.player.pos[1])

    #Display all bullets in the magazine
    def display_projectiles(self):
        for i in range(self.mag_size):
            self.magazine[i].display_bullet()

    #Update position of all bullets in the magazine
    def update_projectiles_pos(self):
        for i in range(self.mag_size):
            self.magazine[i].update_pos()

    #Check for out of bounds projectiles to reload
    def check_projectiles_pos(self):
        for i in range(self.mag_size):
            self.magazine[i].boundary_check()

    #Check if any of the bullets in magazine hit an enemy
    def check_collisions(self, enemy_list):
        for i in range(self.mag_size):
            self.magazine[i].collision(enemy_list, self.player)

    #After every fire, reset the reload timer
    def reset_time(self):
        self.time = 0

    #increase the timer by 1 frame
    def increment_time(self):
        self.time += 1

    #check if space is pressed
    def space_press(self):
        self.space = True

    def space_release(self):
        self.space= False
    

