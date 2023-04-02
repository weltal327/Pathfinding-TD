import pygame
from settings import *
from sprites import Generic
from random import randint, choice
from timer import *

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, interaction, collision_sprites, name, matrix):
        # surf = pygame.Surface(size)
        super().__init__(groups)
        self.name = name

        self.image = pygame.image.load('../graphics/1/walk1.png')

        # self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        # self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        # self.direction.x = 1
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 200

        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy()#.inflate((-10, -10))

        # initial path
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)

        self.grid_pos = (int(self.pos[0] // 32), int(self.pos[1] // 32))

        self.start = self.grid.node(self.grid_pos[0], self.grid_pos[1])

        self.end = self.grid.node(29, 9)

        self.path, self.runs = self.finder.find_path(self.start, self.end, self.grid)


        self.interaction = interaction

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.rect.x = self.hitbox.x
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.y = round(self.pos.y)
        self.rect.y = self.hitbox.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                        #print(self.path)
                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def check_goal(self):
        collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
        if collided_interaction_sprite:
            if collided_interaction_sprite[0].name == 'end':
                self.kill()


    def follow_path(self):  # todo fix this - Need to make the directions to get it ALL THE WAY to next path
        #if the position is right on the grid keep it
        #if it's not right on the grid increase it by 1
        #if self.pos[0] % 32 == 0:
        #    newgridposx = self.pos[0] // 32
        #else:
        #    newgridposx = self.pos[0] // 32 + 1
        #if self.pos[1] % 32 == 0:
        #    newgridposy = self.pos[1] // 32
        #else:
        #    newgridposy = self.pos[1] // 32 + 1
        #self.grid_pos = (newgridposx, newgridposy)
        self.grid_pos = (int(self.pos[0] / 32), int(self.pos[1] / 32)) #took off floor divide to test
        print(self.grid_pos)
        current = None
        next = None
        for node in self.path:
            if node == self.grid_pos:
                start = pygame.math.Vector2(node)
                current = node
            else:
                if current is None:
                    pass
                else:
                    next = pygame.math.Vector2(node)

                    current = None
        if next:
            self.direction = (next - start).normalize()

        else:
            pass

    def find_path(self, matrix):
        self.grid = Grid(matrix=matrix)

        self.grid_pos = (int(self.pos[0] // 32), int(self.pos[1] // 32))
        self.start = self.grid.node(self.grid_pos[0], self.grid_pos[1])
        self.end = self.grid.node(29, 9)

        self.path, self.runs = self.finder.find_path(self.start, self.end, self.grid)

    def update(self, dt):
        # self.input()
        # self.get_status()
        # self.update_timers()
        # self.get_target_pos()
        self.check_goal()
        self.move(dt)
        self.follow_path()
        # self.animate(dt)
