# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
FPS = 200
VISION_DIRS = [
    [-1, -1],
    [0, -1],
    [1, -1],  # diagonals and straight up
    [-0.5, -0.75],
    [0.5, -0.75],  # slight angles
    [-0.25, -1],
    [0.25, -1],  # narrow upward focus
]
SHOW_VISION_RAYS = False

# physics
GRAVITY = 0.2
SIDE_SPEED = 3
JUMP_STRENGTH = -6

# genetics
MUTANT_CHANCE = 0.05

# individuals
INDIV_WIDTH = 10
INDIV_HEIGHT = 20

GENERATION_TIME = 3
