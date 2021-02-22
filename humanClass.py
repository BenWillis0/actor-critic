from entityClass import Entity
import globalVars as g

class Human(Entity):
    def __init__(self, x, y, r, c):
        super().__init__(x,y,r,c)
        self.speed = 2.5
        self.vel = self.randVec()
        self.stuck = False

    def playerCollision(self):
        if g.dist(self, g.player) <= self.r + g.player.r:
            dx = g.player.x - self.x
            dy = g.player.y - self.y
            self.vel['x'] -= 2*dx
            self.vel['y'] -= 2*dy

    def humanCollision(self):
        for h in g.humans:
            if h != self:
                if g.dist(self, h) <= self.r + h.r:
                    self.entityCollision(h)

    def innerCollision(self):
        stuck = False
        for h in g.humans:
            if h!= self:
                if g.dist(self, h) < self.r + h.r:
                    self.stuck = True
                    self.vel['x'] = self.x - h.x
                    self.vel['y'] = self.y - h.y
                    self.normalizeSpeed()
                    stuck = True
        if not stuck:
            self.stuck = False
  

    def update(self, render):
        self.movement()
        self.wallCollision()
        self.humanCollision()
        self.innerCollision()
        self.playerCollision()
        self.draw(render)
