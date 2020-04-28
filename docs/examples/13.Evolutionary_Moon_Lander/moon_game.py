#!/usr/bin/env python3
from __future__ import annotations

from numpy import array as vec
import pygame
import pygame.sprite as sprite

import model
import captain

class TextSprite(sprite.Sprite):
    def __init__(self, ship: model.Spaceship):
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.ship = ship
        self.update(0)

    def update(self, dt):
        super().update(dt)
        self.image = self.font.render(f"{self.ship.mass:03.0f}", True, (255,255,0))
        self.rect = self.image.get_rect().move(self.ship.position[0], 500 - self.ship.position[1])


TIMEREVENT = pygame.USEREVENT + 1

def model_and_repaint():
    global screen, renderups, ship_sprite, clear_screen
    global sur, game_model, cap, ship
    ms = pygame.time.get_ticks()
    t = ms / 1000.0
    game_model.run_to(t)

    renderups.clear(screen, clear_screen)
    ship_sprite.pos = ship.position
    renderups.update(0)

    rects = renderups.draw(screen) # auto + cleared rects
    pygame.display.update(rects)



def main_cycle_body()-> bool:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        return False
    elif event.type == TIMEREVENT:
        model_and_repaint()
    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        print(f"Keyboard event: {event.type}, key: {event.key}")
        if event.key == pygame.K_UP:
            print("This captain does not listen to your instructions")
        elif event.key == pygame.K_RIGHT:
            print("This captain does not listen to your instructions")
        elif event.key == pygame.K_LEFT:
            print("This captain does not listen to your instructions")
    else:
        pass
        #print(event)
    return True


def start_game():
    global clock, screen, clear_screen, sur

    fps = clock.get_fps()
    fps = 30
    pygame.time.set_timer(TIMEREVENT, int(1000 / fps))

    for x in range(0, 1500):
        pygame.draw.line(screen, (160, 160, 160), (x, 500), (x, 500 - sur.get_height(x)))

    pygame.display.update(pygame.Rect(0, 0, 1500, 500))
    clear_screen = screen.copy()


    while main_cycle_body():
        pass


def main():
    global clock, window, screen, renderups, ship_sprite

    global sur, game_model, cap, ship

    sur = model.Surface("surface_heights.csv", 1500.0)
    ship = model.Spaceship(1000.0, vec([20.0, 0.0]), vec([0.0, 200.0]))
    # cap = captain.BraveCaptain()
    cap = captain.CarefulCaptain(verbose=False)
    game_model = model.Model(sur, ship, cap)

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    ship_sprite = TextSprite(ship)
    renderups = sprite.RenderUpdates(ship_sprite)
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1500, 500), 0, 32)
    pygame.display.set_caption("Let's land")
    screen = pygame.display.get_surface()
    start_game()

if __name__ == '__main__':
    main()
