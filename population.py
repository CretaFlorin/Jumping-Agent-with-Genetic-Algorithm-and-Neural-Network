import random
from constants import SCREEN_WIDTH as WIDTH, SCREEN_HEIGHT as HEIGHT, FPS
from individual import Individual
import numpy as np

class Population:
    def __init__(self, size):
        self.individuals = []
        self.size = size
        self.generation = 1
        
        for _ in range(size):
            x = random.randint(50, WIDTH - 50)
            y = HEIGHT - 100
            self.individuals.append(Individual(x, y))
            
    def update(self, screen, platforms):
        for individual in self.individuals:
            
            vision = individual.sense_environment(screen, platforms)
            result = individual.brain.forward(vision)
            # 0 - jump
            # 1 - left
            # 2 - right
            
            action = np.argmax(result)
            jump, left, right = False, False, False
            if action == 0:
                jump = True
            if action == 1:
                left = True
            if action == 2:
                right = True

            individual.move(jump=jump, left=left, right=right)
            
            individual.update(platforms)
    
    def draw(self, screen):
        for individual in self.individuals:
            individual.draw(screen)
            
    def reproduce(self, elites):
        new_gen = []
        for i in range(0, len(elites), 2):
            parent1, parent2 = elites[i], elites[i+1]
            child1, child2 = parent1.crossover(parent2)
            new_gen.append(child1)
            new_gen.append(child2)
            
        for i in range(0, len(elites) // 2):
            parent1, parent2 = elites[i], elites[len(elites) - i - 1]
            child1, child2 = parent1.crossover(parent2)
            new_gen.append(child1)
            new_gen.append(child2)
            
        return new_gen
            
    def go_to_next_gen(self):
        # luam jumatatea din populatie care s-a adaptat mai bine la environment
        elites = sorted(self.individuals, key=lambda ind: ind.fitness)[-27: -1]
        
        new_generation = self.reproduce(elites)
        
        self.generation += 1
        self.individuals = new_generation
        print("GEN:", self.generation)
        
        