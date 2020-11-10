import turtle as tl

def draw_fractal(size):
    if size >= 5:
        draw_fractal(size / 3.0)
        tl.left(45)
        draw_fractal(size / 3.0)
        tl.right(90)
        draw_fractal(size / 3.0)
        tl.left(45)
        draw_fractal(size / 3.0)
    else:
        tl.forward(size)

size = 400
tl.penup()
tl.goto(-size, -size/4)
tl.pendown()

draw_fractal(size)
tl.done()
