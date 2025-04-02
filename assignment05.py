import turtle

swidth, sheight = 800, 500

turtle.title('무지개색 원 그리기')
turtle.setup(width=swidth+50, height=sheight+50)
turtle.screensize(swidth, sheight)

for radius in range(1, 250):
    if radius % 6 == 0:
        turtle.pencolor('red')
    elif radius % 5 == 0:
        turtle.pencolor('orange')
    elif radius % 4 == 0:
        turtle.pencolor('yellow')
    elif radius % 3 == 0:
        turtle.pencolor('green')
    elif radius % 2 == 0:
        turtle.pencolor('blue')
    elif radius % 1 == 0:
        turtle.pencolor('purple')
    turtle.circle(radius)

turtle.done()