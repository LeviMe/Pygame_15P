#!/usr/bin/env python3

import os
import numpy as np
import random as rd
import pygame
from PIL import Image  # , ImageEnhance
from animation import AnimationMove, AnimationGrow

pygame.font.init()
from constants import *


class Tile:
    def __init__(self, value, width):
        self.value = value
        self.width = width
        self.image0 = pygame.image.load(
            os.path.join("Assets", "pictures", "Tile_" + str(value) + "_.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image0, (self.width, self.width))
        self.x, self.y, self.xc, self.yc = 0, 0, 0, 0  # init inutile
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.x, self.y = x, y
        self.xc, self.yc = x + self.width / 2, y + self.width / 2
        self.rect.update(self.y, self.x, self.width, self.width)

    def set_pos_scale(self, new_width):
        self.x = self.xc - new_width / 2
        self.y = self.yc - new_width / 2
        self.width = new_width
        self.image = pygame.transform.scale(self.image0, (self.width, self.width))
        self.rect = self.image.get_rect()


class Game:
    def __init__(self, windw, dim=4, fps=60, sound_on=True):
        self.dim = dim
        self.windw = windw
        self.fps = fps
        h, w = self.windw.get_size()
        self.tile_width = (w - 52) // self.dim
        A = np.append(np.arange(1, self.dim ** 2), -1)
        self.mat = np.reshape(A, [self.dim, self.dim])
        self.position = (self.dim - 1, self.dim - 1)
        self.dict_tiles = {}
        self.build_tiles()
        self.shuffle()
        self.nb_move = 0
        self.update_trigger = True
        self.animation_running = False
        self.animations = []
        self.add_animations_tiles()
        self.adjacent_tiles = []

        bg_image = Image.open(os.path.join("Assets", "pictures", "bg_game01.jpg"))
        bg_image.crop((0, 0, w, w))
        # bg_image = ImageEnhance.Brightness(bg_image).enhance(.85)
        mode, size, data = bg_image.mode, bg_image.size, bg_image.tobytes()
        bg_image = pygame.image.fromstring(data, size, mode)
        bg_image = pygame.transform.scale(bg_image, self.windw.get_size())
        self.bg_image = bg_image
        self.update_adjacent_tiles()

        if not sound_on:
            for sound in {WIN_SOUND, MOVE_SOUND}:
                sound.set_volume(0)

    def set_tiles_coordinates(self, j, i):
        x, y = 10 + (self.tile_width + 10) * j, 10 + (self.tile_width + 10) * i
        return x, y

    def build_tiles(self):
        for i in range(1, self.dim ** 2):
            v, h = i // self.dim, i % self.dim
            x, y = self.set_tiles_coordinates(v, h)
            tile = Tile(i, self.tile_width)
            tile.set_position(x, y)
            self.dict_tiles[i] = tile

    def add_animations_tiles(self):
        for i in range(0, self.dim ** 2):
            v, h = i // self.dim, i % self.dim
            value = self.mat[v, h]
            if value != -1:
                tile = self.dict_tiles[value]
                anim = AnimationGrow(tile)
                self.animations += [anim]
                # print("anim", value)
        self.animation_running = True

    def update_tiles_coordinates(self):
        for v in range(self.dim):
            for h in range(self.dim):
                tile_value = self.mat[v, h]
                if tile_value != -1:
                    tile = self.dict_tiles[tile_value]
                    x, y = self.set_tiles_coordinates(v, h)
                    tile.set_position(x, y)

    def update_adjacent_tiles(self):
        L, M, self.adjacent_tiles = [], [], {}
        x, y = self.position
        if x != 0:
            L, M = L + [(x - 1, y)], M + ["UP"]
        if x != self.dim - 1:
            L, M = L + [(x + 1, y)], M + ["DOWN"]
        if y != 0:
            L, M = L + [(x, y - 1)], M + ["LEFT"]
        if y != self.dim - 1:
            L, M = L + [(x, y + 1)], M + ["RIGHT"]

        for d in zip(M, L):
            direction, adj_pos = d
            adj_tile = self.dict_tiles[self.mat[adj_pos]]
            self.adjacent_tiles[direction] = adj_tile

    def shuffle(self):
        def transformation(i):
            x, y = self.position
            if i == 0 and x >= 1:
                self.position = (x - 1, y)
            if i == 1 and x < self.dim - 1:
                self.position = (x + 1, y)
            if i == 2 and y >= 1:
                self.position = (x, y - 1)
            if i == 3 and y < self.dim - 1:
                self.position = (x, y + 1)

            if (x, y) != self.position:
                self.mat[self.position], self.mat[x, y] = (
                    self.mat[x, y],
                    self.mat[self.position],
                )

        for _ in range(NB_SHUFFLE):
            transformation(rd.randint(0, 4))
        self.update_tiles_coordinates()

    def handle_mouse_motion(self):
        x, y = self.position
        pos = pygame.mouse.get_pos()

        for direction in self.adjacent_tiles.keys():
            adj_tile = self.adjacent_tiles[direction]
            if adj_tile.rect.collidepoint(pos):
                if direction == "LEFT":
                    self.position = (x, y - 1)
                if direction == "RIGHT":
                    self.position = (x, y + 1)
                if direction == "UP":
                    self.position = (x - 1, y)
                if direction == "DOWN":
                    self.position = (x + 1, y)

        self.launch_motion((x, y), self.position)

    def handle_keys(self, key_pressed):
        x, y = self.position

        if key_pressed[pygame.K_LEFT] and y < self.dim - 1:
            self.position = (x, y + 1)
        if key_pressed[pygame.K_RIGHT] and y >= 1:
            self.position = (x, y - 1)
        if key_pressed[pygame.K_UP] and x < self.dim - 1:
            self.position = (x + 1, y)
        if key_pressed[pygame.K_DOWN] and x >= 1:
            self.position = (x - 1, y)

        self.launch_motion((x, y), self.position)

    def launch_motion(self, position, new_position):
        x, y = position
        xp, yp = new_position
        if (x, y) != (xp, yp):
            self.mat[xp, yp], self.mat[x, y] = self.mat[x, y], self.mat[xp, yp]
            self.nb_move += 1
            self.update_trigger = True

            end = self.set_tiles_coordinates(x, y)
            start = self.set_tiles_coordinates(xp, yp)

            self.animation_running = True
            moving_tile = self.dict_tiles[self.mat[x, y]]
            anim = AnimationMove(moving_tile, start, end, 0.27, self.fps)
            self.animations += [anim]

            MOVE_SOUND.play()
            self.update_adjacent_tiles()

    def check_completion(self):
        res = len(self.animations) == 0
        for i in range(self.dim ** 2 - 2, -1, -1):
            x, y = i // self.dim, i % self.dim
            res = res and (self.mat[x, y] == i + 1)
            if not res:
                break
        return res

    def draw_window(self):
        self.windw.blit(self.bg_image, (0, 0))
        for v in range(self.dim):
            for h in range(self.dim):
                value = self.mat[v, h]
                if value != -1:
                    tile = self.dict_tiles[value]
                    try:
                        self.windw.blit(tile.image, (tile.y, tile.x))
                    except:
                        print("error drawing tile at ", tile.y, tile.x)
        pygame.display.update()

    def launch(self):
        clock = pygame.time.Clock()
        run = True
        key_variable = True
        mouse_variable = True

        start_ticks = pygame.time.get_ticks()
        count = 0
        while run:
            clock.tick(self.fps)
            if count % 7 in (0, 1):

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return 0, self.nb_move, 0

                    if (
                        event.type == pygame.MOUSEBUTTONUP
                        and mouse_variable
                        and not self.animation_running
                    ):
                        self.handle_mouse_motion()
                        mouse_variable = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_variable = True

                key_pressed = pygame.key.get_pressed()
                if sum(key_pressed) != key_variable and not self.animation_running:
                    self.handle_keys(key_pressed)
                key_variable = sum(key_pressed)

            count = count + 1

            if len(self.animations) != 0:
                for anim in self.animations:
                    anim.update()
                    self.update_trigger = True
                    if anim.is_over():
                        self.animations.remove(anim)
                        self.update_tiles_coordinates()
            else:
                self.animation_running = False
                self.update_trigger = False

            if self.update_trigger:
                self.draw_window()

            if self.check_completion():
                WIN_SOUND.play()
                run = False

        if __name__ == "__main__":
            pygame.time.delay(8000)
            pygame.quit()
        else:
            next_state = 3
            time = int(np.round((pygame.time.get_ticks() - start_ticks) / 1000))
            return next_state, self.nb_move, time


def main():
    width, height = 510, 510
    FPS = 60
    WIN = pygame.display.set_mode((width, height))
    G = Game(WIN, 4, FPS)
    G.launch()


if __name__ == "__main__":
    main()
