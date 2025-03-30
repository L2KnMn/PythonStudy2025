# # 동전 합계 프로그램
# total = 0

# coins = [500, 100, 50, 10]
# number_coins = []

# for i, coin in enumerate(coins):
#     number_coins.append(int(input("%d 짜리 개수 --> " % coin)))  
#     total += coin * number_coins[-1]

# print("## 동전의 합계 ==> %d" % total)

# 논리합 거북이 그림
import turtle

# 이진수 입력 및 저장
b = []
b.append(int(input('2진수를 입력하세요 : '), 2))
b.append(int(input('2진수를 입력하세요 : '), 2))
b.append(b[0] | b[1])

#초기 설정 변수
width = 1200
height = 800
term_x = 80
term_y = 100

# turtle의 초기 설정
turtle.setup(width, height)
turtle.tracer(0)
turtle.penup()
turtle.shape('turtle')
turtle.left(90)
turtle.goto(width/2 - 20, 100)

# 0일 경우 찍을 도장
def stamp0():
    turtle.shapesize(1)
    turtle.color('blue')
    turtle.goto(turtle.xcor() - term_x, turtle.ycor())
    turtle.stamp()
# 1일 경우 찍을 도장
def stamp1():
    turtle.shapesize(3)
    turtle.color('red')
    turtle.goto(turtle.xcor() - term_x, turtle.ycor())
    turtle.stamp()

# b에서 변수 하나를 얻어내고 
for a in b:
    binary = [] # binary 배열에 각 자리의 0과 1값을 담아두기
    number = a  # 혹시 a의 원본값이 필요할 수 있으니 복사하여 다른 변수를 두어 해당 값 변경 저장하기
    while number > 1: # 뒷자리부터 하나씩 구할 수 있음
        binary.append(number % 2)
        number = number // 2
    if number > 0:
        binary.append(number % 2)
    for n in binary: # 뒷자리부터 하나씩 앞으로 가면서 찍기
        if n == 1:
            stamp1()
        else:
            stamp0()
    turtle.goto(580, turtle.ycor() - term_y) # 다음 줄로 변경
turtle.done()

