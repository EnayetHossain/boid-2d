import math
import random
from typing import List, Tuple

import pygame as pg
from pygame.surface import Surface


class BirdRenderer:
    def __init__(self, screen: Surface) -> None:
        self.__screen = screen

        self.__color = (255, 255, 255)

        # Each bird starts at a different point in its animation.
        self.__phase = random.uniform(0, math.tau)

        self.__flap_speed = 8.0
        self.__wing_span = 12.0

    def update(self, dt: float) -> None:
        self.__phase = (self.__phase + self.__flap_speed * dt) % math.tau

    def __transform_points(self, points: List[pg.Vector2], position: pg.Vector2, angle: float) -> List[Tuple[int, int]]:
        transformed = []

        for point in points:
            rotated = point.rotate(-angle)
            world_point = position + rotated

            transformed.append((round(world_point.x), round(world_point.y)))

        return transformed

    def draw( self, position: pg.Vector2, velocity: pg.Vector2) -> None:
        # Keep the bird's orientation when it is almost stationary.
        if velocity.length_squared() > 0.0001:
            angle = velocity.angle_to(pg.Vector2(1, 0))
        else:
            angle = 0.0

        # Calculate the current wing position.
        flap = math.sin(self.__phase)

        wing_span = (
            self.__wing_span * (0.5 + 0.5 * flap)
        )

        # Upper wing.
        upper_wing = [
            pg.Vector2(1, -1),
            pg.Vector2(-3, -2),
            pg.Vector2(-10, -wing_span),
            pg.Vector2(-6, -2),
        ]

        # Lower wing.
        lower_wing = [
            pg.Vector2(1, 1),
            pg.Vector2(-3, 2),
            pg.Vector2(-10, wing_span),
            pg.Vector2(-6, 2),
        ]

        # Body and beak.
        body = [
            pg.Vector2(12, 0),
            pg.Vector2(7, -2),
            pg.Vector2(1, -2),
            pg.Vector2(-6, -1),
            pg.Vector2(-10, 0),
            pg.Vector2(-6, 1),
            pg.Vector2(1, 2),
            pg.Vector2(7, 2),
        ]

        # Draw wings first so the body appears on top.
        upper_points = self.__transform_points(
            upper_wing, position, angle
        )

        lower_points = self.__transform_points(
            lower_wing, position, angle
        )

        body_points = self.__transform_points(
            body, position, angle
        )

        pg.draw.polygon(
            self.__screen, self.__color, upper_points
        )

        pg.draw.polygon(
            self.__screen, self.__color, lower_points
        )

        pg.draw.polygon(
            self.__screen, self.__color, body_points
        )
