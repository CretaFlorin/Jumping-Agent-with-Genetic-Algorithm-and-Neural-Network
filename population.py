import random
from constants import SCREEN_WIDTH as WIDTH, SCREEN_HEIGHT as HEIGHT, VISION_DIRS, FRAMES_PER_VISION
from individual import Individual
import numpy as np
import pickle
import os

class Population:
    def __init__(self, size):
        self.individuals = []
        self.size: int = size
        self.generation = 1
        self.frame_count = 0
        
        for _ in range(size):
            x = random.randint(50, WIDTH - 50)
            y = HEIGHT 
            self.individuals.append(Individual(x, y))
            
    def update(self, screen, platforms, platform_index):
        sense_now = (self.frame_count % FRAMES_PER_VISION == 0)
        self.frame_count += 1

        for individual in self.individuals:
            if sense_now or individual.vision is None:
                # print("CALLING SENSE")
                individual.sense_environment(screen, platforms)

            # print(len(individual.vision))

            if len(individual.vision) != individual.brain.input_size:
                print(f"[WARN] vision size mismatch: {len(individual.vision)} (expected {individual.brain.input_size})")
                individual.vision = [0] * individual.brain.input_size

            result = individual.brain.forward(individual.vision)

            # result = individual.brain.forward([0]*len(VISION_DIRS))
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
            individual.update(platforms, screen)
    
    def draw(self, screen):
        for individual in self.individuals:
            individual.draw(screen)
            
    # def reproduce(self, elites, mutation_chance=0.1):
    #     new_gen = []

    #     # Pairwise crossover
    #     for i in range(0, len(elites), 2):
    #         if i + 1 >= len(elites):
    #             break  # Skip if odd number of elites
    #         parent1, parent2 = elites[i], elites[i + 1]
    #         child1, child2 = parent1.crossover(parent2)

    #         # Set mutant flags and mutate if needed
    #         child1.mutant = random.random() < mutation_chance
    #         child2.mutant = random.random() < mutation_chance
    #         if child1.mutant:
    #             child1.mutate()
    #         if child2.mutant:
    #             child2.mutate()

    #         new_gen.extend([child1, child2])

    #     # Cross elites from opposite ends
    #     for i in range(len(elites) // 2):
    #         parent1 = elites[i]
    #         parent2 = elites[-i - 1]
    #         child1, child2 = parent1.crossover(parent2)

    #         child1.mutant = random.random() < mutation_chance
    #         child2.mutant = random.random() < mutation_chance
    #         if child1.mutant:
    #             child1.mutate()
    #         if child2.mutant:
    #             child2.mutate()

    #         new_gen.extend([child1, child2])

    #     return new_gen



    def reproduce(self, population, mutation_chance=0.1):
        POP_SIZE = len(population)
        elites_count = max(1, POP_SIZE // 10)  # Top 10%
        new_gen = []

        # 1. Keep top 10% as is (elitism)
        sorted_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        elites = sorted_population[:elites_count]
        for elite in elites:
            elite.reset()
        new_gen.extend(elites)

        # 2. Create selection pool with probabilities proportional to fitness
        fitnesses = [ind.fitness for ind in population]
        total_fitness = sum(fitnesses)

        # Avoid division by zero
        if total_fitness == 0:
            probs = [1 / POP_SIZE] * POP_SIZE
        else:
            probs = [f / total_fitness for f in fitnesses]

        # 3. Generate children until population size is reached
        while len(new_gen) < POP_SIZE:
            # Pick two parents by roulette wheel (fitness-proportional)
            parent1 = random.choices(population, weights=probs, k=1)[0]
            parent2 = random.choices(population, weights=probs, k=1)[0]

            child1, child2 = parent1.crossover(parent2)

            # Mutate if needed
            child1.mutant = random.random() < mutation_chance
            child2.mutant = random.random() < mutation_chance
            if child1.mutant:
                child1.mutate()
            if child2.mutant:
                child2.mutate()

            new_gen.append(child1)
            if len(new_gen) < POP_SIZE:
                new_gen.append(child2)  # Only add second child if space

        return new_gen

            
    def go_to_next_gen(self):
        # luam jumatatea din populatie care s-a adaptat mai bine la environment
        pop = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=True)[:self.size//2]
        
        new_generation = self.reproduce(pop)
        
        self.generation += 1
        self.individuals = new_generation

        # Load generation from file
        os.makedirs("gens", exist_ok=True)
        with open(f"gens/gen_{self.generation}.pkl", "wb") as f:
            pickle.dump(self, f)
        print("GEN:", self.generation)
        
        