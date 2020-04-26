#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum, IntFlag

import numpy as np
vec = np.array
import csv
from scipy import interpolate

class Surface:
    def __init__(self, csv_filename: str, surface_length: float):
        self._surface_length = surface_length
        with open(csv_filename) as cfn:
            height_data = [float(h) for [h] in csv.reader(cfn)]
            step = surface_length / (len(height_data) - 1)
            xs = np.arange(0.0, surface_length + step, step)
            self._height = interpolate.interp1d(xs, height_data)

    def get_width(self):
        return self._surface_length

    def get_height(self, x):
        return self._height(x)

class Spaceship:
    class Thrust(IntFlag):
        NOPE = 0
        LEFT = 1
        RIGHT = 2
        UP = 4

    _moon_g = 1.6
    _engine_thrust = 1.0
    _engine_mass_per_sec = 1.0

    def __init__(self, mass: float, velocity: vec, position: vec):
        self.mass = mass
        self.velocity = velocity
        self.position = position
        self.thrust = Spaceship.Thrust.NOPE

    def advance(self, delta_t: float):
        self.position += self.velocity * delta_t
        self.velocity += [0, -Spaceship._moon_g * delta_t]

        thrust_vec = vec([0, 0])
        dm = 0
        if Spaceship.Thrust.RIGHT in self.thrust:
            thrust_vec += [1, 0]
            dm += 1
        if Spaceship.Thrust.LEFT in self.thrust:
            thrust_vec += [-1, 0]
            dm += 1
        if Spaceship.Thrust.UP in self.thrust:
            thrust_vec += [0, 1]
            dm += 1

        self.velocity += thrust_vec * delta_t * engine_thrust / self.mass
        self.mass -= Spaceship._engine_mass_per_sec * dm * delta_t

class Model:
    def __init__(self, sf: Surface, ss: Spaceship):
        self.surface = sf
        self.spaceship = ss

    def step(self):
        pass

if __name__ == '__main__':
    raise NotImplementedError("This file is not supposed to be launched as a program")
