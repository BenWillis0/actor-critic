from actorCritic import ActorCritic
import torch
import math
import numpy as np
import pygame
import globalVars as g
import menu
import os
import matplotlib.pyplot as plt

learning_rate = 0.00000001
max_gradient = 1
num_steps = 400
max_episodes = 100000

ENTROPY_BETA = 5e-3

stack_size = 3 # number of frames in buffer
frame_skip_size = 3 # skips 3 frames, so uses every 4th frame

input_shape = [stack_size, g.compressedHeight, g.compressedWidth] # shape of input to neural newtwork

def create_save_dir():
	if not os.path.exists('models'):
		os.makedirs('models')
	dirs = os.listdir('models')
	if dirs == []:
		return 'models/001'
	else:
		return 'models/' + (3 - len(str(int(dirs[-1]) + 1))) * '0' + str(int(dirs[-1]) + 1) # next biggest number

def calc_logprob(mu, var, actions): # returns the log of the probability of choosing an action
	p1 = -((mu - actions) ** 2) / (2*var.clamp(min=1e-3))
	p2 = -torch.log(torch.sqrt(2 * math.pi * var))
	return p1 + p2

def convert_actions(actions): # converts actions chosen by agent to ones that can be taken by the environment
	new_actions = []
	# converts an angle to a vector
	new_actions.append({'x': math.cos(math.pi * actions[0]), 'y': math.sin(math.pi * actions[0])})
	new_actions.append({'x': math.cos(math.pi * actions[1]), 'y': math.sin(math.pi * actions[1])})
	return new_actions

# def convert_actions(actions): # converts actions chosen by agent to ones that can be taken by the environment
# 	return [{'x':actions[0], 'y':actions[1]}, {'x':actions[2], 'y':actions[3]}]

def stack_frames(stacked_frames, frame, stack_size):
	if stacked_frames is None:
		stacked_frames = np.zeros(input_shape)
		for i in range(stack_size): # sets all frames to be the same as first frame
			stacked_frames[i,:,:] = frame
	else:
		stacked_frames[0:stack_size-1,:,:] = stacked_frames[1:,:,:] # shits previous frames to the right and last off
		stacked_frames[stack_size-1,:,:] = frame # adds new frame to the start
	return stacked_frames


class AgentA2C:
	def __init__(self, num_actions, gamma=0.99):
		self.gamma = gamma
		self.num_actions = num_actions
		self.actor_critic = ActorCritic(learning_rate, input_shape, self.num_actions)
		self.n_step_size = 12 # batch size for a collection of stacked frames


	def learn(self, values, log_probs, rewards, vars):
		self.actor_critic.optimiser.zero_grad() # sets gradients to zero, so new gradients aren't added to them

		rewards = torch.tanh(torch.tensor(rewards,dtype=torch.float32)) # fits rewards between -1 and 1, used to improve learning

		returns = []
		R = 0
		# creates discounted sum of rewards for a batch
		for i in range(len(rewards)-1,-1,-1):
			# gamma discounts later rewards because they were less certain when predicting the value of the state
			R = rewards[i] + self.gamma * R
			returns.append(R)
		returns = list(reversed(returns)) # contains real values of each state

		log_probs = torch.stack(log_probs) # combines tensors to 1 tensor
		log_probs = torch.sum(log_probs, dim=1) # sums log probs for each action
		returns = torch.tensor(returns)
		values = torch.tensor(values)
		vars = torch.squeeze(torch.stack(vars)) # reformat vars to a matrix

		advantage = (returns - values).to(self.actor_critic.device) # difference between actual and predicted outcomes
		actor_loss = -(log_probs * advantage).mean()
		critic_loss = -advantage.pow(2).mean() # mean squared error loss
		# entropy of each individual action summed
		# entropy of continuous action is 0.5 * (ln(2*pi*var) + 1)
		entropy_loss = -ENTROPY_BETA * torch.sum(0.5*(torch.log(2*math.pi*vars) + torch.ones_like(vars)))
		total_loss = actor_loss + critic_loss + entropy_loss
		total_loss.backward(retain_graph=True)
		# scales gradients down to stop gradients going to infinity
		torch.nn.utils.clip_grad_norm_(self.actor_critic.parameters(), max_norm=max_gradient, norm_type=2)
		self.actor_critic.optimiser.step()


	def n_steps(self, env, stacked_frames, score, score_history, episode, render):
		values, log_probs, total_rewards, vars = [], [], [], []
		step_count = 0
		while step_count < self.n_step_size:
			rewards = 0
			step_count += 1
			# looks at stack of frames and computes a mean and standard deviation for each action along with the expected value of that state
			mu, var, value = self.actor_critic.forward(stacked_frames)
			sigma = torch.sqrt(var)
			actions = torch.normal(mu.detach(), sigma.detach())[0]  # selects actions from a normal distribution
			actions = torch.tanh(actions)  # keeps actions between -1 and 1
			log_prob = torch.squeeze(calc_logprob(mu, var, actions))
			new_state, reward, done = env.step(convert_actions(actions.cpu().numpy()), render)
			new_stacked_frames = stack_frames(stacked_frames, new_state, stack_size) # add new frame to stack
			for i in range(frame_skip_size): # skip frames
				if not done:
					_, reward, done = env.step([{'x':0,'y':0},{'x':0,'y':0},False],render) # take no action
					rewards += reward
			score += rewards # add collected rewards to episode score

			if done:
				state, _, done = env.reset(render)
				stacked_frames = None # resets frame buffer
				for i in range(frame_skip_size):  # skip frames
					if not done:
						_, _, done = env.step([{'x': 0, 'y': 0}, {'x': 0, 'y': 0}, False], render) # take no action
				stacked_frames = stack_frames(stacked_frames, state, stack_size)  # add first frame to the stack
				print('episode', episode, 'score %.2f' % score)
				score_history.append(score)
				score = 0
				episode += 1
				value *= 0
			else:
				stacked_frames = new_stacked_frames
			rewards += reward
			vars.append(var)
			values.append(value)
			log_probs.append(log_prob)
			total_rewards.append(rewards)
		return values, log_probs, total_rewards, stacked_frames, score, score_history, episode, vars

	def a2c(self, env, train, render):
		if train:
			save_button = pygame.Rect(round(g.button_surface_width / 2 - 100), 25, 200, 75)
			evaluate_button = pygame.Rect(round(g.button_surface_width / 2 - 100), 125, 200, 75)
			menu.training_screen(save_button, evaluate_button)
		stacked_frames = None
		rewards = 0
		score = 0 # total rewards of an episode
		score_history = [] # keeps track of scores from every episode
		episode = 1

		if train:
			max_episodes = 100000
		else:
			max_episodes = 100

		state, reward, done = env.reset(render)
		rewards += reward
		for i in range(frame_skip_size):
			if not done:
				_, reward, done = env.step([{'x': 0, 'y': 0}, {'x': 0, 'y': 0}, False], render)  # skip frames
				rewards += reward
		stacked_frames = stack_frames(stacked_frames, state, stack_size)  # add first frame to the stack
		while episode < max_episodes:
			for event in pygame.event.get():  # keeps window running properly
				if event.type == pygame.QUIT: # lets you close window
					pygame.quit()
					quit()

				xPos, yPos = pygame.mouse.get_pos()
				xPos += -g.screenWidth + g.button_surface_width
				yPos += -g.screenHeight + g.button_surface_height

				if event.type == pygame.MOUSEBUTTONUP:
					if save_button.collidepoint(xPos, yPos):
						torch.save(self.actor_critic.state_dict(),create_save_dir())
					if evaluate_button.collidepoint(xPos, yPos):
						self.evaluate(score_history)



			values, log_probs, rewards, stacked_frames, score, score_history, episode, vars = self.n_steps(env, stacked_frames, score, score_history, episode, render)
			if train:
				self.learn(values, log_probs, rewards, vars)

		self.evaluate(score_history)

	def evaluate(self, score_history):
		plt.plot(score_history)
		plt.ylabel('score')
		plt.xlabel('episode')
		plt.show()
		score_history = np.array(score_history)
		score_average = np.mean(score_history[:(len(score_history) // 100) * 100].reshape(-1, 100), axis=1)
		plt.plot(score_average)
		plt.ylabel('average score')
		plt.xlabel('hundred episodes')
		plt.show()
