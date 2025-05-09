import math
import turtle
import random
from tkinter.simpledialog import *


swidth, sheight = 800, 600

turtle.title("회오리 글자")
turtle.shape("turtle")
turtle.setup(swidth + 50, sheight + 50)
turtle.screensize(swidth + 50, sheight + 50)
turtle.penup()

instr = askstring('입력', '이곳에 글자 입력')

cur_r = radius = min(swidth, sheight) / 2 - 100
cnt = 0
txSize = min(swidth, sheight) // 10

for ch in instr:
    angle = cnt / len(instr) * 720
    tx = cur_r * math.cos(math.radians(angle))
    ty = cur_r * math.sin(math.radians(angle))

    turtle.goto(tx, ty)

    turtle.pencolor(random.random(), random.random(), random.random())
    turtle.write(ch, font=('맑은고딕', txSize, 'bold'))

    cnt += 1
    cur_r = (len(instr) - cnt) / len(instr) * radius

turtle.done()


