# -*- coding: utf-8 -*-
import pygame as pg
from settings import WIDTH, HEIGHT, FPS, MOVE_MS_BASE, SPEEDUP_DELTA, SPEEDUP_EVERY, MOVE_MS_MIN
from storage import load_best, save_best, load_skin_index, save_skin_index
from skins import SKINS
from entities import Snake, Food
from ui import draw_background, draw_header, draw_snake, draw_food, draw_menu

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Greedy Snake")
    clock = pg.time.Clock()

    font_big = pg.font.SysFont("arial", 56, bold=True)
    font_small = pg.font.SysFont("arial", 20)

    STATE_MENU, STATE_PLAY = 0, 1
    state = STATE_MENU

    best = load_best()
    skin_idx = load_skin_index()
    wrap = False

    snake = None
    food = None
    score = 0
    paused = False
    move_interval = MOVE_MS_BASE
    move_timer = 0.0

    running = True
    left_btn = right_btn = None

    while running:
        dt = clock.tick(FPS) / 1000.0

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False

                if state == STATE_MENU:
                    if e.key == pg.K_LEFT:
                        skin_idx = (skin_idx - 1) % len(SKINS); save_skin_index(skin_idx)
                    elif e.key == pg.K_RIGHT:
                        skin_idx = (skin_idx + 1) % len(SKINS); save_skin_index(skin_idx)
                    elif e.key in (pg.K_RETURN, pg.K_SPACE):
                        snake = Snake()
                        food = Food(snake)
                        score = 0
                        paused = False
                        move_interval = MOVE_MS_BASE
                        move_timer = 0.0
                        state = STATE_PLAY
                    elif e.key == pg.K_t:
                        wrap = not wrap

                elif state == STATE_PLAY:
                    if e.key == pg.K_p:
                        paused = not paused
                    elif e.key == pg.K_r:
                        snake = Snake()
                        food = Food(snake)
                        score = 0
                        move_interval = MOVE_MS_BASE
                        paused = False
                    elif e.key == pg.K_t:
                        wrap = not wrap
                    elif e.key in (pg.K_LEFT, pg.K_a):
                        snake.set_dir((-1, 0))
                    elif e.key in (pg.K_RIGHT, pg.K_d):
                        snake.set_dir((1, 0))
                    elif e.key in (pg.K_UP, pg.K_w):
                        snake.set_dir((0, -1))
                    elif e.key in (pg.K_DOWN, pg.K_s):
                        snake.set_dir((0, 1))


        if state == STATE_MENU:
            draw_menu(screen, font_big, font_small, skin_idx, best, wrap)
            pg.display.flip()
            continue

        # ======= 游戏中 =======
        current_skin = SKINS[skin_idx]

        if not paused and snake.alive:
            move_timer += dt * 1000
            if move_timer >= move_interval:
                moved = snake.move(wrap)
                move_timer = 0.0
                if not moved and not snake.alive:
                    best = max(best, score); save_best(best)
                else:
                    if snake.head() == food.pos:
                        snake.eat()
                        score += 1
                        if score % SPEEDUP_EVERY == 0:
                            move_interval = max(MOVE_MS_MIN, move_interval - SPEEDUP_DELTA)
                        food.respawn(snake)

        draw_background(screen)
        draw_snake(screen, snake, current_skin)
        draw_food(screen, food, dt, current_skin)
        draw_header(screen, font_big, font_small, score, best, paused, wrap, current_skin)

        if not snake.alive:
            # Game Over
            overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA); overlay.fill((0,0,0,120))
            msg1 = font_big.render("GAME OVER", True, (250, 250, 250))
            msg2 = font_small.render(" Press R: Restart", True, (240, 240, 240))
            msg3 = font_small.render(" Press Esc: Exit", True, (240, 240, 240))

            screen.blit(overlay, (0,0))
            screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 180))
            screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 240))
            screen.blit(msg3, (WIDTH // 2 - msg2.get_width() // 2, 280))

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
