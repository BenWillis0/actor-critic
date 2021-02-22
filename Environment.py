import pygame
import random
import math
import numpy as np

from playerClass import Player
from zombieClass import Zombie
from humanClass import Human
from bulletClass import Bullet
import globalVars as g

numZombies = 1
numHumans = 1


def checkZombieSpawn(x, y, r):  # Checks zombies dont spawn in the same pos
	for z in g.zombies:
		if math.sqrt((z.x - x) ** 2 + (z.y - y) ** 2) <= r + z.r:
			x = r + g.gameWidth * 0.6 + (g.gameWidth * 0.4 - 2 * r) * random.random() # keeps zombies in right 40% of map
			y = r + (g.gameHeight - 2 * r) * random.random()
			checkZombieSpawn(x, y, r)

	return x, y


def checkHumanSpawn(x, y, r):  # Checks zombies dont spawn in the same
	for h in g.humans:
		if math.sqrt((h.x - x) ** 2 + (h.y - y) ** 2) <= r + h.r:
			x = r + (g.gameWidth * 0.4 - 2 * r) * random.random() # keeps humans in left 40% of map
			y = r + (g.gameHeight - 2 * r) * random.random()
			checkHumanSpawn(x, y, r)

	return x, y

def checkSpawn(x, y, r):
	for h in g.humans:
		if math.sqrt((h.x - x) ** 2 + (h.y - y) ** 2) <= r + h.r:
			x = r + (g.gameWidth - 2 * r) * random.random()
			y = r + (g.gameHeight - 2 * r) * random.random()
			checkSpawn(x, y, r)

	for z in g.zombies:
		if math.sqrt((z.x - x) ** 2 + (z.y - y) ** 2) <= r + z.r:
			x = r + (g.gameWidth - 2 * r) * random.random()
			y = r + (g.gameHeight - 2 * r) * random.random()
			checkSpawn(x, y, r)

	if math.sqrt((g.player.x - x) ** 2 + (g.player.y - y) ** 2) <= r + g.player.r:
		x = r + (g.gameWidth - 2 * r) * random.random()
		y = r + (g.gameHeight - 2 * r) * random.random()
		checkSpawn(x, y, r)

	return x, y

def shootBullet(bulletVec):
    g.bullets[0].fired = True
    g.bullets[0].setVel(bulletVec)
    x = g.player.x
    y = g.player.y
    r = 7
    c = (100, 100, 100)
    g.bullets.insert(0, Bullet(x, y, r, c))

def greyscale(img):
	# combines rgb values by scaled amounts to create a single greyscale value
	return np.dot(img[..., :3], [0.2989, 0.5870, 0.1140]) / 255


class Environment:

	# action - [moveVec, bulletVec, shootBullet]
	def step(self, action, render):
		reward = -.01
		game_over = g.player.update(action[0], render)
		if action[1]['x'] != 0 or action[1]['y'] != 0: # checks to see its not a zero vector
			shootBullet(action[1])
		for b in g.bullets:
			reward += b.update(render)
			if b.timer > 1000:  # delete bullet after 1000 ticks
				g.bullets.remove(b)
		for z in g.zombies:
			z.update(render)
		for h in g.humans:
			h.update(render)

		if len(g.zombies) == 0:
			game_over = True
			g.win = True

		if len(g.humans) == 0:
			game_over = True
			g.loss = True

		# scales image to smaller size
		surf = pygame.transform.scale(g.screen, (g.compressedWidth, g.compressedHeight))
		state = pygame.surfarray.array3d(surf) # converts pygame surface to numpy array of pixel values
		state = np.array(greyscale(state)).T # converts image to greyscale and transposes so screen orientated correctly


		if render:
			g.main_screen.blit(g.screen, (0, 0))
			g.main_screen.blit(g.button_screen, (g.screenWidth-g.button_surface_width, g.screenHeight-g.button_surface_height))
			pygame.display.update()
			g.screen.fill((0, 0, 0))
			pygame.draw.rect(g.screen, (255, 255, 255), ((int(-g.cameraX), int(-g.cameraY)), (int(g.gameWidth), int(g.gameHeight))))
		else:
			g.main_screen.blit(g.button_screen, (0, 0))
			pygame.display.update()
		return state, reward, game_over



	def reset(self, render):  # initializes entities
		g.cameraX = g.gameWidth / 2 - g.screenWidth / 2 # reset camera
		g.cameraY = g.gameHeight / 2 - g.screenHeight / 2

		g.screen.fill((0, 0, 0))
		pygame.draw.rect(g.screen, (255, 255, 255), ((int(-g.cameraX), int(-g.cameraY)), (int(g.gameWidth), int(g.gameHeight))))

		x = g.gameWidth / 2
		y = g.gameHeight / 2
		r = 20
		c = (255, 0, 0)

		g.player = Player(x, y, r, c)

		g.bullets = []
		r = 7
		c = (100, 100, 100)
		g.bullets.append(Bullet(x, y, r, c))

		g.zombies = []
		for i in range(numZombies):
			r = 20
			x = r + (g.gameWidth - 2 * r) * random.random()
			y = r + (g.gameHeight - 2 * r) * random.random()
			x, y = checkSpawn(x, y, r)
			c = (0, 128, 0)
			g.zombies.append(Zombie(x, y, r, c))

		g.humans = []
		for i in range(numHumans):
			r = 20
			x = r + (g.gameWidth - 2 * r) * random.random()
			y = r + (g.gameHeight - 2 * r) * random.random()
			x, y = checkSpawn(x, y, r)
			c = (255, 105, 180)
			g.humans.append(Human(x, y, r, c))
		return self.step([{'x':0,'y':0},{'x':0,'y':0},False], render)