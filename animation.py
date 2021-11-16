#!/usr/bin/env python3
import numpy as np
import pygame
from constants import *


class Animation:
    def __init__(self, button, start, end, duration, FPS):
        self.duration = duration
        self.start = np.array(start)
        self.end = np.array(end)

        self.nb_steps = int(self.duration * FPS)
        self.step = 0
        self.button = button

    def compute_F_vector(self, rate_function="LINEAR"):
        fact = 4
        T_vector = np.linspace(0, 1, self.nb_steps)
        formula = {
            "LINEAR": lambda x: x,
            "ATAN": lambda x: (np.arctan(fact * (x - 0.5))) / (np.pi) + 1 / 2,
            "ATAN2": lambda x: (np.arctan(fact * x)) / (np.pi / 2),
            "EXP": lambda x: (1 - np.exp(-fact * x)) / (1 - np.exp(-1)),
        }

        f = formula[rate_function]
        F_vector = f(T_vector)
        F_vector = [F_vector[i] - F_vector[0] for i in range(self.nb_steps)]
        F_vector = [F_vector[i] / F_vector[-1] for i in range(self.nb_steps)]
        return F_vector

    def is_over(self):
        return self.step == self.nb_steps


class AnimationMove(Animation):
    def __init__(self, button, start, end, duration, FPS):
        super().__init__(button, start, end, duration, FPS)
        self.compute_coordinates("EXP")

    def compute_coordinates(self, rate_function="LINEAR"):
        F_vector = self.compute_F_vector(rate_function)
        self.coordinates = []
        for i in range(self.nb_steps):
            x = self.start[0] + F_vector[i] * (self.end[0] - self.start[0])
            y = self.start[1] + F_vector[i] * (self.end[1] - self.start[1])
            self.coordinates += [(x, y)]

    def update(self):
        x, y = self.coordinates[self.step]
        self.button.set_position(x, y)  # attention au passage par valeur
        self.step += 1


class AnimationVanish(AnimationMove):
    def __init__(self, button, start, end, duration, FPS, event):
        super().__init__(button, start, end, duration, FPS)
        self.event = event

    def is_over(self):
        res = self.step == self.nb_steps
        if res:
            if self.event == "START":
                pygame.event.post(pygame.event.Event(STARTe))
            if self.event == "EXIT":
                pygame.event.post(pygame.event.Event(EXITe))
            if self.event == "SETTING":
                pygame.event.post(pygame.event.Event(SETTINGe))
        return res


class AnimationGrow(Animation):
    def __init__(self, button, start=0, end=1, duration=1, FPS=30):
        super().__init__(button, start, end, duration, FPS)
        self.compute_width_list("EXP")

    def compute_width_list(self, rate_function="LINEAR"):
        F_vector = self.compute_F_vector(rate_function)
        self.width_list = self.button.width * np.array(F_vector)
        self.width_list = np.array(self.width_list, dtype=np.int32)

    def update(self):
        new_width = self.width_list[self.step]
        self.button.set_pos_scale(new_width)
        self.step += 1
