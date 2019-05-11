from pygame.locals import Rect
from abc import ABC, abstractmethod
import pygame

SCREEN_RECT: Rect
IMAGES_FOLDER = r'resources/images'
RESOURCES_FOLDER = r'resources'
PIXEL_SCALE = 10

WORLD_GRID = [[0 for i in range(100)] for j in range(100)]
WORLD_GRID_SIZE = PIXEL_SCALE
