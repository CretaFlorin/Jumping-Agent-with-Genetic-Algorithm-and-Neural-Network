import pygame
from constants import (
    SCREEN_WIDTH as WIDTH,
    SCREEN_HEIGHT as HEIGHT,
    VISION_DIRS as DIRS,
    SHOW_VISION_RAYS,
    GRAVITY,
    SIDE_SPEED,
    JUMP_STRENGTH,
    MUTANT_CHANCE,
    INDIV_WIDTH,
    INDIV_HEIGHT,
    MAX_VISION_DISTANCE,
)
from NN import NeuralNetwork
import random
from helpers import point_in_rect
import numpy as np


class Individual:
    def __init__(
        self,
        x=None,
        y=HEIGHT - INDIV_HEIGHT,
        width=INDIV_WIDTH,
        height=INDIV_HEIGHT,
        color=(100, 255, 100),
    ):
        self.x = x or random.randint(50, WIDTH - 50)
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.mutant = random.random() < MUTANT_CHANCE

        if self.mutant:
            self.color = (250, 105, 100)

        self.vel_x = 0
        self.vel_y = 0

        self.gravity = GRAVITY
        self.on_ground = False
        self.speed = SIDE_SPEED
        self.jump_strength = JUMP_STRENGTH

        #

        self.brain = NeuralNetwork(input_size=len(DIRS))
        self.fitness = 0
        self.color = (0, self.fitness / 10, 0)
        if self.mutant:
            self.color = (self.fitness / 10, 0, 0)

        self.vision = None
        self.center = None
        self.horizontal_movement = 0

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT - INDIV_HEIGHT
        self.fitness = 0
        self.vision = None
        self.center = None
        self.horizontal_movement = 0
        # reset other fields as needed (e.g., collision state, score)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def apply_physics(self):
        self.vel_y += self.gravity

    def handle_collision(self, platforms):
        self_rect = self.get_rect()

        for platform in platforms:
            platform_rect = platform.get_rect()

            if self_rect.colliderect(platform_rect) and self.vel_y > 0:
                self.y = platform.y - self.height
                self.vel_y = 0
                self.on_ground = True

        # ground collision
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True

        # left wall collision
        if self.x < 0:
            self.vel_x = 0

        # right wall collision
        if self.x > WIDTH - self.width:
            self.vel_x = 0

    def move(self, left=False, right=False, jump=False):
        self.vel_x = 0
        if left and self.x > 0:
            self.vel_x = -self.speed
        elif right and self.x < WIDTH - self.width:
            self.vel_x = self.speed

        if jump and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def update(self, platforms, screen):
        self.apply_physics()
        self.handle_collision(platforms)
        self.show_vision_rays(screen)

        self.x += self.vel_x
        self.y += self.vel_y

        self.horizontal_movement += self.vel_x // 5
        if  HEIGHT - self.y + self.horizontal_movement > self.fitness:
            self.fitness = HEIGHT - self.y + self.horizontal_movement
            self.color = (0, min(self.fitness / 4, 255), 0)
            if self.mutant:
                self.color = (255, 0, 0)

    def sense_environment(self, screen, platforms):
        for p in platforms:
            pygame.draw.rect(screen, (255, 0, 0), p.get_rect(), width=2)

        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        self.center = (cx, cy)

        increment = 20
        vision = []

        for dx, dy in DIRS:
            distance = 0
            detected_distance = 0
            done = False

            while True:
                distance += increment
                end_x = cx + dx * distance
                end_y = cy + dy * distance

                # Check if out of bounds (wall)
                if end_x < 0 or end_y < 0 or end_x > WIDTH or end_y > HEIGHT:
                    detected_distance = distance
                    done = True
                    break

                # Check collision with any platform
                for p in platforms:
                    rect = p.get_rect()
                    if point_in_rect((end_x, end_y), rect):
                        detected_distance = distance
                        done = True
                        break

                if done:
                    break

                # Stop at max vision distance
                if distance >= MAX_VISION_DISTANCE:
                    # Nothing detected within max vision distance
                    detected_distance = 0
                    break

            vision.append(detected_distance)

        self.vision = vision

    def show_vision_rays(self, screen):
        if not SHOW_VISION_RAYS:
            return
        
        cx = self.center[0]
        cy = self.center[1]

        num_dirs = len(DIRS)
        platforms_hit = self.vision[:num_dirs]
        walls = self.vision[num_dirs : 2 * num_dirs]
        empty = self.vision[2 * num_dirs :]

        for i, (dx, dy) in enumerate(DIRS):
            # Draw platform hits in red
            if platforms_hit[i] > 0:
                end_x = cx + dx * platforms_hit[i]
                end_y = cy + dy * platforms_hit[i]
                pygame.draw.line(screen, (255, 0, 0), (cx, cy), (end_x, end_y))
            # Draw wall hits in green
            elif walls[i] > 0:
                end_x = cx + dx * walls[i]
                end_y = cy + dy * walls[i]
                pygame.draw.line(screen, (0, 255, 0), (cx, cy), (end_x, end_y))
            # Draw max vision distance in blue
            elif empty[i] > 0:
                end_x = cx + dx * empty[i]
                end_y = cy + dy * empty[i]
                pygame.draw.line(screen, (0, 0, 255), (cx, cy), (end_x, end_y))

    # Consideram cele 4 serii de parametri ai
    # retelei setul de gene al unui individ
    def crossover(self, partner):
        child1 = Individual()
        child2 = Individual()

        def crossover_array(a, b):
            mask = np.random.rand(*a.shape) < 0.5
            child1_gene = np.where(mask, a, b)
            child2_gene = np.where(mask, b, a)
            return child1_gene, child2_gene

        b1 = self.brain
        b2 = partner.brain
        c1 = child1.brain
        c2 = child2.brain

        # Input to first hidden layer weights and biases
        c1.w_input_hidden1, c2.w_input_hidden1 = crossover_array(
            b1.w_input_hidden1, b2.w_input_hidden1
        )
        c1.b_hidden1, c2.b_hidden1 = crossover_array(b1.b_hidden1, b2.b_hidden1)

        # First hidden to second hidden layer weights and biases
        c1.w_hidden1_hidden2, c2.w_hidden1_hidden2 = crossover_array(
            b1.w_hidden1_hidden2, b2.w_hidden1_hidden2
        )
        c1.b_hidden2, c2.b_hidden2 = crossover_array(b1.b_hidden2, b2.b_hidden2)

        # Second hidden to output layer weights and biases
        c1.w_hidden2_output, c2.w_hidden2_output = crossover_array(
            b1.w_hidden2_output, b2.w_hidden2_output
        )
        c1.b_output, c2.b_output = crossover_array(b1.b_output, b2.b_output)

        return child1, child2

    def mutate(self, mutation_rate=0.05, mutation_strength=0.5):
        def apply_mutation(arr):
            mutation_mask = np.random.rand(*arr.shape) < mutation_rate
            noise = np.random.uniform(-mutation_strength, mutation_strength, arr.shape)
            arr += mutation_mask * noise

        brain = self.brain

        apply_mutation(brain.w_input_hidden1)
        apply_mutation(brain.b_hidden1)

        apply_mutation(brain.w_hidden1_hidden2)
        apply_mutation(brain.b_hidden2)

        apply_mutation(brain.w_hidden2_output)
        apply_mutation(brain.b_output)

        self.color = (255, 0, 0)
