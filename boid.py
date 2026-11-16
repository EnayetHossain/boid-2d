from typing import List
from random import randint 
from pygame import Surface, Vector2, draw


class Boid:
    def __init__(self, screen: Surface) -> None:
        self.__pos = Vector2(randint(0, screen.get_size()[0]), randint(0, screen.get_size()[1]))
        self.__velocity = Vector2(0, 0)
        self.__acc = Vector2(0, 0)
        self.__max_speed = 300
        self.__max_force = 300
        self.__screen = screen
        self.__white = (255, 255, 255)
        # self.__light_gray = (18, 18, 18)
        # self.__dark_gray = (10, 10, 10)

        self.__shape = [
                Vector2(0, -10), # head
                Vector2(-10, 15), # bottom left
                Vector2(0, 7.5), # bump in middle bottom
                Vector2(10, 15) # bottom right
                ]

        self.__pr = 100 # persection radius
        self.__sr = 60 # seperation radius

    @property
    def pos(self) -> Vector2:
        return self.__pos

    @property
    def velocity(self) -> Vector2:
        return self.__velocity

    def __get_neighbors(self, boids: List["Boid"]) -> List["Boid"]:
        neighbors: List["Boid"] = []

        for boid in boids:
            if boid is self:
                continue

            if self.__pos.distance_to(boid.pos) < self.__pr:
                neighbors.append(boid)

        return neighbors

    def __separation(self, neighbors: List["Boid"]) -> Vector2:
        direction = Vector2(0, 0)
        total = 0

        for neighbor in neighbors:
            ad = self.__pos - neighbor.pos # avoidence distence
            if 0 < ad.length() < self.__sr:
                ad = ad.normalize()

                weight = 1.0 / ad.length()
                direction += ad * weight
                total += 1

        if total > 0:
            direction /= total

            if direction.length() > 0:
                direction.scale_to_length(self.__max_speed)
                direction -= self.__velocity

                if direction.length() > self.__max_force:
                    direction.scale_to_length(self.__max_force)

        return direction

    def __boundary(self) -> Vector2:
        steering = Vector2(0, 0)
        margin = 10

        width, height = self.__screen.get_size()

        if self.__pos.x < margin:
            steering.x = self.__max_speed

        elif self.__pos.x > width - margin:
            steering.x = -self.__max_speed

        if self.__pos.y < margin:
            steering.y = self.__max_speed
        elif self.__pos.y > height - margin:
            steering.y = -self.__max_speed

        return steering

    def calculate_acceleration(self, boids: List["Boid"]) -> None:
        neighbors = self.__get_neighbors(boids)

        separation_force = self.__separation(neighbors)
        boundary_force = self.__boundary()

        separation_weight = 1.3
        boundary_weight = 2.0

        self.__acc = (separation_force * separation_weight + boundary_force * boundary_weight)

        if self.__acc.length() > self.__max_force:
            self.__acc.scale_to_length(self.__max_force)

    def update(self, dt: float) -> None:
        self.__velocity += self.__acc * dt

        if self.__velocity.length() > self.__max_speed:
            self.__velocity.scale_to_length(self.__max_speed)

        self.__pos += self.__velocity * dt
        self.__acc.update(0, 0)

    def draw(self) -> None:
        angle = self.__velocity.as_polar()[1]
        points = [self.__pos + point.rotate(angle + 90) for point in self.__shape]
        # draw.circle(self.__screen, self.__dark_gray, (self.__pos.x, self.__pos.y), self.__pr)
        # draw.circle(self.__screen, self.__light_gray, (self.__pos.x, self.__pos.y), self.__sr)
        draw.polygon(self.__screen, self.__white, points)
