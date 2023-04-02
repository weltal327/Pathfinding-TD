import pygame
import settings
from settings import TILE_SIZE
from timer import Timer
from sprites import Generic, Interaction
from enemy import Enemy
from tower import Tower
from pytmx.util_pygame import load_pygame



class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.all_sprites = CameraGroup()
		self.interaction_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		self.enemies = []
		self.towers = []

		#timers
		self.timers = {'spawn' : Timer(3000, self.spawn)}


		self.setup()

	def setup(self):
		tmx_data = load_pygame('../data/map2.tmx')

		Generic(
			pos=(0, 0),
			surf=pygame.image.load('../graphics/map.png').convert_alpha(),
			groups=self.all_sprites)

		# collision tiles
		for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		#grid setup
		ground = pygame.image.load('../graphics/map.png')
		h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

		self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
		for x, y, _ in load_pygame('../data/map2.tmx').get_layer_by_name('walkable').tiles():
			self.grid[y][x] = '1'
		for x, y, _ in load_pygame('../data/map2.tmx').get_layer_by_name('barrier1').tiles():
			self.grid[y][x] = '0'
		for x, y, _ in load_pygame('../data/map2.tmx').get_layer_by_name('barrier2').tiles():
			self.grid[y][x] = '0'



		# Enemy
		for obj in tmx_data.get_layer_by_name('enemy'):
			if obj.name == 'start':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			if obj.name == 'end':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

		#self.enemy = Enemy( pos = (500, 500), groups = self.all_sprites, name = '1')
					#collision_sprites=self.collision_sprites,
					#tree_sprites=self.tree_sprites,
					#interaction=self.interaction_sprites,
					#soil_layer=self.soil_layer,
					#toggle_shop=self.toggle_shop)

		#timer
		#self.timers['spawn'].activate()

	def spawn(self):
		# Enemy
		for interaction in self.interaction_sprites:
			if interaction.name == 'start':
				start_pos = (0,320)
		self.enemies.append(Enemy(pos=start_pos, groups=self.all_sprites, interaction = self.interaction_sprites, collision_sprites=self.collision_sprites, name='1', matrix = self.grid))


	def input(self):
		click = pygame.mouse.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		if click[0]:
			tower_pos = (mouse_pos[0]//32*32, mouse_pos[1]//32*32)
			self.towers.append(Tower(tower_pos,[self.all_sprites, self.collision_sprites],'1'))

			#update grid
			x = tower_pos[0]// TILE_SIZE
			y = tower_pos[1] // TILE_SIZE
			print(x)
			print(y)
			self.grid[y][x] = '0'

			for enemy in self.enemies:
				enemy.find_path(self.grid) #may need to pass the grid into enemies as they have old grid


	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def run(self, dt):
		self.display_surface.fill('green')
		self.input()
		if self.timers['spawn'].active:
			pass
		else:
			self.timers['spawn'].activate()
		self.update_timers()
		self.all_sprites.update(dt)
		self.all_sprites.custom_draw()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self):
		for sprite in self.sprites():
			self.display_surface.blit(sprite.image, sprite.rect.topleft)
