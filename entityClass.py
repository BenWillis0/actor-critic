import random
import math
import pygame

import globalVars as g


class Entity():
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.m = 1

    @staticmethod
    def randVec():
        angle = random.random()*math.pi*2
        return {
            'x': math.sin(angle),
            'y': math.cos(angle)}
    
    def movement(self):
        if random.random() < .005:
            self.vel = self.randVec()
            
        self.normalizeSpeed()
        
        self.x += self.vel['x']
        self.y += self.vel['y']

    def wallCollision(self): # if stuck in walls
        if self.x + self.r + self.vel['x'] >= g.gameWidth or self.x - self.r + self.vel['x'] <= 0:
            self.vel['x'] *= -1

        if self.y + self.r + self.vel['y'] >= g.gameHeight or self.y - self.r + self.vel['y'] <= 0:
            self.vel['y'] *= -1

    def normalizeSpeed(self):
        mag = math.sqrt(self.vel['x']**2 + self.vel['y']**2)
        if mag != 0:
            self.vel['x'] /= mag
            self.vel['y'] /= mag
            self.vel['x'] *= self.speed
            self.vel['y'] *= self.speed


                        
        
    def entityCollision(self, e): # performs elastic collision of 2 circles
        # implementing this equation: https://wikimedia.org/api/rest_v1/media/math/render/svg/f8c2fdb8539aeda1e02fbf46de0f0c35229e76e1
        v1 = math.sqrt(self.vel['x']**2 + self.vel['y']**2)
        v2 = math.sqrt(e.vel['x']**2 + e.vel['y']**2)

        theta1 = math.atan2(self.vel['y'], self.vel['x'])
        theta2 = math.atan2(e.vel['y'], e.vel['x'])

        m1 = self.m
        m2 = e.m

        phi = math.atan2(e.y-self.y,e.x-self.x)

        num1x = v1*math.cos(theta1-phi)*(m1-m2) + 2*m2*v2*math.cos(theta2 - phi)
        num1y = num1x

        self.vel['x'] = (num1x/(m1+m2))*math.cos(phi) + v1*math.sin(theta1-phi)*math.cos(phi + math.pi*0.5)
        self.vel['y'] = (num1y/(m1+m2))*math.sin(phi) + v1*math.sin(theta1-phi)*math.sin(phi + math.pi*0.5)

        num2x = v2*math.cos(theta2-phi)*(m2-m1) + 2*m1*v1*math.cos(theta1 - phi)
        num2y = num2x

        e.vel['x'] = (num2x/(m1+m2))*math.cos(phi) + v2*math.sin(theta2-phi)*math.cos(phi + math.pi*0.5)
        e.vel['y'] = (num2y/(m1+m2))*math.sin(phi) + v2*math.sin(theta2-phi)*math.sin(phi + math.pi*0.5)

    
    
    def draw(self, render):
        if render:
            # draws circle on the screen
            pygame.draw.circle(g.screen,self.c,(round(self.x - g.cameraX), round(self.y - g.cameraY)), self.r)

