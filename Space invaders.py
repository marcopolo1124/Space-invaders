import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space_background.jpg')
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


class Character:
    def __init__(self, name, image_file, img_size, health, x, y, speed, state = 1):
        self.charImg = pygame.image.load(image_file)
        self.img_size = img_size

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

    #Could add finesse score, also allow for volley counting and reloading
    rounds_fired = 0

    def __init__(self, name, image_file, img_size, x, y, health = 3, magazine=2, speed=0.6, state = 1):
        super().__init__(name, image_file, img_size,health, x, y, speed, state)
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
            self.magazine[i].collision(enemy_list, self)

    def score_up(self, points):
        self.score += points
    
    def show_score(self):
        score = font.render('Score: '+ str(self.score), True, (255,255,255))
        screen.blit(score, (10, 10))

    def decrease_health(self, damage, enemy):
        self.health -= damage
        if self.health <= 0:
            self.status_dead()
            print('You are killed by', enemy)
            self.pos = [-10, -10]

    def enemy_collision(self, enemy_list):
        collision = False
        for enemy in enemy_list:
            d2 = np.dot(enemy.pos - self.pos, enemy.pos - self.pos)
            if d2 < (enemy.img_size[0]/2)**2:
                self.decrease_health(1, enemy)
                print('player health', self.health)
                collision = True

            else:
                collision = False
        return collision
    


class Enemy(Character):
    def __init__(self, name, image_file, img_size,health, x, y, speed, state):
        super().__init__(name, image_file,img_size,health, x, y, speed, state)
        self.char_move = np.array([speed, 0])
        self.move_down = np.array([0, 50])


    def boundary_check(self):
        if self.pos[0] < 30 or self.pos[0] > 740:
            self.char_move = -self.char_move
            self.pos += self.move_down
        if self.pos[1] > 600:
            self.respawn()

    def decrease_health(self, damage, player):
        self.health -= damage
        if self.health <= 0:
            self.status_dead()
            player.score_up(10)
            self.respawn()

    def respawn(self):
        new_x = random.randint(0, 739)
        new_y = random.randint(1,150)
        self.pos = np.array([new_x,new_y])
        self.health = self.max_health
        self.speed += 0.1
        self.char_move = np.array([self.speed, 0])
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
            self.pos[0] = x
            self.pos[1] = y

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
        collision = False
        if self.available == 'yes':
            for i in range(len(enemy_list)):
                d2 = np.dot(enemy_list[i].pos - self.pos, enemy_list[i].pos - self.pos)
                if d2 < (enemy_list[i].img_size[0]/2)**2:
                    enemy_list[i].decrease_health(1, player)
                    print(enemy_list[i], 'health ', enemy_list[i].health)
                    player.score_up(1)
                    self.available = 'no'
                    collision = True
                
                else:
                    collision = False
        return collision

class Army:
    def __init__(self, monster_lst):
        self.monster_lst = monster_lst
    def display_army(self):
        for monster in self.monster_lst:
            monster.display_char()
    def update_pos(self):
        for monster in self.monster_lst:
            monster.update_pos()
    def boundary_check(self):
        for monster in self.monster_lst:
            monster.boundary_check()

def game_over(player):
    over_text = over_font.render('GAME OVER', True, (255,0,0))
    if player.score >= 1000 or player.state == 0:
        screen.blit(over_text, (200,250))
        

                    


# Initialize characters

Eyeball_monster1 = Enemy('Eyeball Monster1', 'eyeball.png', [80, 80], 3, random.randint(0,739), random.randint(1,150), 0.2, 1)
Eyeball_monster2 = Enemy('Eyeball Monster2', 'eyeball.png', [80, 80], 3, random.randint(0,739), random.randint(1,150), 0.2, 1)
Eyeball_monster3 = Enemy('Eyeball Monster3', 'eyeball.png', [80, 80], 3, random.randint(0,739), random.randint(1,150), 0.2, 1)

enemy_list = [Eyeball_monster1, Eyeball_monster2, Eyeball_monster3]

Eyeball_army = Army(enemy_list)
player1 = Player('Marco','player.png',[30,30], 370, 480, magazine = 100)


running = True
while running:
    screen.fill((0, 0, 34))
    screen.blit(background, (0, 0))
    player1.display_projectiles()
    player1.display_char()
    Eyeball_army.display_army()

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
                player1.fire()


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



        # Quit checker
        if event.type == pygame.QUIT:
            running = False

    player1.update_pos()
    player1.boundary_check()
    player1.update_projectiles_pos()
    Eyeball_army.update_pos()
    Eyeball_army.boundary_check()
    player1.check_projectiles_pos()
    player1.check_collisions(Eyeball_army.monster_lst)
    player1.enemy_collision(Eyeball_army.monster_lst)
    player1.show_score()
    game_over(player1)
    pygame.display.update()
