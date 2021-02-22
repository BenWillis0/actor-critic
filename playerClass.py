import globalVars as g
from entityClass import Entity

class Player(Entity):
    def __init__(self, x, y, r, c):
        super().__init__(x, y, r, c)
        self.speed = 3

    def update(self, direction, render):
        self.movement(direction)
        game_over = self.zombieCollision()
        self.draw(render)
        return game_over

    def zombieCollision(self):
        game_over = False
        for z in g.zombies:
            if g.dist(self,z) <= self.r + z.r:
                g.loss = True
                game_over = True
        return game_over

    def movement(self, direction):
        self.vel = {'x': direction['x']*self.speed, 'y': direction['y']*self.speed}

        self.normalizeSpeed()

        if self.x + self.r + self.vel['x'] > g.gameWidth or self.x - self.r + self.vel['x'] < 0:
            self.vel['x'] = 0
        if self.y + self.r + self.vel['y'] > g.gameHeight or self.y - self.r + self.vel['y'] < 0:
            self.vel['y'] = 0

        
        self.x += self.vel['x']
        self.y += self.vel['y']
        g.cameraX += self.vel['x']
        g.cameraY += self.vel['y']
        

