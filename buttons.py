#!/usr/bin/env python3
import pygame, pygame.freetype
from PIL import ImageFont, ImageDraw, Image

from constants import *

pygame.freetype.init()


class Button:
    def __init__(self, label, x, y, width=300, height=60):
        self.width, self.height = width, height
        self.label = label
        image = self.generate_image()
        image = pygame.transform.scale(image, (self.width, self.height))
        self.image = image
        self.x, self.y = int(x), int(y)
        self.rect = pygame.Rect(self.y, self.x, self.width, self.height)

    def set_position(self, x, y):
        self.x, self.y = int(x), int(y)
        self.rect.update(self.y, self.x, self.width, self.height)

    def generate_image(self):
        img = Image.new("RGB", (4 * self.width, 4 * self.height))
        self.draw_label(img)
        mode, size, data = img.mode, img.size, img.tobytes()
        img = pygame.image.fromstring(data, size, mode)
        return img

    def draw_label(self, img):
        draw = ImageDraw.Draw(img)
        FONTPATH = "./Assets/fonts/BRAVEEightyone-Regular.ttf"
        FONT = ImageFont.truetype(FONTPATH, int(2.4 * self.height))
        draw.text(
            (0.3 * self.width, self.height * 0.3),
            self.label,
            font=FONT,
            fill=(0xFF, 0xFF, 0xFF),
        )

    def react(self):
        react_dict = {
            "3": SELECT_3,
            "4": SELECT_4,
            "5": SELECT_5,
            "<": SELECT_R,
            "new game": STARTs,
            "exit": EXITs,
            "settings": SETTINGs,
        }
        try:
            # print("post event ",self.label)
            pygame.event.post(pygame.event.Event(react_dict[self.label]))
            if self.label in ("3", "4", "5", "<", "settings"):
                CLICK_SOUND.play()
        except:
            print("exception evenement nom reconnu")


class SelectButton(Button):
    def __init__(self, label, x, y, width=60, height=60):
        super().__init__(label, x, y, width, height)

    def draw_label(self, img):
        img.putalpha(35)
        draw = ImageDraw.Draw(img)
        FONTPATH = "./Assets/fonts/BRAVEEightyone-Regular.ttf"
        FONT = ImageFont.truetype(FONTPATH, int(3.2 * self.height))
        draw.text(
            (0.9 * self.width, 0.05 * self.height),
            self.label,
            font=FONT,
            fill=(24, 61, 222),
        )


class OnOffButton(Button):
    def __init__(self, on_off_dict, init_state, x, y, width=60, height=60):
        self.on_off_dict = on_off_dict
        self.state = init_state
        label = self.on_off_dict[self.state]
        super().__init__(label, x, y, width, height)

    def update_image(self):
        self.label = self.on_off_dict[self.state]
        image = self.generate_image()
        image = pygame.transform.scale(image, (self.width, self.height))
        self.image = image

    def draw_label(self, img):
        img.putalpha(25)
        draw = ImageDraw.Draw(img)
        FONTPATH = "./Assets/fonts/Gore Rough.otf"
        FONT = ImageFont.truetype(FONTPATH, int(2.4 * self.height))
        draw.text(
            (0.2 * self.width, self.height * 0.3),
            self.label,
            font=FONT,
            fill=(40, 129, 212),
        )

    def react(self):
        self.state = not (self.state)
        self.update_image()
        pygame.event.post(pygame.event.Event(SELECT_S))
        CLICK_SOUND.play()
