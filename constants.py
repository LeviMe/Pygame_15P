#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 19:46:13 2021

@author: levi
"""

import pygame
import os

STARTe = pygame.USEREVENT + 10
EXITe = pygame.USEREVENT + 17
STARTs = pygame.USEREVENT + 1
EXITs = pygame.USEREVENT + 12
SETTINGs = pygame.USEREVENT + 19
SETTINGe = pygame.USEREVENT + 20

SELECT_3 = pygame.USEREVENT + 81
SELECT_4 = pygame.USEREVENT + 82
SELECT_5 = pygame.USEREVENT + 83
SELECT_S = pygame.USEREVENT + 84
SELECT_R = pygame.USEREVENT + 85

pygame.mixer.init()
START_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "start.wav"))
CLICK_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "click.wav"))
MOVE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "move.wav"))
WIN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "Win.wav"))

NB_SHUFFLE = 10000
