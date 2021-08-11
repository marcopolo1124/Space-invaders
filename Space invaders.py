import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space_background.jpg')

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


class Character:
    def __init__(self, name, image_file, health, x, y, speed, state = 1):
        self.charImg = pygame.image.load(image_file)

        #Movement tracker
        
        self.speed = speed
        self.pos = np.array([x, y])
        self.char_move = np.array([0, 0])
        self.up = np.array([0, -1 * speed])
        self.down = np.array([0, speed])
        self.right = np.array([speed, 0])
        self.left = np.array([-1*speed, 0])
        
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
            screen.blit(self.charImg, (self.pos[0], self.pos[1]))
    
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

    #Could add finesse score, also allow for volley counting and reloading
    rounds_fired = 0

    def __init__(self, name, image_file, x, y, health = 3, magazine=2, speed=0.6, state = 1):
        super().__init__(name, image_file, health, x, y, speed, state)
        self.mag_size = magazine

        #Dictionary that stores all available bullets. Auto initialization of projectile objects
        self.magazine = {}
        for i in range(magazine):
            self.magazine[i] = Projectile('bullet.png', 'basic', 0.4)

    def key_press(self, direction):
        self.char_move = self.char_move + (direction * self.speed)

    def key_release(self, direction):
        self.char_move = self.char_move - (direction * self.speed)

    def boundary_check(self):
        if self.pos[0] < 30:
            self.pos[0] = 30
        if self.pos[0] > 740:
            self.pos[0] = 740
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > 550:
            self.pos[1] = 550

    def fire(self):
        if self.magazine[self.rounds_fired % self.mag_size].state == 'ready':
            self.rounds_fired += 1
        self.magazine[(self.rounds_fired-1) %
                      self.mag_size].fire(self.pos[0], self.pos[1])

        print(self.rounds_fired)

    def display_projectiles(self):
        for i in range(self.mag_size):
            self.magazine[i].display_bullet()

    def update_projectiles_pos(self):
        for i in range(self.mag_size):
            self.magazine[i].update_pos()

    def check_projectiles_pos(self):
        for i in range(self.mag_size):
            self.magazine[i].boundary_check()

    def check_collisions(self, enemy_list):
        for i in range(self.mag_size):
            if self.magazine[i].collision(enemy_list, self):
                self.score_up(1)
                print('Score: ', self.score)

    def score_up(self, points):
        self.score += points

    def decrease_health(self, damage, enemy):
        self.health -= damage
        if self.health <= 0:
            self.status_dead()
            print('You are killed by', enemy)
            self.pos = [-10, -10]

    def enemy_collision(self, enemy_list):
            for enemy in enemy_list:
                d2 = np.dot(enemy.pos - self.pos, enemy.pos - self.pos)
                if d2 < 729:
                    self.decrease_health(1, enemy)
                    print('player health', self.health)

                    return True
                else:
                    return False


class Enemy(Character):
    def __init__(self, name, image_file,health, x, y, speed, state):
        super().__init__(name, image_file,health, x, y, speed, state)
        self.char_move = np.array([speed, 0])
        self.move_down = np.array([0, 50])


    def boundary_check(self):
        if self.pos[0] < 30 or self.pos[0] > 740:
            self.char_move = -self.char_move
            self.pos += self.move_down

    def decrease_health(self, damage, player):
        self.health -= damage
        if self.health <= 0:
            self.status_dead()
            player.score_up(10)
            print(player.score)
            self.respawn()

    def respawn(self):
        new_x = random.randint(0, 740)
        new_y = random.randint(1,150)
        self.pos = np.array([new_x,new_y])
        self.health = self.max_health
        self.status_alive()



class Projectile:
    def __init__(self, image_file, name, speed):
        self.bullet_image = pygame.image.load(image_file)
        self.name = name
        self.movement = np.array([0, -speed])
        self.state = 'ready'
        self.available = 'yes'
        self.pos = np.array([0, 0])

    def __repr__(self):
        return self.name

    def fire(self, x, y):
        print('fire')
        if self.state == 'ready':
            self.state = 'fire'
            self.available = 'yes'
            self.pos[0] = x+16
            self.pos[1] = y+10

    def update_pos(self):
        if self.state == 'fire':
            self.pos = self.pos + self.movement

    def display_bullet(self):
        if self.state == 'fire' and self.available == 'yes':
            screen.blit(self.bullet_image, (self.pos[0], self.pos[1]))

    def boundary_check(self):
        if self.pos[1] < 0:
            self.state = 'ready'

    def collision(self, enemy_list, player):
        if self.available == 'yes':
            for enemy in enemy_list:
                d2 = np.dot(enemy.pos - self.pos, enemy.pos - self.pos)
                if d2 < 729:
                    enemy.decrease_health(1, player)
                    print('health ', enemy.health)
                    self.available = 'no'

                    return True
                else:
                    return False
                    


# Initialize characters

Eyeball_monster = Enemy('Eyeball Monster', 'eyeball.png', 10, 30, 30, 0.2, 1)
enemy_list = [Eyeball_monster]
player1 = Player('Marco','player.png', 370, 480, magazine = 10)


running = True
while running:
    screen.fill((0, 0, 34))
    screen.blit(background, (0, 0))
    player1.display_projectiles()
    player1.display_char()
    Eyeball_monster.display_char()

    # event checker
    for event in pygame.event.get():

        # Check event for a key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.key_press(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_press(player1.right)
            # if event.key == pygame.K_UP:
            #     player1.key_press(player1.up)
            # if event.key == pygame.K_DOWN:
            #     player1.key_press(player1.down)

        # Check event for a key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player1.key_release(player1.left)
            if event.key == pygame.K_RIGHT:
                player1.key_release(player1.right)
            # if event.key == pygame.K_UP:
            #     player1.key_release(player1.up)
            # if event.key == pygame.K_DOWN:
            #     player1.key_release(player1.down)
            if event.key == pygame.K_SPACE:
                player1.fire()

        # Quit checker
        if event.type == pygame.QUIT:
            running = False

    player1.update_pos()
    player1.boundary_check()
    player1.update_projectiles_pos()
    Eyeball_monster.update_pos()
    Eyeball_monster.boundary_check()
    player1.check_projectiles_pos()
    player1.check_collisions(enemy_list)
    player1.enemy_collision(enemy_list)
    pygame.display.update()
