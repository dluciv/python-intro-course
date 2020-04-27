#!/usr/bin/env python3
from __future__ import annotations
from typing import List

import numpy as np
from numpy import array as vec
import matplotlib.pyplot as plt

import model
import captain


def trackship(m: model.Model) -> List[vec]:
    poss = []
    while m.step():
        poss.append(m.spaceship.position.copy())
    return poss

if __name__ == '__main__':
    sur = model.Surface("surface_heights.csv", 1500.0)

    m = model.Model(
        sur,
        model.Spaceship(1000.0, vec([20.0, 0.0]), vec([0.0, 200.0])),
        captain.CarefulCaptain(verbose=False)
    )

    xs = np.arange(0.0, sur.get_width())
    plt.plot(xs, [sur.get_height(x) for x in xs])

    poss = trackship(m)
    tx, ty = tuple(zip(*poss))
    plt.plot(tx, ty)

    plt.show()
