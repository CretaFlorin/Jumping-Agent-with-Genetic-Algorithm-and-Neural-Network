import random
from platform import Platform  # type: ignore
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def create_platforms(seed=None):
    platforms = []

    NUM_LEVELS = 10
    PLATFORM_HEIGHT = 20
    LEVEL_SPACING = 90
    PLATFORM_MIN_WIDTH = 100
    PLATFORM_MAX_WIDTH = 200
    WIDTH_OFFSET = 500

    if seed is not None:
        random.seed(seed)

    for i in range(NUM_LEVELS):
        y = SCREEN_HEIGHT - 100 - i * LEVEL_SPACING

        level_width = 0
        while SCREEN_WIDTH - level_width > PLATFORM_MAX_WIDTH:
            space = random.randint(0, WIDTH_OFFSET)
            width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
            x = level_width + space

            platforms.append(Platform(x, y, width, PLATFORM_HEIGHT))
            level_width += space + width

    return platforms
