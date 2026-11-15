from typing import Tuple
import pygame as pg
from boid import Boid

class Game:
    def __init__(self, size: Tuple[int, int]) -> None:
        pg.init()
        self.__screen = pg.display.set_mode(size)
        self.__clock = pg.time.Clock()
        self.__running = True
        self.__boids = [Boid(self.__screen) for _ in range(100)]

    def __handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.__running = False

    def run(self) -> None:
        while self.__running:
            dt = self.__clock.tick() / 1000.0
            self.__handle_events()

            self.__screen.fill("black")

            for boid in self.__boids:
                boid.calculate_acceleration(self.__boids)

            for boid in self.__boids:
                boid.update(dt)

            for boid in self.__boids:
                boid.draw()

            pg.display.flip()

            pg.display.set_caption(f"Boids - FPS: {self.__clock.get_fps():.1f}")

        pg.quit()

if __name__ == "__main__":
    game = Game((1000,750))
    game.run()
