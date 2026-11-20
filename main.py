from collections import defaultdict
from typing import DefaultDict, List, Tuple
import pygame as pg
import time
from boid import Boid, Cell, SpatialGrid

# Cell = Tuple[int, int]
# SpatialGrid = Dict[Cell, List["Boid"]]

class Game:
    def __init__(self, size: Tuple[int, int]) -> None:
        pg.init()
        self.__screen = pg.display.set_mode(size)
        pg.display.set_caption("Boids")

        self.__clock = pg.time.Clock()
        self.__running = True
        self.__boids = [Boid(self.__screen) for _ in range(100)]

    def __build_spatial_gird(self) -> SpatialGrid:
        grid: DefaultDict[Cell, List[Boid]] = defaultdict(list)

        cell_size = 100
        for boid in self.__boids:
            cell_x = int(boid.pos.x // cell_size)
            cell_y = int(boid.pos.y // cell_size)

            grid[(cell_x, cell_y)].append(boid)

        return grid

    def __handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.__running = False

    def run(self) -> None:
        prev_time = time.perf_counter()

        while self.__running:
            now = time.perf_counter()
            dt = now - prev_time
            prev_time = now

            self.__handle_events()

            self.__screen.fill("black")

            grid = self.__build_spatial_gird()

            for boid in self.__boids:
                boid.calculate_acceleration(grid)

            for boid in self.__boids:
                boid.update(dt)

            for boid in self.__boids:
                boid.draw()

            pg.display.flip()

            self.__clock.tick()
            pg.display.set_caption(f"Boids: {self.__clock.get_fps():.1f}")

        pg.quit()

if __name__ == "__main__":
    game = Game((800, 600))
    game.run()
