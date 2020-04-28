#!/usr/bin/env python3
from __future__ import annotations

import model

class BraveCaptain(model.Captain):
    def control(self):
        surface = self.model.surface
        spaceship = self.model.spaceship
        time = self.model.time

        drained = False
        if 5.0 < time < 10.0:
            spaceship.thrust = model.Spaceship.Thrust.UP
        elif 26.5 < time < 27.0 or 30.0 < time < 30.5:
            if not drained:
                spaceship.drain_fuel(200)
            spaceship.thrust = model.Spaceship.Thrust.UP | model.Spaceship.Thrust.LEFT
        else:
            spaceship.thrust = model.Spaceship.Thrust.NOPE


class CarefulCaptain(model.Captain):
    def __init__(self, verbose = True):
        self.count = 0
        self.verbose = verbose

    def control(self):
        surface = self.model.surface
        spaceship = self.model.spaceship
        time = self.model.time
        left = spaceship.velocity[0] > spaceship.maxlandingvelocity / 2.0 ** 0.5
        up =   spaceship.velocity[1] < -spaceship.maxlandingvelocity / 2.0 ** 0.5

        spaceship.thrust = \
            (model.Spaceship.Thrust.LEFT if left else model.Spaceship.Thrust.NOPE) | \
            (model.Spaceship.Thrust.UP if up else model.Spaceship.Thrust.NOPE)

        if self.verbose and self.count % 1000 == 0:
            print(time, spaceship.thrust, spaceship.mass)
        self.count += 1

