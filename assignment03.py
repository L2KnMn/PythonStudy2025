# # 동전 교환 프로그램
# total = int(input("교환할 돈은 얼마인가?  "))
# total = 777777

# coins = [50000, 10000, 5000, 1000, 500, 100, 50, 10]
# number_coins = []
# change = total

# for i, coin in enumerate(coins):
#     number_coins.append(change // coin)  
#     change = change % coin
#     # print(coin, number_coins[i])

# for i in range(coins.__len__()):
#     print("%d원짜리 %d개" % (coins[i], number_coins[i]))
# print("바꾸지 못한 잔돈 %d" % change)

import turtle 
import random 

swidth, sheight, pSize, exitCount = 1300, 800, 3, 0

r, g, b, angle, dist, curX, curY = [0] * 7

turtle.title("거북이가 맘대로 다니기")
turtle.pensize(pSize)
turtle.setup(width=swidth+30, height=sheight+30)
turtle.screensize(swidth, sheight)
turtle.shape('turtle')


red_turtle = turtle.Turtle()  
red_turtle.shape('turtle')
red_turtle.pensize(pSize)
blue_turtle = turtle.Turtle()
blue_turtle.shape('turtle')
blue_turtle.pensize(pSize)
classic_turtle = turtle.Turtle()
classic_turtle.shape('turtle')
classic_turtle.pensize(pSize)

turtles = [red_turtle, blue_turtle, classic_turtle, turtle]

while True:
    for aturtle in turtles:
        r=random.random()
        g=random.random()
        b=random.random()
        
        aturtle.pencolor((r, g, b))

        angle = random.randrange(0, 360)
        dist = random.randrange(1, 100)
        aturtle.left(angle)
        aturtle.forward(dist)
        curX=aturtle.xcor()
        curY=aturtle.ycor()

        if(-swidth / 2 <= curX and curX <= swidth / 2) and\
        (-sheight / 2 <= curY and curY <= sheight/2):
            pass
        else:
            aturtle.penup()
            aturtle.goto(0, 0)
            aturtle.pendown()
            exitCount += 1
    if exitCount >= 5:
        break

turtle.done()