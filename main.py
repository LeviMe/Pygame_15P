#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from game import Game
from menus import *
from types import SimpleNamespace

import os
import yaml


def load_config():
    default_config = {
        "width": 480,
        "height": 480,
        "FPS": 60,
        "dim": 4,
        "sound_on": True,
    }
    if os.path.exists("config.yml"):
        with open("config.yml") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    else:
        config = default_config
    return config


def dump_config(config, dim, sound_on):  # plus eficace avec un **kwargs
    config["dim"], config["sound_on"] = dim, sound_on
    if os.path.exists("config.yml"):
        with open("config.yml", "w") as f:
            yaml.dump(config, stream=f, sort_keys=False)


def main():

    config = load_config()
    n = SimpleNamespace(**config)

    width, height, FPS = n.width, n.height, n.FPS
    dim, sound_on = n.dim, n.sound_on

    WIN = pygame.display.set_mode((width, height))
    state = 1
    while True:
        if state == 0:
            pygame.quit()
            dump_config(config, dim, sound_on)
            break
        if state == 1:
            G = StartMenu(WIN, FPS, sound_on)
            state = G.launch()
        if state == 2:
            G = Game(WIN, dim, FPS, sound_on)
            state, nb_moves, time = G.launch()
        if state == 3:
            G = EndMenu(WIN, FPS, nb_moves, time, sound_on)
            state = G.launch()
        if state == 4:
            G = SettingMenu(dim, sound_on, WIN, FPS)
            state, dim, sound_on = G.launch()


if __name__ == "__main__":
    main()
