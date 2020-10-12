import pygame
import os

from base import Base
from bird import Bird
from pipe import Pipe

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 50)

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


def draw_window(win, bird, pipes, base, score, lost, last_update):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    if lost:
        lose_text = STAT_FONT.render("GAME OVER", 1, (255, 255, 255))
        lose_score = STAT_FONT.render("Final Score: " + str(score), 1, (255, 255, 255))
        win.blit(lose_text, (160, 250))
        win.blit(lose_score, (150, 300))

    if not last_update:
        text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
        pygame.display.update()

    if lost:
        return True
    else:
        return False


def main():
    last_update = False
    lost = False
    bird = Bird(230, 250)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pipes = [Pipe(600)]
    base = Base(730)
    score = 0
    running = True

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                lost = True
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))
            add_pipe = False

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img .get_height() >= 730 or bird.y < 0:
            lost = True

        bird.move()
        base.move()
        last_update = draw_window(win, bird, pipes, base, score, lost, last_update)


if __name__ == "__main__":
    main()
