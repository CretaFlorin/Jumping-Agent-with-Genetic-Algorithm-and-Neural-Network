import random
from my_platform import Platform  # type: ignore
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import math
from rtree import index


def create_platforms(seed=None):
    platforms = []

    NUM_LEVELS = 10
    PLATFORM_HEIGHT = 20
    LEVEL_SPACING = 90
    PLATFORM_MIN_WIDTH = 100
    PLATFORM_MAX_WIDTH = 200
    WIDTH_OFFSET = 1000

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


def build_platform_index(platforms):
    idx = index.Index()
    for i, p in enumerate(platforms):
        idx.insert(i, (p.x, p.y, p.x + p.width, p.y + p.height))
    return idx


def line_rect_intersection(p1, p2, rect):
    # p1, p2 = (x,y) line points
    # rect = (x_min, y_min, x_max, y_max)

    x_min, y_min, x_max, y_max = rect

    # Define rectangle edges as lines
    edges = [
        ((x_min, y_min), (x_max, y_min)),  # top
        ((x_max, y_min), (x_max, y_max)),  # right
        ((x_max, y_max), (x_min, y_max)),  # bottom
        ((x_min, y_max), (x_min, y_min)),  # left
    ]

    for edge_p1, edge_p2 in edges:
        if lines_intersect(p1, p2, edge_p1, edge_p2):
            # Optional: find exact intersection point here if needed
            return True
    return False


def lines_intersect(p1, p2, q1, q2):
    # Check if line segments p1p2 and q1q2 intersect
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))


def line_rect_intersection_point(p1, p2, rect):
    # Define rectangle edges as line segments
    edges = [
        ((rect.left, rect.top), (rect.right, rect.top)),  # top
        ((rect.right, rect.top), (rect.right, rect.bottom)),  # right
        ((rect.right, rect.bottom), (rect.left, rect.bottom)),  # bottom
        ((rect.left, rect.bottom), (rect.left, rect.top)),  # left
    ]

    for edge_start, edge_end in edges:
        intersect = segment_intersection(p1, p2, edge_start, edge_end)
        if intersect:
            return intersect  # return first hit point

    return None


def segment_intersection(p1, p2, q1, q2):
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    x_diff = (p1[0] - p2[0], q1[0] - q2[0])
    y_diff = (p1[1] - p2[1], q1[1] - q2[1])

    div = det(x_diff, y_diff)
    if div == 0:
        return None  # Lines are parallel

    d = (det(p1, p2), det(q1, q2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div

    # Check if the point is within both segments
    if (
        min(p1[0], p2[0]) <= x <= max(p1[0], p2[0])
        and min(p1[1], p2[1]) <= y <= max(p1[1], p2[1])
        and min(q1[0], q2[0]) <= x <= max(q1[0], q2[0])
        and min(q1[1], q2[1]) <= y <= max(q1[1], q2[1])
    ):
        return (x, y)

    return None


def point_in_rect(point, rect):
    x, y = point
    return rect.collidepoint(x, y)