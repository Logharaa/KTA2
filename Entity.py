import pygame, pytmx, sys
from pygame.locals import *
from Map import *
import Map
sys.path.insert(0, "Entity")
sys.path.insert(0, "HUD")
import Player

class Entity:
	temp = 0
	entities = []
	mapmatrix = []

	def __init__(self, x, y, speed, image, nbAnimsFrames, pace):
		self.sprite = pygame.image.load(image)
		self.position = self.sprite.get_rect()
		self.size = self.position.size
		self.position = self.position.move(x, y)
		self.speed = speed
		self.anim = 0
		self.frame = 0
		self.maxAnimsFrames = 0
		for i in nbAnimsFrames:
			if i >= self.maxAnimsFrames:
				self.maxAnimsFrames = i
		self.nbAnimsFrames = nbAnimsFrames
		self.pace = pace
		self.entities.append(self)
		self.key = False
		self.keyowned = False

	@staticmethod
	def draw(window, camera):
		for i in Entity.entities:
			type(i).render(i, window, camera)
		Entity.temp = (Entity.temp + 1) % 256

	@staticmethod
	def collider(self, maps, map_imgs, player, camera, currentlevel):
		sTile = 16
		collideBloc = pygame.image.load("textures/collision.png")
		keyImg = pygame.image.load("textures/objects/key.png")
		keyImg = pygame.transform.scale(keyImg, (14*2, 16*2))
		key = pygame.key.get_pressed()

		for tile_object in maps[currentlevel].tmxdata.objects:
			if tile_object.name == 'o':
				if key[pygame.K_c]:
					posBloc = collideBloc.get_rect().move(int(-camera.x * 1024 / camera.w + 512), int(-camera.y * 1024 / camera.w + 383))
					self.blit(collideBloc, (tile_object.x * 1024 / camera.w + posBloc.x, tile_object.y * 768 / camera.h + posBloc.y))
					posBloc = collideBloc.get_rect().move(int(camera.x * 1024 / camera.w - 512), int(camera.y * 1024 / camera.w - 383))

			if not player.keyowned:
				if tile_object.name == 'key':
					top = tile_object.y
					bottom = tile_object.y + sTile
					left = tile_object.x
					right = tile_object.x + sTile
					posKey = keyImg.get_rect().move(int(-camera.x * 1024 / camera.w + 512), int(-camera.y * 1024 / camera.w + 383))
					self.blit(keyImg, (tile_object.x * 1024 / camera.w + posKey.x, tile_object.y * 768 / camera.h + posKey.y))
					posKey = keyImg.get_rect().move(int(-camera.x * 1024 / camera.w + 512), int(-camera.y * 1024 / camera.w + 383))
					if player.position.x + sTile >= left and player.position.x <= right and player.position.y + sTile >= top and player.position.y <= bottom:
						player.key = True

			if tile_object.name.startswith('exit'):
				if tile_object.x <= player.position.x + player.size[0] and tile_object.x + 16 >= player.position.x and tile_object.y <= player.position.y + player.size[1] and tile_object.y + 16 >= player.position.y:
					if int(tile_object.name[4:]) == 2:
						if player.keyowned:
							oldcurrentlevel = currentlevel
							currentlevel = int(tile_object.name[4:])
							Entity.entities = []
							camera = Map.Camera(currentlevel)
							import loadmap
							loadmap.initMatrix(Entity, self, maps[currentlevel], False, oldcurrentlevel)
							return [currentlevel, camera]
					else:
						oldcurrentlevel = currentlevel
						currentlevel = int(tile_object.name[4:])
						Entity.entities = []
						camera = Map.Camera(currentlevel)
						import loadmap
						loadmap.initMatrix(Entity, self, maps[currentlevel], player.keyowned, oldcurrentlevel)
						return [currentlevel, camera]
		return [-1, None]

	def render(self, window, camera):
		self.sprite = pygame.transform.scale(self.sprite, (int(self.size[0] * 1024 / camera.w), int(self.size[1] * 768 / camera.h)))
		width = self.sprite.get_rect().size[0]
		height = self.sprite.get_rect().size[1]
		position = [self.position.x, self.position.y]
		if self.anim < 4:
			self.position = self.position.move(int(-camera.x + (position[0] - camera.x) * (1024 / camera.w - 1) + 512), int(-camera.y + (position[1] - camera.y) * (1024 / camera.w - 1) + 383))
			window.blit(self.sprite, self.position, (0, self.anim * height / len(self.nbAnimsFrames), width / self.maxAnimsFrames, height / len(self.nbAnimsFrames)))
			self.position = self.position.move(int(camera.x - (position[0] - camera.x) * (1024 / camera.w - 1) - 512), int(camera.y - (position[1] - camera.y) * (1024 / camera.w - 1) - 383))
		if self.anim >= 4 and self.anim < 8:
			if Entity.temp % self.pace == 0:
				self.frame = (self.frame + 1) % self.nbAnimsFrames[self.anim]
			self.position = self.position.move(int(-camera.x + (position[0] - camera.x) * (1024 / camera.w - 1) + 512), int(-camera.y + (position[1] - camera.y) * (1024 / camera.w - 1) + 383))
			window.blit(self.sprite, self.position, (self.frame * width / self.maxAnimsFrames, self.anim * height / len(self.nbAnimsFrames), width / self.maxAnimsFrames, height / len(self.nbAnimsFrames)))
			self.position = self.position.move(int(camera.x - (position[0] - camera.x) * (1024 / camera.w - 1) - 512), int(camera.y - (position[1] - camera.y) * (1024 / camera.w - 1) - 383))
			if self.anim == 4:
				self.position = self.position.move(0, self.speed)
			elif self.anim == 5:
				self.position = self.position.move(-self.speed, 0)
			elif self.anim == 6:
				self.position = self.position.move(0, -self.speed)
			elif self.anim == 7:
				self.position = self.position.move(self.speed, 0)
		if self.anim >= 8:
			if Entity.temp % self.pace == 0:
				self.frame += 1
			if self.frame == self.nbAnimsFrames[self.anim]:
				self.frame = 0
				self.anim %= 4
			self.position = self.position.move(int(-camera.x + (position[0] - camera.x) * (1024 / camera.w - 1) + 512), int(-camera.y + (position[1] - camera.y) * (1024 / camera.w - 1) + 383))
			window.blit(self.sprite, self.position, (self.frame * width / self.maxAnimsFrames, self.anim * height / len(self.nbAnimsFrames), width / self.maxAnimsFrames, height / len(self.nbAnimsFrames)))
			self.position = self.position.move(int(camera.x - (position[0] - camera.x) * (1024 / camera.w - 1) - 512), int(camera.y - (position[1] - camera.y) * (1024 / camera.w - 1) - 383))

	def unwalk(self):
		if self.anim >= 4 and self.anim < 8:
			self.anim %= 4
			self.frame = 0
