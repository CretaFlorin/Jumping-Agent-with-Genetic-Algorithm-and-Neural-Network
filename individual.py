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
    INDIV_HEIGHT
)
from NN import NeuralNetwork
import random


class Individual:
    def __init__(
        self, x=None, y=HEIGHT - INDIV_HEIGHT, width=INDIV_WIDTH, height=INDIV_HEIGHT, color=(100, 255, 100)
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

        self.brain = NeuralNetwork()
        self.fitness = 0

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

    def update(self, platforms):
        self.apply_physics()
        self.handle_collision(platforms)

        self.x += self.vel_x
        self.y += self.vel_y

        if HEIGHT - self.y > self.fitness:
            self.fitness = HEIGHT - self.y

    def sense_environment(self, screen, platforms):
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        vision = []

        for dx, dy in DIRS:
            distance = 0
            x, y = cx, cy
            multiplier = 50

            while True:
                x += multiplier * dx
                y += multiplier * dy
                distance += multiplier

                # Verificam daca am ajuns la margine
                if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
                    if SHOW_VISION_RAYS:
                        pygame.draw.line(screen, (0, 255, 0), (cx, cy), (x, y))
                    break

                # Verificam daca am ajuns la o platforma
                hit = False
                for p in platforms:
                    if p.x <= x <= p.x + p.width and p.y <= y <= p.y + p.height:
                        hit = True

                if hit:
                    if SHOW_VISION_RAYS:
                        pygame.draw.line(screen, (255, 0, 0), (cx, cy), (x, y))
                    break

            vision.append(distance)

        return vision

    # Consideram cele 4 serii de parametri ai
    # retelei setul de gene al unui individ
    def crossover(self, partener):
        child1 = Individual()
        child2 = Individual()

        brain1 = self.brain
        brain2 = partener.brain

        for i in range(self.brain.hidden_size):
            if i % 2:
                if child1.mutant:
                    child1.brain.b_hidden[i] = random.uniform(-1, 1)
                else:
                    child1.brain.b_hidden[i] = brain1.b_hidden[i]
                if child2.mutant:
                    child2.brain.b_hidden[i] = random.uniform(-1, 1)
                else:
                    child2.brain.b_hidden[i] = brain2.b_hidden[i]
            else:
                if child1.mutant:
                    child1.brain.b_hidden[i] = random.uniform(-1, 1)
                else:
                    child1.brain.b_hidden[i] = brain2.b_hidden[i]
                if child2.mutant:
                    child2.brain.b_hidden[i] = random.uniform(-1, 1)
                else:
                    child2.brain.b_hidden[i] = brain1.b_hidden[i]

            for j in range(self.brain.input_size):
                if (i + j) % 2:
                    if child1.mutant:
                        child1.brain.w_input_hidden[i][j] = random.uniform(-1, 1)
                    else:
                        child1.brain.w_input_hidden[i][j] = brain1.w_input_hidden[i][j]

                    if child2.mutant:
                        child2.brain.w_input_hidden[i][j] = random.uniform(-1, 1)
                    else:
                        child2.brain.w_input_hidden[i][j] = brain2.w_input_hidden[i][j]
                else:
                    if child1.mutant:
                        child1.brain.w_input_hidden[i][j] = random.uniform(-1, 1)
                    else:
                        child1.brain.w_input_hidden[i][j] = brain2.w_input_hidden[i][j]

                    if child2.mutant:
                        child2.brain.w_input_hidden[i][j] = random.uniform(-1, 1)
                    else:
                        child2.brain.w_input_hidden[i][j] = brain1.w_input_hidden[i][j]

        for i in range(self.brain.output_size):
            if i % 2:
                if child1.mutant:
                    child1.brain.b_output[i] = random.uniform(-1, 1)
                else:
                    child1.brain.b_output[i] = brain1.b_output[i]

                if child2.mutant:
                    child2.brain.b_output[i] = random.uniform(-1, 1)
                else:
                    child2.brain.b_output[i] = brain2.b_output[i]
            else:
                if child1.mutant:
                    child1.brain.b_output[i] = random.uniform(-1, 1)
                else:
                    child1.brain.b_output[i] = brain2.b_output[i]

                if child2.mutant:
                    child2.brain.b_output[i] = random.uniform(-1, 1)
                else:
                    child2.brain.b_output[i] = brain1.b_output[i]

            for j in range(self.brain.hidden_size):
                if (i + j) % 2:
                    if child1.mutant:
                        child1.brain.w_hidden_output[i][j] = random.uniform(-1, 1)
                    else:
                        child1.brain.w_hidden_output[i][j] = brain1.w_hidden_output[i][
                            j
                        ]

                    if child2.mutant:
                        child2.brain.w_hidden_output[i][j] = random.uniform(-1, 1)
                    else:
                        child2.brain.w_hidden_output[i][j] = brain2.w_hidden_output[i][
                            j
                        ]
                else:
                    if child1.mutant:
                        child1.brain.w_hidden_output[i][j] = random.uniform(-1, 1)
                    else:
                        child1.brain.w_hidden_output[i][j] = brain2.w_hidden_output[i][
                            j
                        ]

                    if child2.mutant:
                        child2.brain.w_hidden_output[i][j] = random.uniform(-1, 1)
                    else:
                        child2.brain.w_hidden_output[i][j] = brain1.w_hidden_output[i][
                            j
                        ]

        return child1, child2
