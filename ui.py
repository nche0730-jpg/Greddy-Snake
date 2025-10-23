# -*- coding: utf-8 -*-
import math
import pygame as pg
from settings import (
    WIDTH, HEIGHT, GRID_W, GRID_H, CELL, GAP, MARGIN, HEADER,
    BG_TOP, BG_BOTTOM, GRID_COLOR, BOARD_BG, TXT_DARK, SHADOW
)
from skins import SKINS
from entities import Snake, lerp_color


def cell_rect(cell):
    x, y = cell
    px = MARGIN + x * CELL
    py = HEADER + y * CELL
    return pg.Rect(px + GAP, py + GAP, CELL - 2 * GAP, CELL - 2 * GAP)


def draw_background(screen):

    for i in range(HEIGHT):
        t = i / max(1, HEIGHT)
        c = lerp_color(BG_TOP, BG_BOTTOM, t)
        pg.draw.line(screen, c, (0, i), (WIDTH, i))


    board_rect = pg.Rect(MARGIN, HEADER, GRID_W * CELL, GRID_H * CELL)
    pg.draw.rect(screen, BOARD_BG, board_rect, border_radius=12)


    gx0, gy0 = MARGIN, HEADER
    for x in range(GRID_W + 1):
        xx = gx0 + x * CELL
        pg.draw.line(screen, GRID_COLOR, (xx, gy0), (xx, gy0 + GRID_H * CELL))
    for y in range(GRID_H + 1):
        yy = gy0 + y * CELL
        pg.draw.line(screen, GRID_COLOR, (gx0, yy), (gx0 + GRID_W * CELL, yy))


def draw_snake(screen, snake: Snake, skin):

    shadow_surf = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    for seg in snake.body:
        r = cell_rect(seg)
        rs = r.copy()
        rs.x += 2
        rs.y += 3
        pg.draw.rect(shadow_surf, SHADOW, rs, border_radius=10)
    screen.blit(shadow_surf, (0, 0))


    n = len(snake.body)
    for i, seg in enumerate(snake.body):
        t = i / max(1, n - 1)
        col = lerp_color(skin["SNAKE_HEAD"], skin["SNAKE_TAIL"], t)
        r = cell_rect(seg)
        pg.draw.rect(screen, col, r, border_radius=10)


    hx, hy = snake.head()
    head_r = cell_rect((hx, hy))
    dx, dy = snake.dir
    ex = -6 if dx < 0 else (6 if dx > 0 else 0)
    ey = -6 if dy < 0 else (6 if dy > 0 else 0)
    center1 = (head_r.centerx - 6 + ex, head_r.centery - 4 + ey)
    center2 = (head_r.centerx + 6 + ex, head_r.centery - 4 + ey)
    pg.draw.circle(screen, (20, 35, 41), center1, 4)
    pg.draw.circle(screen, (20, 35, 41), center2, 4)


def draw_food(screen, food, dt, skin):
    if food.pos is None:
        return
    food.anim = (food.anim + dt * 2.5) % 1.0
    x, y = food.pos
    r = cell_rect((x, y))


    scale = 1.0 + 0.06 * math.sin(food.anim * 3.1415 * 2)
    rr = r.inflate(int(r.w * (scale - 1)), int(r.h * (scale - 1)))
    pg.draw.ellipse(screen, skin["APPLE_RED"], rr)


    shine = rr.inflate(-int(rr.w * 0.55), -int(rr.h * 0.55))
    shine.x -= rr.w // 6
    shine.y -= rr.h // 6
    pg.draw.ellipse(screen, (255, 255, 255), shine)


    leaf_rect = pg.Rect(rr.centerx - 4, rr.y - 6, 14, 10)
    pg.draw.ellipse(screen, skin["LEAF"], leaf_rect)


def draw_header(
    screen,
    font_big,
    font_small,
    score,
    best,
    paused,
    wrap,
    skin,
    title_override=None,
    show_hint=True,
):

    title_text = title_override if title_override else "SNAKE"
    title = font_big.render(title_text, True, skin["TITLE"])
    screen.blit(title, (MARGIN, 22))


    def box(label, val, x):
        w, h = 140, 56
        rect = pg.Rect(x, 20, w, h)

        dark_bg = (64, 74, 87)
        pg.draw.rect(screen, dark_bg, rect, border_radius=10)
        lbl = font_small.render(label, True, (255, 255, 255))
        v = font_small.render(str(val), True, (255, 255, 255))
        screen.blit(lbl, (x + (w - lbl.get_width()) // 2, 26))
        screen.blit(v, (x + (w - v.get_width()) // 2, 50))

    box("SCORE", score, WIDTH - MARGIN - 140 * 2 - 12)
    box("BEST", best, WIDTH - MARGIN - 140)




def draw_menu(screen, font_big, font_small, skin_idx, best, wrap):

    skin = SKINS[skin_idx]
    draw_background(screen)


    draw_header(
        screen,
        font_big,
        font_small,
        score=0,
        best=best,
        paused=False,
        wrap=wrap,
        skin=skin,
        title_override="SNAKE — MENU",
        show_hint=False,
    )


    board_rect = pg.Rect(MARGIN, HEADER, GRID_W * CELL, GRID_H * CELL)
    name_y = board_rect.y + int(board_rect.h * 0.70)
    name_surf = font_big.render(skin["name"], True, TXT_DARK)
    screen.blit(name_surf, (board_rect.centerx - name_surf.get_width() // 2, name_y))


    from collections import deque

    fake = Snake()
    fake.body = deque()


    preview_y = GRID_H // 2

    start_x = GRID_W // 2 - 3


    for i in range(6):
        fake.body.append((start_x + i, preview_y))

    fake.dir = (1, 0)
    draw_snake(screen, fake, skin)


    lines = [
        "← / →: Switch skins ",
        "Enter / Space:  Start the game",
        "Esc: Exit",
    ]
    for i, text in enumerate(lines):
        s = font_small.render(text, True, TXT_DARK)
        screen.blit(s, (MARGIN, HEIGHT - 28 - (len(lines) - 1 - i) * 24))



    return
