import turtle as tl
import time
import math
import numpy as np

MODEL_DT = 0.05
MODEL_G = 9.81
MODEL_T = 15

sc = tl.Screen()    # показ экрана
tl.hideturtle()     # спрятать черепашку по умолчанию
tl.tracer(0,0)      # отключение автоматического обновления экрана

class Body:
    def __init__(self, x, y, vx, vy, color = 'black'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.turtle = tl.Turtle()
        self.turtle.hideturtle()
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.radians() # Переключились на радианы
        self._draw()
        self.turtle.showturtle()

    def _draw(self):
        self.turtle.setheading(math.atan2(self.vy, self.vx))
        self.turtle.goto(self.x, self.y)

    def advance(self):
        self.x += self.vx * MODEL_DT
        self.y += self.vy * MODEL_DT

        self.vy -= MODEL_G * MODEL_DT

        self._draw()

bodies = [
    Body(-300, 0, 50.0, 50.0, 'blue'),
    Body(-300, 0, 55.0, 45.0, 'red')
]

def up():
    bodies[0].vy += 3

sc.onkey(up, "Up")
sc.listen()

t0 = time.time()
for t in np.arange(t0, t0 + MODEL_T + MODEL_DT, MODEL_DT):
    for b in bodies:
        b.advance()
    st = t + MODEL_DT - time.time()
    if st > 0:
        time.sleep(st)
        tl.update()
tl.done()
