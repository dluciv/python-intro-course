#!/usr/bin/env python3
from __future__ import annotations

import model

class BraveCaptain(model.Captain):
    def control(self, surface: model.Surface, spaceship: model.Spaceship, time: float):
        if 5.0 < time < 20.0:
            spaceship.thrust = model.Spaceship.Thrust.UP
        elif 25.0 < time < 40.0:
            spaceship.thrust = model.Spaceship.Thrust.UP | model.Spaceship.Thrust.LEFT
        else:
            spaceship.thrust = model.Spaceship.Thrust.NOPE


class CarefulCaptain(model.Captain):
    def __init__(self, verbose = True):
        self.count = 0
        self.verbose = verbose

    def control(self, surface: model.Surface, spaceship: model.Spaceship, time: float):
        left = spaceship.velocity[0] > spaceship.maxlandingvelocity / 2.0
        up =   spaceship.velocity[1] < -spaceship.maxlandingvelocity / 2.0

        spaceship.thrust = \
            (model.Spaceship.Thrust.LEFT if left else model.Spaceship.Thrust.NOPE) | \
            (model.Spaceship.Thrust.UP if up else model.Spaceship.Thrust.NOPE)

        if self.verbose and self.count % 1000 == 0:
            print(time, spaceship.thrust, spaceship.mass)
        self.count += 1

