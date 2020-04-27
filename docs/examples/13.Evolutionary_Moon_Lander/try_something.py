#!/usr/bin/env python3
from __future__ import annotations
from typing import List

import numpy as np
from numpy import array as vec
import matplotlib.pyplot as plt

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
    def __init__(self):
        self.count = 0

    def control(self, surface: model.Surface, spaceship: model.Spaceship, time: float):
        left = spaceship.velocity[0] > spaceship.maxlandingvelocity / 2.0
        up =   spaceship.velocity[1] < -spaceship.maxlandingvelocity / 2.0

        spaceship.thrust = \
            (model.Spaceship.Thrust.LEFT if left else model.Spaceship.Thrust.NOPE) | \
            (model.Spaceship.Thrust.UP if up else model.Spaceship.Thrust.NOPE)

        if self.count % 1000 == 0:
            print(time, spaceship.thrust, spaceship.mass)
        self.count += 1


def trackship(m: model.Model) -> List[vec]:
    poss = []
    while m.step():
        poss.append(m.spaceship.position.copy())
    return poss

if __name__ == '__main__':
    sur = model.Surface("surface_heights.csv", 2000.0)

    m = model.Model(
        sur,
        model.Spaceship(1000.0, vec([25.0, 0.0]), vec([0.0, 200.0])),
        CarefulCaptain()
    )

    xs = np.arange(0.0, sur.get_width())
    plt.plot(xs, [sur.get_height(x) for x in xs])

    poss = trackship(m)
    tx, ty = tuple(zip(*poss))
    plt.plot(tx, ty)

    plt.show()
