# #3부터 100까지의 소수 구해서 출력하기
# import math
#
# prime_number = []
#
# number = 2
# while number <= 100:
#     q = math.sqrt(number)
#     q = int(q)
#     b = False
#     for s in prime_number:
#         if q < s:
#             break
#         if (number % s) == 0:
#             b = True
#             break
#     if not b:
#         prime_number.append(number)
#     number = number + 1
# print(prime_number)

# 거북이로 별 그리기
import turtle
import random

def drawStartRandom():
    len = random.randint(10, 200)
    random_24bit = random.randint(0, 0xFFFFFF)
    # 8비트 단위로 나누어 RGB 값 할당
    r = (random_24bit >> 16) & 0xFF # 상위 8비트
    g = (random_24bit >> 8) & 0xFF  # 중간 8비트
    b = random_24bit & 0xFF         # 하위 8비트
    turtle.colormode(255)
    turtle.color(r, g, b)
    turtle.pencolor((r, g, b))
    turtle.pendown()
    for i in range(5):
        turtle.forward(len)
        turtle.right(144)

turtle.title('파이썬 과제 4번 연습문제 9번')
turtle.shape('turtle')
width, height = turtle.Screen().screensize()

while(True):
    turtle.penup()
    turtle.goto(random.randint(-width//2, width//2), random.randint(-height//2, height//2))
    turtle.pendown()
    drawStartRandom()

turtle.done()