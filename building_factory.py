from configs import *
from player import Player
from game_object import GameObject
import os
from bbox import CircleBBox
import random


class BuildingFactory:
    def __init__(self, screen, world):
        self._screen = screen
        self._world = world

    def create_building(self, name, player, coordinates):
        if name == "BuildingWorker":
            return BuildingWorker(self._screen, self._world, coordinates, player)
        if name == "BuildingWarrior":
            return BuildingWarrior(self._screen, self._world, coordinates, player)


class Building(GameObject, ABC):
    _image: pygame.Surface
    _sprite_name: str

    def __init__(self, screen, world, coordinates, owner):
        self._screen = screen
        self._world = world
        self._owner = owner

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, self._sprite_name)).convert_alpha()
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )
        self._bbox = CircleBBox(coordinates[0] + self._image.get_width() / 2,
                                coordinates[1] + self._image.get_height() / 2,
                                3)
        self._health = random.randint(1, 100)

    def step(self, delta_t):
        pass

    def is_dead(self):
        pass

    def render(self):
        self._screen.blit(self._image,
                          (self._bbox.x - self._image.get_width() / 2,
                           self._bbox.y - self._image.get_height() / 2))

    def get_y(self):
        return self._bbox.y

    '''def build_it(self):
            for i in range(self.height):
                crop_surf = pygame.transform.chop(self._image, (0, 0, 0, self.height - i))
                self._screen.blit(crop_surf, (440, 440 - i))
                pygame.display.flip()
                self._screen.fill((255, 255, 255))'''


class BuildingWarrior(Building):
    _sprite_name = "warbuilding.png"

    def attack(self):
        pass


class BuildingWorker(Building):
    _sprite_name = "building.png"

    def get_ore(self):
        pass


class Ore(GameObject):
    _moving = False
    _chasing_object: GameObject = None
    _bbox: CircleBBox

    def __init__(self, screen, world, coordinates):
        self._screen = screen
        self._world = world

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'ore.png')).convert()
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )

        self._bbox = CircleBBox(coordinates[0] + self._image.get_width() / 2,
                                coordinates[1] + self._image.get_height() / 2,
                                10)

    def render(self):
        if self._world.check_ore_collision(self):
            self._world.objects.remove(self)
            return
        self._screen.blit(self._image, (self._bbox.x, self._bbox.y))

    def step(self, delta_t):
        pass

    def is_dead(self):
        pass

    def get_y(self):
        return self._bbox.y
