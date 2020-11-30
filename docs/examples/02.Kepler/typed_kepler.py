#!/usr/bin/env python3

"""
Численное решение задачи скольких-то тел
"""

from __future__ import annotations  # !! typing
from abc import abstractmethod, ABC
from typing import List
from numpy import array as vec
import numpy.linalg
import matplotlib.pyplot as plt
import matplotlib.axes


class Body:
    """Тело, движущаееся по двумерной плоскости"""

    def __init__(self, universe: Universe, mass: float, position: vec, velocity: vec):
        # Аннотации типов по желанию, но могут помочь IDE и компилятору, когда таковые имеются
        self.universe: Universe = universe
        self.mass: float = mass
        self.position: vec = position
        self.velocity: vec = velocity

    def force_induced_by_other(self, other: Body) -> vec:
        """Сила, с которой другое тело действует на данное"""
        # Body is forward reference here
        delta_p = other.position - self.position
        distance = numpy.linalg.norm(delta_p)  # Евклидова норма (по теореме Пифагора)
        force_direction = delta_p / distance
        force = force_direction * self.mass * other.mass *\
                self.universe.gravity_flow_dencity_per_1_1(distance)
        return force

    def advance(self):
        """Перемещаем тело, исходя из его скорости"""
        self.position += self.velocity * MODEL_DELTA_T

    def apply_force(self, force: vec):
        """Изменяем скорость, исходя из силы, действующей на тело"""
        self.velocity += force * MODEL_DELTA_T / self.mass


# ABC это не алфавит, а AbstractBaseClass. Не даст создать экземпляр, пока не переопределишь все методы-заглушки
class Universe(ABC):
    """Невнятная вселенная, основа всех миров"""

    def __init__(self,
                 G: float,  # гравитационная постоянная
                 collision_distance: float  # всё-таки это не точки
                 ):
        self.G: float = G
        self.collision_distance: float = collision_distance


    @abstractmethod
    def gravity_flow_dencity_per_1_1(self, dist: float) -> float:
        """
        Плотность потока гравитационного поля между двумя
        единичными массами на заданном расстоянии
        """
        ...

    @abstractmethod
    def model_step(self):
        """Итерация решения задачи Коши. Конечно не присуща вселенной, но тут на своём месте"""
        ...

class UniverseWith3Bodies(Universe):
    """
    Демо-вселенная.
    Кому угодно понятно, что она ненастоящая.
    Зато уже есть.
    """

    def __init__(self,
                 G: float,  # гравитационная постоянная
                 collision_distance: float  # всё-таки это не точки
                 ):
        """В начале было... да, а потом тестовая вселенная с пупом мира и двумя камнями"""
        super().__init__(G, collision_distance)

        self.centrum = Body(self, 500.0, vec([0.0, 0.0]), vec([0.0, 0.0]))
        self.p_1 = Body(self, 10.0, vec([50.0, 0.0]), vec([0.0, 15.0]))
        self.p_2 = Body(self, 10.0, vec([50.0, 40.0]), vec([-7.0, 7.0]))

    def gravity_flow_dencity_per_1_1(self, dist: float) -> float:
        # будем считать, что отскакивают точки друг от друга резко,
        # но стараться не допускать этого
        return self.G / (
            dist ** 2 if dist > self.collision_distance
            else -self.G / dist ** 3
        )

    def model_step(self):
        self.p_1.apply_force(self.p_1.force_induced_by_other(self.centrum))
        self.p_2.apply_force(self.p_2.force_induced_by_other(self.centrum))
        self.p_1.advance()
        self.p_2.advance()

class UniverseWithBodies(Universe):
    """
    Будем считать, что это наша вселенная. Кстати, в ней тела действуют и
    друг на друга.
    """

    def __init__(self,
                 G: float,  # гравитационная постоянная
                 collision_distance: float  # всё-таки это не точки
                 ):
        super().__init__(G, collision_distance)
        self.bodies: List[Body] = []

    def add_body(self, b: Body):
        raise NotImplementedError("Запрограммируй меня!")

    @abstractmethod
    def gravity_flow_dencity_per_1_1(self, dist: float) -> float:
        pass

    @abstractmethod
    def model_step(self):
        pass


class UniverseWithDimensionsAndBodies(UniverseWithBodies):
    """
    А это уже вселенная, у которой пространственных измерений, сколько скажут
    """

    def __init__(self,
                 dimensions: int, # сколько пространственных измерений
                 G: float,  # гравитационная постоянная
                 collision_distance: float  # всё-таки это не точки
                 ):
        super().__init__(G, collision_distance)
        self.dimensions = dimensions

    def gravity_flow_dencity_per_1_1(self, dist: float) -> float:
        # Должна использовать self.dimensions
        raise NotImplementedError("Запрограммируй меня!")


if __name__ == '__main__':

    un = UniverseWith3Bodies(50, 3.0)

    MODEL_DELTA_T = 0.01
    TIME_TO_MODEL = 10

    xs_1 = []
    ys_1 = []
    xs_2 = []
    ys_2 = []
    for stepn in range(int(TIME_TO_MODEL / MODEL_DELTA_T)):
        xs_1.append(un.p_1.position[0])
        ys_1.append(un.p_1.position[1])
        xs_2.append(un.p_2.position[0])
        ys_2.append(un.p_2.position[1])
        un.model_step()

    c = plt.Circle((0, 0), 2, color='b')
    ax: matplotlib.axes.Axes = plt.gca()  # !! typing
    ax.set_aspect('equal')
    ax.add_patch(c)

    plt.plot(xs_1, ys_1)
    plt.plot(xs_2, ys_2)

    plt.show()
