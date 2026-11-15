import random
from typing import List
import pygame as pg
from pygame.surface import Surface
from bird import BirdRenderer


class Boid:
    def __init__(self, screen: Surface) -> None:
        self.__pos = pg.math.Vector2(random.randint(0, screen.get_size()[0]), random.randint(0, screen.get_size()[1]))
        # Velocity and max_speed are now in pixels per second
        self.__velocity = pg.math.Vector2(random.randint(-500, 500), random.randint(-500, 500))
        self.__acc = pg.math.Vector2(0, 0)
        self.__max_speed = 600
        self.__max_force = 400

        self.__pr = 100 # perception radius
        self.__sr = 60 # separation radius

        self.__screen = screen

        self.__renderer = BirdRenderer(screen) 
        # self.__white = (255, 255, 255)

    @property
    def pos(self) -> pg.math.Vector2:
        return self.__pos

    @property
    def velocity(self) -> pg.math.Vector2:
        return self.__velocity

    def get_neighbors(self, boids: List["Boid"]) -> List["Boid"]:
        neighbors: List["Boid"] = []

        for neighbor in boids:
            if neighbor is self:
                continue

            distence = self.__pos.distance_to(neighbor.pos)
            if distence < self.__pr:
                neighbors.append(neighbor)

        return neighbors

    def separate(self, neighbors: List["Boid"]) -> pg.math.Vector2:
        steering = pg.math.Vector2(0, 0)
        total = 0

        for neighbor in neighbors:
            ad = self.__pos - neighbor.pos # Avoidence direction vector of each boid
            direction = ad.length()

            if 0 < direction < self.__sr:
                ad = ad.normalize()

                weight = 1.0 / direction
                steering += ad * weight
                total += 1

        if total > 0:
            steering /= total

            if steering.length() > 0:
                steering.scale_to_length(self.__max_speed)
                steering -= self.__velocity # steering is the desired velocity: Steering = desired velocity - current velocity

                if steering.length() > self.__max_force:
                    steering.scale_to_length(self.__max_force)

        return steering

    def alignment(self, neighbors: List["Boid"]) -> pg.math.Vector2:
        avg_vel = pg.math.Vector2(0, 0)

        for neighbor in neighbors:
            avg_vel += neighbor.velocity

        if len(neighbors) > 0:
            avg_vel /= len(neighbors)

            if avg_vel.length() > 0:
                desired_vel = avg_vel.normalize() * self.__max_speed

                steering = desired_vel - self.__velocity

                if steering.length() > self.__max_force:
                    steering.scale_to_length(self.__max_force)

                return steering

        return avg_vel

    def cohesion(self, neighbors: List["Boid"]) -> pg.math.Vector2:
        center_of_mass = pg.math.Vector2(0, 0)

        if not neighbors:
            return pg.math.Vector2(0, 0)

        for neighbor in neighbors:
            center_of_mass += neighbor.pos

        center_of_mass /= len(neighbors)
        desired_val = center_of_mass - self.__pos

        if desired_val.length_squared() == 0:
            return pg.math.Vector2(0, 0)

        desired_val = desired_val.normalize() * self.__max_speed
        steering = desired_val - self.__velocity

        if steering.length() > self.__max_force:
            steering.scale_to_length(self.__max_force)

        return steering

    def boundaries(self) -> pg.math.Vector2:
        steering = pg.math.Vector2(0, 0)

        margin = 80
        turn_strength = self.__max_speed

        width, height = self.__screen.get_size()

        if self.__pos.x < margin:
            steering.x = turn_strength

        elif self.__pos.x > width - margin:
            steering.x = -turn_strength

        if self.__pos.y < margin:
            steering.y = turn_strength

        elif self.__pos.y > height - margin:
            steering.y = -turn_strength

        if steering.length_squared() > 0:
            steering = steering.normalize() * self.__max_speed
            steering -= self.__velocity

            if steering.length() > self.__max_force:
                steering.scale_to_length(self.__max_force)

        return steering

    def calculate_acceleration(self, boids: List["Boid"]) -> None:
        neighbors = self.get_neighbors(boids)

        separation_force = self.separate(neighbors)
        alignment_force = self.alignment(neighbors)
        cohesion_force = self.cohesion(neighbors)
        boundary_force = self.boundaries()

        separation_weight = 1.3
        alignment_weight = 1.2
        cohesion_weight = 1.0
        boundary_weight = 2.0

        self.__acc = (
                separation_force * separation_weight 
                + alignment_force * alignment_weight 
                + cohesion_force * cohesion_weight
                + boundary_force * boundary_weight
                )

        if self.__acc.length() > self.__max_force:
            self.__acc.scale_to_length(self.__max_force)


    def update(self, dt: float) -> None:
        self.__velocity += self.__acc * dt

        if self.__velocity.length() > self.__max_speed:
            self.__velocity.scale_to_length(self.__max_speed)

        self.__pos += self.__velocity * dt
        self.__acc.update(0, 0)
        self.__renderer.update(dt)

    def draw(self) -> None:
        # angle = self.__velocity.angle_to(pg.math.Vector2(1, 0))
        # points = [self.__pos + point.rotate(-angle) for point in self.__shape]
        # pg.draw.polygon(self.__screen, self.__white, points)
        self.__renderer.draw(self.__pos, self.__velocity)
