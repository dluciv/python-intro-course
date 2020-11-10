import turtle as tl

def draw_fractal(size):
    if size >= 5:
        tl.pensize(max(size / 50, 1))
        tl.forward(size)
        tl.left(35)
        draw_fractal(size / 2)
        tl.right(65)
        draw_fractal(size / 1.5)
        tl.left(30)
        tl.penup()
        tl.backward(size)
        tl.pendown()
    else:
        tl.pensize(3)
        tl.dot()
        
size = 300

tl.delay(1)  # уменьшение задержки для скорости
tl.penup()
tl.color('green')
tl.goto(0, -size * 2)
tl.setheading(90)
tl.pendown()

draw_fractal(size)
tl.done()
