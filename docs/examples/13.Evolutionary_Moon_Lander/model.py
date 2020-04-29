#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional
from enum import IntFlag
from abc import ABC, abstractmethod

import numpy as np
from numpy import array as vec
from numpy.linalg import norm
import csv
from scipy import interpolate


class Relief:
    def __init__(self, csv_filename: str):
        with open(csv_filename) as cfn:
            height_data = [(float(x), float(h)) for [x, h] in csv.reader(cfn)]
            xs, hs = tuple(zip(*height_data))
            self._relief_length = max(xs)
            self._height = interpolate.interp1d(xs, hs)

    def get_width(self):
        return self._relief_length

    def get_height(self, x):
        return float(self._height(x))


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

    def drain_fuel(self, amount: float):
        """
        Drain fuel to decrease weight
        """
        self.fuel_mass = max(self.fuel_mass - amount, 0.0)

    @property
    def mass(self):
        return self.dry_mass + self.fuel_mass

    def advance(self, delta_t: float):
        self.position += self.velocity * delta_t
        self.velocity += [0.0, -Spaceship._moon_g * delta_t]

        thrust_vec = vec([0.0, 0.0])
        dm = 0.0

        if self.fuel_mass > 0.0:
            if Spaceship.Thrust.RIGHT & self.thrust:
                thrust_vec += [0.25, 0.0]
                dm += 0.25
            if Spaceship.Thrust.LEFT & self.thrust:
                thrust_vec += [-0.25, 0.0]
                dm += 0.25
            if Spaceship.Thrust.UP & self.thrust:
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
    def __init__(self):
        self.model: Optional[Model] = None
        pass

    @abstractmethod
    def control(self):
        pass


class ResponsiveCaptin(Captain):
    def __init__(self):
        super().__init__()
        self.controlled_from_outside = False

    def instruct(self, what_engine: Spaceship.Thrust, turn_on: bool):
        self.controlled_from_outside = True
    
    def free(self):
        self.controlled_from_outside = False


class Model:
    def __init__(self, rl: Relief, ss: Spaceship, cap: Captain, default_delta_t = 0.01):
        self.default_delta_t: float = default_delta_t
        self.relief: Relief = rl
        self.spaceship: Spaceship = ss
        self.cap = cap
        cap.model = self
        self.time = 0.0

    def step_delta_t(self, delta_t):
        self.cap.control()
        self.spaceship.advance(delta_t)
        self.time += delta_t
        [sx, sy] = self.spaceship.position
        sv = norm(self.spaceship.velocity)
        if self.relief.get_height(sx) >= sy:
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
