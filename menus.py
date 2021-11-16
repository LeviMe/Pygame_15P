# -*- coding: utf-8 -*-

import numpy as np
import pygame, pygame.freetype
import os
from animation import AnimationMove, AnimationVanish
from buttons import Button, OnOffButton, SelectButton

from constants import *

pygame.freetype.init()


class Menu:
    def __init__(self, windw, fps, sound_on=True):
        self.windw = windw
        self.fps = fps
        bg_image = pygame.image.load(
            os.path.join("Assets", "pictures", "bg_game01.jpg")
        ).convert()
        self.bg_image = pygame.transform.scale(bg_image, self.windw.get_size())
        self.update_trigger = True
        self.animation_running = False
        self.animations = []

        if not sound_on:
            for sound in {START_SOUND, CLICK_SOUND}:
                sound.set_volume(0)

    def draw_window(self):
        self.windw.blit(self.bg_image, (0, 0))
        for b in self.buttons:
            self.windw.blit(b.image, (b.y, b.x))
        pygame.display.update()

    def handle_mouse_motion(self):
        pos = pygame.mouse.get_pos()
        for b in self.buttons:
            if b.rect.collidepoint(pos):
                b.react()

    def clear_screen_anim(self, event):
        c = 1
        h, w = self.windw.get_size()
        for b in self.buttons:
            x, y, y_end = b.x, b.y, -(b.y + w)
            if c == 1:
                y_end = w + b.y
            anim = AnimationVanish(b, [x, y], [x, y_end], 1, self.fps, event)
            self.animations += [anim]
            self.animation_running = True
            c = -c

    def specific_action(self, counter):
        pass

    def specific_event_handler(self, event):
        pass

    def launch(self):
        h, w = self.windw.get_size()
        self.draw_window()
        counter = 0
        clock = pygame.time.Clock()
        run = True
        mouse_variable = True
        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0

                if (
                    event.type == pygame.MOUSEBUTTONUP
                    and mouse_variable
                    and not self.animation_running
                ):
                    self.handle_mouse_motion()
                    mouse_variable = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_variable = True

                res = self.specific_event_handler(event)
                if res is not None:
                    return res

            self.specific_action(counter)
            counter += 1

            if self.animation_running:
                for anim in self.animations:
                    anim.update()
                    # self.update_trigger = True
                    if anim.is_over():
                        self.animations.remove(anim)
                        if len(self.animations) == 0:
                            self.animation_running = False
                self.draw_window()


class StartMenu(Menu):
    def __init__(self, windw, fps, sound_on=True):
        super().__init__(windw, fps, sound_on)
        h, _ = self.windw.get_size()
        self.buttons = [Button("new game", h, 0), Button("settings", h, 0)]

    def specific_action(self, counter):
        h, w = self.windw.get_size()
        if counter == 10:
            anim = AnimationMove(
                self.buttons[0], [h, w * 0.12], [h * 0.17, w * 0.12], 1.1, self.fps
            )
            self.animations += [anim]
            self.animation_running = True

        if counter == 10:
            anim = AnimationMove(
                self.buttons[1], [h, w], [h * 0.31, w * 0.12], 1.1, self.fps
            )
            self.animations += [anim]
            self.animation_running = True

    def specific_event_handler(self, event):
        if event.type == STARTs:
            self.clear_screen_anim("START")
            START_SOUND.play()
        if event.type == STARTe:
            return 2
        if event.type == SETTINGs:
            self.clear_screen_anim("SETTING")
        if event.type == SETTINGe:
            return 4


class EndMenu(Menu):
    def __init__(self, windw, fps, nb_moves, time, sound_on=True):
        super().__init__(windw, fps, sound_on)
        h, _ = self.windw.get_size()
        self.buttons = [Button("new game", h, 0), Button("exit", h, 0)]
        self.nb_moves, self.time = nb_moves, time

    def specific_action(self, counter):
        h, w = self.windw.get_size()
        if counter == 10:
            anim = AnimationMove(
                self.buttons[0], [h, w * 0.12], [h * 0.5, w * 0.12], 1, self.fps
            )
            self.animations += [anim]
            self.animation_running = True

        if counter == 10:
            anim = AnimationMove(
                self.buttons[1], [h, w], [h * 0.65, w * 0.12], 1, self.fps
            )
            self.animations += [anim]
            self.animation_running = True

    def specific_event_handler(self, event):
        if event.type == STARTs:
            self.clear_screen_anim("START")
            START_SOUND.play()
        if event.type == STARTe:
            return 2
        if event.type == EXITs:
            self.clear_screen_anim("EXIT")
        if event.type == EXITe:
            return 0

        # pygame.quit()

    def draw_window(self):
        self.windw.blit(self.bg_image, (0, 0))
        h, w = self.windw.get_size()
        myfont = pygame.freetype.Font("./Assets/fonts/cookie.ttf", 40)
        text1 = "Game completed with " + str(self.nb_moves) + " moves"
        m, s = self.time // 60, self.time % 60
        mn_str, sc_str = "", ""
        if m > 0:
            mn_str = str(m) + ":"
        if s < 10 and m > 0:
            sc_str += "0" + str(s)
        else:
            sc_str += str(s)
        text2 = " in " + mn_str + str(sc_str)
        if m == 0:
            text2 += " s"
        text_surface1, _ = myfont.render(text1, (0, 5, 11))
        text_surface2, _ = myfont.render(text2, (0, 5, 11))
        self.windw.blit(text_surface1, (int(w * 0.08), int(h * 0.27)))
        self.windw.blit(text_surface2, (int(w * 0.30), int(h * 0.37)))
        # possibilité d'ajouter un copyright ici
        for b in self.buttons:
            self.windw.blit(b.image, (b.y, b.x))
        pygame.display.update()


class SettingMenu(Menu):
    def __init__(self, dim, sound_on, windw, fps):
        super().__init__(windw, fps, sound_on)
        self.selected_dim = str(dim)
        self.sound_on = sound_on

        h, _ = self.windw.get_size()

        self.dict_pos = {
            "3": (h * 0.43, h * 0.2),
            "4": (h * 0.43, h * 0.45),
            "5": (h * 0.43, h * 0.7),
            "<": (h * 0.1, h * 0.15),
            "S": (h * 0.65, h * 0.27),
        }

        self.buttons = {}
        for bb in self.dict_pos:
            x_bb, y_bb = self.dict_pos[bb]
            if bb != "S":
                self.buttons[bb] = SelectButton(bb, x_bb, y_bb)
            else:
                sound_b_dict = {True: "Sound ON", False: "Sound OFF"}
                self.buttons[bb] = OnOffButton(
                    sound_b_dict, self.sound_on, x_bb, y_bb, width=240
                )

        self.buttons["S"].update_image()

        selector = np.ones([80, 80, 3]) * [170, 75, 40]
        for i in range(10, 70):
            for j in range(10, 70):
                selector[i, j] = (255, 255, 255)
        self.selector = pygame.surfarray.make_surface(selector)
        self.current_event = 0

    def launch(self):
        h, w = self.windw.get_size()
        self.draw_window()
        clock = pygame.time.Clock()
        run = True
        mouse_variable = True
        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    res = 0, int(self.selected_dim), self.sound_on
                    return res

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_variable = True
                    self.update_trigger = False

                if event.type == pygame.MOUSEBUTTONUP and mouse_variable:
                    self.handle_mouse_motion()
                    mouse_variable = False
                    self.update_trigger = True

                res = self.specific_event_handler(event)
                if res is not None:
                    return res

                if self.update_trigger:
                    self.draw_window()

    def handle_mouse_motion(self):
        pos = pygame.mouse.get_pos()
        for b in self.buttons.values():
            if b.rect.collidepoint(pos):
                b.react()

    def specific_event_handler(self, event):
        self.current_event = event
        if event.type == SELECT_3:
            self.selected_dim = "3"
        if event.type == SELECT_4:
            self.selected_dim = "4"
        if event.type == SELECT_5:
            self.selected_dim = "5"
        if event.type == SELECT_S:
            self.sound_on = self.buttons["S"].state
            for sound in {START_SOUND, CLICK_SOUND}:
                sound.set_volume(self.sound_on * 1)

        if event.type == SELECT_R:
            next_state = 1
            return next_state, int(self.selected_dim), self.sound_on

    def draw_window(self):
        self.windw.blit(self.bg_image, (0, 0))
        h, w = self.windw.get_size()
        myfont = pygame.freetype.Font("./Assets/fonts/Gore Rough.otf", 34)
        text1 = "Dimension"  # + str(self.selected_dim)
        #        text2 =  str(self.sound_on)
        text_surface1, _ = myfont.render(text1, (0, 5, 11))
        #       text_surface2, _ = myfont.render(text2, (0,5, 11))

        self.windw.blit(text_surface1, (int(h * 0.30), int(h * 0.28)))
        # self.windw.blit(text_surface2, (int(h*.05),int(h*.65)))

        selected_button = self.buttons[self.selected_dim]

        x_select_dim, y_select_dim = selected_button.x - 10, selected_button.y - 10
        self.windw.blit(self.selector, (y_select_dim, x_select_dim))

        for b in self.buttons.values():
            self.windw.blit(b.image, (b.y, b.x))

        pygame.display.update()


def main():
    width, height = 510, 510
    FPS = 30
    WIN = pygame.display.set_mode((width, height))
    i = 2
    if i == 0:
        G = EndMenu(WIN, FPS, 200, 52)
    if i == 1:
        G = StartMenu(WIN, FPS)
    if i == 2:
        G = SettingMenu(4, True, WIN, FPS)
    if i in (0, 1, 2):
        G.launch()
    pygame.quit()


if __name__ == "__main__":
    main()
