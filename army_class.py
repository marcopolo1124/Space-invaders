import pygame
import numpy as np
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

#Words
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
health_font = pygame.font.Font('freesansbold.ttf', 10)

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
    def show_health(self):
        for monster in self.monster_lst:
            monster.show_health()