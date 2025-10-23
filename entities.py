# -*- coding: utf-8 -*-
import random
from collections import deque
from settings import GRID_W, GRID_H

def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp_color(c1, c2, t):
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))

class Snake:
    def __init__(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.body = deque([(cx, cy), (cx-1, cy), (cx-2, cy)])
        self.dir = (1, 0)
        self.grow = 0
        self.alive = True

    def set_dir(self, ndir):
        if (-self.dir[0], -self.dir[1]) == ndir:
            return
        self.dir = ndir

    def head(self):
        return self.body[0]

    def move(self, wrap: bool):
        if not self.alive:
            return False
        hx, hy = self.head()
        nx, ny = hx + self.dir[0], hy + self.dir[1]
        if wrap:
            nx %= GRID_W
            ny %= GRID_H
        else:
            if not (0 <= nx < GRID_W and 0 <= ny < GRID_H):
                self.alive = False
                return False
        if (nx, ny) in self.body and (nx, ny) != self.body[-1]:
            self.alive = False
            return False
        self.body.appendleft((nx, ny))
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()
        return True

    def eat(self):
        self.grow += 1

class Food:
    def __init__(self, snake: Snake):
        self.pos = self._spawn(snake)
        self.anim = 0.0

    def _spawn(self, snake: Snake):
        taken = set(snake.body)
        free = [(x, y) for y in range(GRID_H) for x in range(GRID_W) if (x, y) not in taken]
        return random.choice(free) if free else None

    def respawn(self, snake: Snake):
        self.pos = self._spawn(snake)
