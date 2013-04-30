import math

from vector import Vector3

class Command:
    def __init__(self):
        pass

    def tick(self, dt):
        pass

class Move(Command):
    def __init__(self, ent, dest):
        self.ent = ent
        self.dest = dest

        self.threshold = 0.1

    # Orient entity towards the point and move to it
    def tick(self, dt):
        # Heading
        moveDir = self.ent.pos - self.dest
        self.ent.desiredHeading = math.pi/2 + math.atan2(moveDir.x, moveDir.z)

        # Velocity
        # Figure out stopping distance
        stopDist = self.ent.speed/(2*self.ent.acceleration*dt)
        if self.ent.pos.distance(self.dest) > stopDist:
            self.ent.desiredSpeed = self.ent.maxSpeed
        else:
            self.ent.desiredSpeed = 0

class Follow(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target
        self.stopDist = 100

    # Orient entity towards the point and move to it
    def tick(self, dt):
        self.dest = self.target.pos

        # Heading
        moveDir = self.ent.pos - self.dest
        self.ent.desiredHeading = math.pi/2 + math.atan2(moveDir.x, moveDir.z)

        # Velocity
        # Figure out stopping distance
        stopDist = self.ent.speed/(2*self.ent.acceleration*dt)
        if self.ent.pos.distance(self.dest)-self.stopDist > stopDist:
            self.ent.desiredSpeed = self.ent.maxSpeed
        else:
            self.ent.desiredSpeed = 0

class Intercept(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target

    # Orient entity towards the point and move to it
    def tick(self, dt):
        self.dest = self.target.pos

        # Time to intercept
        relativeSpeed = (self.target.vel - self.ent.vel).length()
        distance = self.ent.pos.distance(self.target.pos)
        if relativeSpeed != 0:
            time = distance/relativeSpeed
        else:
            time = 9999999

        # Target's projected location
        self.dest = self.target.pos + self.target.vel * time

        # Heading
        moveDir = self.ent.pos - self.dest
        self.ent.desiredHeading = math.pi/2 + math.atan2(moveDir.x, moveDir.z)

        # Velocity
        # Figure out stopping distance
        stopDist = self.ent.speed/(2*self.ent.acceleration*dt)
        if self.ent.pos.distance(self.dest) > stopDist:
            self.ent.desiredSpeed = self.ent.maxSpeed
        else:
            self.ent.desiredSpeed = 0



