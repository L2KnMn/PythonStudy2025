# 7주차 실습 시간 예제 (list)

import turtle
import random

myTurtle, tx, ty, tColor, tSize, tShape = [None] * 6
shapeList = turtle.getshapes()

swidth, sheight = 500, 500

for i in range(100):
    random.shuffle(shapeList)
    myTurtle = turtle.Turtle(shapeList[0])