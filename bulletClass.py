from entityClass import Entity
import globalVars as g

class Bullet(Entity):
    def __init__(self, x, y, r, c):
        super().__init__(x,y,r,c)
        self.vel = {'x':0, 'y':0}
        self.speed = 7
        self.fired = False
        self.timer = 0

    def movement(self):
        self.normalizeSpeed()
        
        self.x += self.vel['x']
        self.y += self.vel['y']

    def followPlayer(self):
        self.x = g.player.x
        self.y = g.player.y

    def setVel(self, bulletVec):
        self.vel = bulletVec
        self.normalizeSpeed()

    def kill(self):
        reward = 0
        for i,z in enumerate(g.zombies):
            if g.dist(self, z) <= self.r + z.r:
                g.zombies.remove(z)
                g.zombiesDead += 1
                reward += 1
                break
        for i,h in enumerate(g.humans):
            if g.dist(self, h) <= self.r + h.r:
                g.humans.remove(h)
                g.humansDead += 1
                reward -= 1
                break
        return reward

    def update(self,render):
        reward = 0
        if self.fired:
            self.movement()
            reward += self.kill()
            self.timer += 1
        else:
            self.followPlayer()
        self.draw(render)
        return reward