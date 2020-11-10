import turtle as tl

def draw_fractal(scale):
    if scale >= 5:
        draw_fractal(scale / 3.0)
        tl.left(45)
        draw_fractal(scale / 3.0)
        tl.right(90)
        draw_fractal(scale / 3.0)
        tl.left(45)
        draw_fractal(scale / 3.0)
    else:
        tl.forward(scale)

scale = 400
tl.pensize(2)
tl.penup()
tl.goto(-scale, -scale/4)
tl.pendown()

draw_fractal(scale)
tl.done()
