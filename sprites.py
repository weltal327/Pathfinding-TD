import pygame
from settings import *
from random import randint, choice
from timer import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy() #.inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

    #def update(self, dt):
    #    pass


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.pos = pos
        self.name = name

