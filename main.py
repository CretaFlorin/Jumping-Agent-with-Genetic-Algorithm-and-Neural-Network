import pygame
from platform import Platform
from individual import Individual
from population import Population
import time

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    platforms = [
        Platform(0, SCREEN_HEIGHT // 3 + 100, SCREEN_WIDTH // 4 + 100, 50),
        Platform(SCREEN_WIDTH // 8, 2 * SCREEN_HEIGHT // 3 + 100, SCREEN_WIDTH // 4 + 100, 50),
        Platform(SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + 100, SCREEN_WIDTH // 4 + 100, 50),
        Platform(3*SCREEN_WIDTH//8, SCREEN_HEIGHT // 6 - 50, SCREEN_WIDTH // 4, 50),
        Platform(SCREEN_WIDTH - 3*SCREEN_WIDTH // 8, 2 * SCREEN_HEIGHT // 3 + 100, SCREEN_WIDTH // 4 + 100, 50),
    ]
    
    pop = Population(52)
    start = time.time()

    running = True
    
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255)) # Make the screen white
        
        for platform in platforms:
            platform.draw(screen)
        
        pop.update(screen, platforms)
        pop.draw(screen)
        
        stop = time.time()
        if stop - start > 6:
            pop.go_to_next_gen()
            start = time.time()
        
        pygame.display.flip()



if __name__ == "__main__":
    main()