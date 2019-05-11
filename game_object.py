from configs import *
from bbox import BBox

import pygame


class GameObject(ABC):
    _owner = 0
    _is_selected: bool = False
    _image: pygame.Surface
    _screen: pygame.Surface
    _bbox: BBox
    _health: float
    _max_health: float
    _dying = False

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def step(self, delta_t):
        pass

    @abstractmethod
    def is_dead(self):
        pass

    def get_owner(self):
        return self._owner

    def get_bbox(self):
        return self._bbox

    def set_is_selected(self, state):
        self._is_selected = state

    def get_is_selected(self):
        return self._is_selected

    def is_dying(self):
        return self._dying

    def get_health(self):
        return self._health

    def set_health(self, val):
        self._health = val
