import globalVars as g
from entityClass import Entity

class Zombie(Entity):
    def __init__(self, x, y, r, c):
        super().__init__(x, y, r, c)
        self.speed = 2
        self.vel = self.randVec()
        self.followRad = 200
        self.following_humans = False
        self.following_player = False
        self.stuck = False

    def update(self, render):
        self.followHumans()
        self.followPlayer()
        self.innerCollision() # unsticks zombies that have been pushed together
        self.wallCollision() # pushes out of walls when stuck
        self.infectHumans()
        if self.following_player or self.following_humans:
            self.x += self.vel['x']
            self.y += self.vel['y']
        else:
            self.movement()
        self.draw(render)


        # if not self.following:
        #     self.movement()
        # self.wallCollision()
        # self.followHumans()
        # self.infectHumans()
        # if not self.stuck:
        #     self.followPlayer()
        #     self.zombieCollision()
        # self.innerCollision()
        # self.draw(render)

    def infectHumans(self):
        for i, h in enumerate(g.humans):
            if g.dist(self, h) < self.r + h.r:
                g.zombies.append(Zombie(h.x,h.y,h.r,self.c))
                g.humans.pop(i)
                g.humansToZombie += 1
                i -= 1

    def followHumans(self):
        follow = False
        for h in g.humans: # loops through humans
            if g.dist(self, h) <= self.followRad: # if any other humans are close enough
                self.vel['x'] = h.x - self.x
                self.vel['y'] = h.y - self.y
                self.normalizeSpeed()
                follow = True
                break
                
        if follow == False and self.following_humans: # if no longer following
            self.vel = self.randVec()
        if not follow:
            self.following_humans = False
        if follow:
            self.following_humans = True


    def zombieCollision(self):
        for z in g.zombies:
            if z!= self:
                if g.dist(self, z) <= self.r + z.r:
                    self.entityCollision(z)

    def followPlayer(self):
        follow = False
        if g.dist(self, g.player) <= self.followRad:
            self.vel['x'] = g.player.x - self.x
            self.vel['y'] = g.player.y - self.y
            self.normalizeSpeed()
            follow = True

        if follow == False and self.following_player: # if no longer following
            self.vel = self.randVec()
        if not follow:
            self.following_player = False
        if follow:
            self.following_player = True


    def innerCollision(self):
        stuck = False
        for z in g.zombies:
            if z!= self:
                if g.dist(self, z) < self.r + z.r: # if inside another zombie
                    self.stuck = True
                    self.vel['x'] = self.x - z.x
                    self.vel['y'] = self.y - z.y
                    self.normalizeSpeed()
                    stuck = True
        if not stuck:
            self.stuck = False
