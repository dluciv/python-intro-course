#!/usr/bin/env python3
from __future__ import annotations

from numpy import array as vec
import pygame
import os
import model
import captain

_scriptdir = os.path.dirname(os.path.realpath(__file__))


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, ship: model.Spaceship):
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.ship = ship
        self.update(0)

    def update(self, dt):
        super().update(dt)
        f = f"{self.ship.fuel_mass:03.0f}"
        vx = f"{self.ship.velocity[0]:0.2f}"
        vy = f"{self.ship.velocity[1]:0.2f}"
        self.image = self.font.render(f"{f} [{vx},{vy}]", True, (255,255,0))
        ir: pygame.Rect = self.image.get_rect()
        self.rect = ir.move(
            int(self.ship.position[0]) - ir.width // 2,
            500 - int(self.ship.position[1]) - ir.height // 2
        )


TIMEREVENT = pygame.USEREVENT + 1

def model_and_repaint():
    global screen, renderups, ship_sprite, clear_screen
    global relief, game_model, cap, ship
    ms = pygame.time.get_ticks()
    t = ms / 1000.0
    game_model.run_to(t)

    renderups.clear(screen, clear_screen)
    ship_sprite.pos = ship.position
    renderups.update(0)

    rects = renderups.draw(screen) # auto + cleared rects
    pygame.display.update(rects)


_key_to_thrust = {
    pygame.K_UP: model.Spaceship.Thrust.UP,
    pygame.K_w: model.Spaceship.Thrust.UP,
    pygame.K_LEFT: model.Spaceship.Thrust.LEFT,
    pygame.K_a: model.Spaceship.Thrust.LEFT,
    pygame.K_RIGHT: model.Spaceship.Thrust.RIGHT,
    pygame.K_d: model.Spaceship.Thrust.RIGHT
}

def main_cycle_body()-> bool:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        return False
    elif event.type == TIMEREVENT:
        model_and_repaint()
    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        print(f"Keyboard event: {event.type}, key: {event.key}")
        ktt = _key_to_thrust.get(event.key)
        if ktt:
            cap.instruct(ktt, event.type == pygame.KEYDOWN)
        else:
            print("Giving controls back to cap!")
            cap.free()
    else:
        pass
        #print(event)
    return True


def start_game():
    global screen, clear_screen, relief

    # fps = clock.get_fps()  # how to get system FPS?..
    fps = 30
    pygame.time.set_timer(TIMEREVENT, int(1000 / fps))

    bg = pygame.image.load(os.path.join(_scriptdir, 'images', "background.jpg"))
    screen.fill((0, 0, 0))
    screen.blit(bg, bg.get_rect())

    for x in range(0, 1500):
        pygame.draw.line(
            screen,
            (160, 160, 160),
            (round(x), 500),
            (round(x), 500 - round(relief.get_height(x)))
        )

    pygame.display.update(pygame.Rect(0, 0, 1500, 500))
    clear_screen = screen.copy()

    while main_cycle_body():
        pass


def main():
    global window, screen, renderups, ship_sprite

    global relief, game_model, cap, ship

    relief = model.Relief("surface_heights.csv")
    ship = model.Spaceship(1000.0, vec([20.0, 0.0]), vec([0.0, 200.0]))
    # cap = captain.BraveCaptain()
    cap = captain.CarefulCaptain()
    game_model = model.Model(relief, ship, cap)

    pygame.init()
    # pygame.mixer.init()
    pygame.font.init()

    ship_sprite = TextSprite(ship)
    renderups = pygame.sprite.RenderUpdates(ship_sprite)
    window = pygame.display.set_mode((1500, 500), 0, 32)
    pygame.display.set_caption("Let's land")
    screen = pygame.display.get_surface()
    start_game()

if __name__ == '__main__':
    main()
