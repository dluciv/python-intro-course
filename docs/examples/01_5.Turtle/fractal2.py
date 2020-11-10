import turtle as tl

def draw_fractal(size):
    if size >= 5:
        tl.forward(size)
        tl.left(35)
        tl.forward(size)
        draw_fractal(size / 2)
        tl.backward(size)
        tl.right(65)
        tl.forward(size)
        draw_fractal(size / 1.5)
        tl.backward(size)
        tl.left(30)
        tl.backward(size)
    else:
        tl.circle(2)
        

size = 100
tl.penup()
tl.color('green')
tl.goto(0, -size * 2)
tl.setheading(90)
tl.pendown()

draw_fractal(size)
tl.done()
