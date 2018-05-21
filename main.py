#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pygame, math, copy, sys
from pygame.locals import *
from Map import *
import Menu
from Entity import Entity
sys.path.insert(0, "Entity")
sys.path.insert(0, "Entity/Human")
sys.path.insert(0, "Menu")
sys.path.insert(0, "HUD")
import Dialog
import Player
import Human
import Enemy
import Button

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Kill the Anthony 2")
popsound = pygame.mixer.Sound("textures/hud/pop.wav")
m = False


window = pygame.display.set_mode((1024, 768))

def f():
	Menu.Menu.menustate = 0
button1 = Button.Button(380, 300, 250, 70, "textures/menu/button.png", "textures/menu/INVASION2000.TTF", 48, "Play", f, -1, -1, 1, -1)
def f():
	exit()
button2 = Button.Button(380, 500, 250, 70, "textures/menu/button.png", "textures/menu/INVASION2000.TTF", 48, "Quit", f, 0, -1, -1, -1)

menu = Menu.Menu([button1, button2], "textures/menu/background/")

currentlevel = 1
map1 = Map('textures/tmx/level{}.tmx'.format(currentlevel))
map_img = map1.make_map()

player = Player.Player(1000, 500, "textures/link.png", [1, 1, 1, 1, 10, 10, 10, 10], 5)
camera = Camera(0, 0, 500)
npc = Enemy.Enemy(864, 192, "textures/link.png", [1, 1, 1, 1, 10, 10, 10, 10], 5, player, [[896, 240], [976, 240], [976, 320], [896, 320]])
Entity.initMatrix(Entity, map1)
dCount = 0

script = "scripts/script.txt"
dialog = Dialog.Dialog(40, script, dCount)
clock = pygame.time.Clock()

windowOpen = True
while windowOpen:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_g:
				m = False

	key = pygame.key.get_pressed()

	if key[pygame.K_ESCAPE]:
		Menu.Menu.menustate = 1

	if Menu.Menu.menustate == 0:
		camera.x = player.position.x
		camera.y = player.position.y

		map_img = pygame.transform.scale(map_img, (int(1600 * 1024 / camera.w), int(1600 * 1024 / camera.w)))
		posmap = map_img.get_rect()

		posmap = posmap.move(int(-camera.x * 1024 / camera.w + 512), int(-camera.y * 1024 / camera.w + 383))
		window.blit(map_img, posmap)
		posmap = posmap.move(int(camera.x * 1024 / camera.w - 512), int(camera.y * 1024 / camera.w - 383))

		Entity.draw(window, camera)
		Entity.collider(window, map1, map_img, player, currentlevel)
	else:
		Menu.Menu.menus[Menu.Menu.menustate - 1].draw(window)
	if key[pygame.K_g]:
		if not m:
			popsound.play()
			dCount += 1
			m = True
		if dCount <= dialog.maxLines():
			Dialog.Dialog(40, script, dCount).box(window)
	pygame.display.flip()

	clock.tick(144)
