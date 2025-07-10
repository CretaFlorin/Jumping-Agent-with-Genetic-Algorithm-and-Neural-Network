# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
FPS = 1000
VISION_DIRS = [
    [-1, -1],
    [0, -1],
    [1, -1],           # diagonals and straight up
    [-0.66, -1],
    [0.66, -1],       # slight upward angles
    [-0.25, -1],
    [0.25, -1],         # narrow upward focus
    [-0.5, 1],          
    [0.5, 1],           
]

SHOW_VISION_RAYS = True
FRAMES_PER_VISION = 1
MAX_VISION_DISTANCE = 200

# physics
GRAVITY = 0.2
SIDE_SPEED = 4
JUMP_STRENGTH = -7

# genetics
MUTANT_CHANCE = 0.1

# individuals
INDIV_WIDTH = 10
INDIV_HEIGHT = 20

GENERATION_TIME = 500 # in number of actions taken (frames spent)
POPULATION_SIZE = 32
TRAINING_MODE = True
ONLY_BEST = False
RANDOM_SEED = 41
