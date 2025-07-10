import sys
import pygame
import pickle

from my_platform import Platform  # type: ignore
from individual import Individual
from population import Population
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GENERATION_TIME,
    POPULATION_SIZE,
    TRAINING_MODE,
    RANDOM_SEED,
    ONLY_BEST,
)
from helpers import create_platforms, build_platform_index


def main(population_path):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    platforms = create_platforms(seed=RANDOM_SEED)


    if population_path:
        with open(population_path, "rb") as f:
            pop = pickle.load(f)
            if ONLY_BEST:
                best = max(pop.individuals, key=lambda ind: ind.fitness)
                pop.individuals = [best]
        print(f"Loaded population from {population_path}")
    else:
        pop = Population(POPULATION_SIZE)

    running = True
    actions_taken = 0

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

        actions_taken += 1
        if actions_taken > GENERATION_TIME and TRAINING_MODE:
            pop.go_to_next_gen()
            actions_taken = 0

        pygame.font.init()
        font = pygame.font.SysFont("Arial", 24)
        fps = clock.get_fps()
        fps_text = font.render(f"{fps:.1f} FPS", True, (0, 0, 0)) 
        screen.blit(fps_text, (SCREEN_WIDTH - fps_text.get_width() - 10, 10))
        pygame.display.flip()


if __name__ == "__main__":
    population_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(population_path)
