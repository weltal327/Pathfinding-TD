import pygame
from settings import *
from sprites import Generic
from random import randint, choice
from timer import *

class Tower(pygame.sprite.Sprite):
        def __init__(self, pos, groups, name):
            #surf = pygame.Surface(size)
            super().__init__(groups)
            self.name = name

            self.image = pygame.image.load('../graphics/tower.png')

            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.copy()#.inflate((-10, -10))

