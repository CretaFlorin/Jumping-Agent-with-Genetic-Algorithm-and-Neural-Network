import pygame
from platform import Platform # type: ignore
from individual import Individual
from population import Population
import time


from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GENERATION_TIME
from helpers import create_platforms


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    platforms = create_platforms(seed=42)

    pop = Population(52)
    start = time.time()

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Make the screen white

        for platform in platforms:
            platform.draw(screen)

        pop.update(screen, platforms)
        pop.draw(screen)

        stop = time.time()
        if stop - start > GENERATION_TIME:
            pop.go_to_next_gen()
            start = time.time()

        pygame.display.flip()


if __name__ == "__main__":
    main()
