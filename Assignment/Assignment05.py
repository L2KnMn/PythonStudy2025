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

cur_r = radius = min(swidth, sheight) / 2 * 0.8 ## radius는 원본 길이 cur_r는 실제 그릴 때 사용할 길이
cnt = 0 # 쓴 글자 횟수
txSize = min(swidth, sheight) // 10

for ch in instr:
    angle = cnt / len(instr) * 720 # 각도로 먼저 구함
    tx = cur_r * math.cos(math.radians(angle))
    ty = cur_r * math.sin(math.radians(angle))

    turtle.goto(tx, ty)
    turtle.pencolor(random.random(), random.random(), random.random())
    turtle.write(ch, font=('맑은고딕', txSize, 'bold'))

    ## 다음 루프를 위해 값 변경
    cnt += 1
    cur_r = (len(instr) - cnt) / len(instr) * radius

turtle.done()