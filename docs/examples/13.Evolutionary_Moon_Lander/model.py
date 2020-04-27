#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum, IntFlag
from abc import ABC, abstractmethod

import numpy as np
from numpy import array as vec
from numpy.linalg import norm
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
    _engine_thrust = 3000.0
    _engine_mass_per_sec = 3.0

    def __init__(self, mass: float, velocity: vec, position: vec):
        self.maxlandingvelocity: float = 1.0
        self.navigates = True
        self.ok: bool = True
        self.velocity: vec = velocity
        self.position: vec = position
        self.thrust: Spaceship.Thrust = Spaceship.Thrust.NOPE

        self.dry_mass: float = mass / 2.0
        self.fuel_mass: float = mass / 2.0

    @property
    def mass(self):
        return self.dry_mass + self.fuel_mass

    def advance(self, delta_t: float):
        self.position += self.velocity * delta_t
        self.velocity += [0.0, -Spaceship._moon_g * delta_t]

        thrust_vec = vec([0.0, 0.0])
        dm = 0.0

        if self.fuel_mass > 0.0:
            if Spaceship.Thrust.RIGHT in self.thrust:
                thrust_vec += [0.25, 0.0]
                dm += 0.25
            if Spaceship.Thrust.LEFT in self.thrust:
                thrust_vec += [-0.25, 0.0]
                dm += 0.25
            if Spaceship.Thrust.UP in self.thrust:
                thrust_vec += [0.0, 1.0]
                dm += 1.0

        self.velocity += thrust_vec * delta_t * Spaceship._engine_thrust / self.mass
        self.fuel_mass -= Spaceship._engine_mass_per_sec * dm * delta_t
    
    def land(self):
        self.velocity = vec([0.0, 0.0])
        self.navigates = False

    def crash(self):
        self.land()
        self.ok = False

class Captain(ABC):
    def __init__(self, ):
        pass

    @abstractmethod
    def control(self, surface: Surface, spaceship: Spaceship, time: float):
        pass


class Model:
    def __init__(self, sf: Surface, ss: Spaceship, cap: Captain, default_delta_t = 0.01):
        self.default_delta_t: float = default_delta_t
        self.surface: Surface = sf
        self.spaceship: Spaceship = ss
        self.cap = cap
        self.time = 0.0

    def step_delta_t(self, delta_t):
        self.cap.control(self.surface, self.spaceship, self.time)
        self.spaceship.advance(delta_t)
        self.time += delta_t
        [sx, sy] = self.spaceship.position
        sv = norm(self.spaceship.velocity)
        if self.surface.get_height(sx) >= sy:
            self.spaceship.navigates = False
            if sv <= self.spaceship.maxlandingvelocity:
                print("Landing ok!")
                self.spaceship.land()
            else:
                print("Crash...")
                self.spaceship.crash()

    def step(self) -> bool:
        self.step_delta_t(self.default_delta_t)
        return self.spaceship.navigates

    def run_to(self, up_to_time: float = None) -> bool:
        if up_to_time is None:
            up_to_time = self.time + self.default_delta_t

        while self.time < up_to_time and self.spaceship.navigates:
            self.step_delta_t(self.default_delta_t)

        return self.spaceship.navigates


if __name__ == '__main__':
    raise NotImplementedError("This file is not supposed to be launched as a program")
