from world import *
from game_object import GameObject
import random
from typing import List

import pygame


class Player:
    name: str
    _age: str
    _resources = {}
    _ore = 0

    def __init__(self, world, name):
        self.world = world
        self.name = name


class AIPlayer(Player):
    pass


def list_to_rect(lst):
    return pygame.Rect(*lst)


class HumanPlayer(Player):
    events: List[str] = []
    selected_objects: List[GameObject] = []

    def __init__(self, world, name):
        super().__init__(world, name)

    def selection_rect_finished(self, rect_list: list):
        for obj in self.selected_objects:
            obj.set_is_selected(False)
        self.selected_objects.clear()
        self.selected_objects = self.world.select_objects(list_to_rect(rect_list))

    def right_click(self, mouse_pos):
        self.world.move_selected(self.selected_objects, mouse_pos)

    def left_click(self, c):
        pass

    def act(self):
        for i in range(5):
            for j in range(5):
                self.world.create_man("ManWorker", self, [300 + i * 50, 300 + j * 50])
                self.world.create_man("ManBuilder", self, [600 + i * 50, 300 + j * 50])
                self.world.create_man("ManWarrior", self, [900 + i * 50, 300 + j * 50])
        self.world.create_building("BuildingWarrior", self, [1200, 300])

    def create_army(self, num):
        for i in range(num):
            self.world.create_man('CarWarrior', self, [random.randint(100, 100), random.randint(100, 100)])

    def delete_button(self):
        self.world.remove_selected()

    def process_events(self):
        for event in self.events:
            self.__getattribute__(event['name'])(*(event['params']))
        self.events.clear()

    def push_events(self, events):
        self.events = events
