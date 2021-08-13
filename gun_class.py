import pygame
from projectile_class import Projectile


pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('space_background.jpg')

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)

class Gun:
    
    
    def __init__(self, img_file, magazine, reload_time, direction = 1):
        self.mag_size = magazine
        self.reload_time = reload_time
        self.time = reload_time
        self.firing = False
        self.direction = direction
        self.hit = 0
        self.rounds_fired = 0
        self.img_file = img_file

        #Dictionary that stores all available bullets. Auto initialization of projectile objects based on mag size
        self.magazine = {}
        for i in range(magazine):
            self.magazine[i] = Projectile(img_file, 'basic', 0.4, direction = self.direction)

    #lets players fire volleys
    def fire(self, x, y):
        #Checks if firing is pressed and not released. Allows continuous press of firing key
        if self.firing:
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
                self.magazine[(self.rounds_fired-1) % self.mag_size].fire(x, y)

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
    def check_enemy_collisions(self, enemy_list, player):
        for i in range(self.mag_size):
            self.magazine[i].enemy_collision(enemy_list, player)


    #After every fire, reset the reload timer
    def reset_time(self):
        self.time = 0

    #increase the timer by 1 frame
    def increment_time(self):
        self.time += 1

    #check if firing is pressed




class Player_Gun(Gun):
    def check_enemy_collisions(self, enemy_list, player):
        for i in range(self.mag_size):
            self.magazine[i].enemy_collision(enemy_list, player)
    
    def firing_press(self):
        self.firing = True

    def firing_release(self):
        self.firing= False

    def execute(self, x, y, enemy_list, player):
        self.display_projectiles()
        self.update_projectiles_pos()
        self.check_projectiles_pos()
        self.check_enemy_collisions(enemy_list, player)
        self.increment_time()
        self.fire(x, y)

class Enemy_Gun(Gun):
    def __init__(self, img_file, magazine, reload_time, direction):
        super().__init__(img_file, magazine, reload_time, direction=direction)
        self.firing = True

    def execute(self, x, y, player_list, enemy):
        self.display_projectiles()
        self.update_projectiles_pos()
        self.check_projectiles_pos()
        self.check_enemy_collisions(player_list, enemy)
        self.increment_time()
        self.fire(x,y)


    


