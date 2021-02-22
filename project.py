import pygame

import globalVars as g
import menu as menu
from Environment import Environment
from actorCriticAgent import AgentA2C
import torch

num_actions = 2

env = Environment()
agent = AgentA2C(num_actions)

run = True
menuScore = 0
clock = pygame.time.Clock()
game_over = False

DIRECTION = {'x': 0, 'y': 0}

render = True

env.reset(False)

model_loaded = False
model_n = 0

def calcBulletVec(mousePos):
	return {'x': mousePos[0] - g.bullets[0].x, 'y': mousePos[1] - g.bullets[0].y}


while run:
	if menuScore == 0:
		play_button = pygame.Rect(int(g.screenWidth / 2 - 350), int(g.screenHeight / 2 - 50), 200, 75)
		train_button = pygame.Rect(int(g.screenWidth / 2 - 100), int(g.screenHeight / 2 - 50), 200, 75)
		load_button = pygame.Rect(int(g.screenWidth / 2 + 150), int(g.screenHeight / 2 - 50), 200, 75)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			xPos, yPos = pygame.mouse.get_pos()

			if event.type == pygame.MOUSEBUTTONUP:
			    if play_button.collidepoint(xPos, yPos):
			        menuScore = 1

			    if train_button.collidepoint(xPos, yPos):
			        menuScore = 2

			    if load_button.collidepoint(xPos, yPos):
				    menuScore = 3

		menu.startScreen(play_button, train_button, load_button)
	elif menuScore == 1:
		if not game_over:
			pygame.draw.rect(g.screen, (255, 255, 255), ((int(-g.cameraX), int(-g.cameraY)), (int(g.gameWidth), int(g.gameHeight))))
			shootBullet = False
			for event in pygame.event.get():
			    if event.type == pygame.QUIT:
			        quit()

			    xPos, yPos = pygame.mouse.get_pos()
			    xPos += g.cameraX
			    yPos += g.cameraY


			    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			        shootBullet = True

			    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			        shootBullet = True

			    if event.type == pygame.KEYDOWN:
			        if event.key == pygame.K_w:
			            DIRECTION['y'] = -1

			    if event.type == pygame.KEYUP:
			        if event.key == pygame.K_w or event.key == pygame.K_s:
			            DIRECTION['y'] = 0

			    if event.type == pygame.KEYDOWN:
			        if event.key == pygame.K_s:
			            DIRECTION['y'] = 1

			    if event.type == pygame.KEYDOWN:
			        if event.key == pygame.K_d:
			            DIRECTION['x'] = 1

			    if event.type == pygame.KEYUP:
			        if event.key == pygame.K_d or event.key == pygame.K_a:
			            DIRECTION['x'] = 0

			    if event.type == pygame.KEYDOWN:
			        if event.key == pygame.K_a:
			            DIRECTION['x'] = -1

			gun_vec = {'x': 0,'y': 0}
			if shootBullet:
				gun_vec = calcBulletVec([xPos, yPos])
			action = [DIRECTION, gun_vec, shootBullet]
			_, _, game_over = env.step(action, render)
			clock.tick(60)
		else:  # end screen
			for event in pygame.event.get():
			    if event.type == pygame.QUIT:
			        quit()

			menu.endScreen()
			pygame.display.update()

	elif menuScore == 2:
		agent.a2c(env, True, render)

	elif menuScore == 3:
		train_test_buttons = []
		if model_loaded:
			train_test_buttons = menu.train_test()
		else:
			buttons = menu.load_model()
		for event in pygame.event.get():  # keeps window running properly
			if event.type == pygame.QUIT:  # lets you close window
				pygame.quit()
				quit()
			xPos, yPos = pygame.mouse.get_pos()

			for i in range(len(buttons)):
				if buttons[i].collidepoint(xPos, yPos):
					if event.type == pygame.MOUSEBUTTONUP:
						model_loaded = True
						model_n = i+1

			if model_loaded:
				for i in range(len(train_test_buttons)):
					if event.type == pygame.MOUSEBUTTONUP:
						if train_test_buttons[i].collidepoint(xPos, yPos):
							# loads parameters to new model
							agent.actor_critic.load_state_dict(torch.load('models/' + (3 - len(str(model_n))) * '0' + str(model_n)))
							agent.actor_critic.eval()
							if i == 0: # train
								agent.a2c(env, True, render)
							elif i == 1: #test
								agent.a2c(env, False, render)

