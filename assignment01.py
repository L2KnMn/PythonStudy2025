a = int(input('첫번째 숫자를 입력하시오:'))
b = int(input('두번째 숫자를 입력하시오:'))
c = int(input('세번째 숫자를 입력하시오:'))

result = a+b+c
print(a, '+', b, '+', c, '=', result)
result = a*b*c
print(a, '*', b, '*', c, '=', result)



import turtle
import random

isHandle = False # 이벤트 처리 중 호출 시 작업이 중단되는 것을 제어
pSize = 10

def screenClick(x, y):
    global isHandle
    if isHandle:
        return
    isHandle = True
    random_24bit = random.randint(0, 0xFFFFFF)
    # 8비트 단위로 나누어 RGB 값 할당
    r = (random_24bit >> 16) & 0xFF # 상위 8비트
    g = (random_24bit >> 8) & 0xFF   # 중간 8비트
    b = random_24bit & 0xFF          # 하위 8비트
    turtle.color(r, g, b)
    turtle.pencolor((r, g, b))
    #거북이 이동 및 선 그리기
    turtle.pendown()
    turtle.goto(x, y)
    #이동 후 
    #랜덤한 크기, 각도의 거북이 도장찍기
    tSize = random.randrange(1, 10)
    turtle.shapesize(tSize)
    turtle.tracer(0) # 거북이 애니메이션 비활성
    turtle.setheading(random.randrange(0, 360)) #거북이 회전
    turtle.update() # 애니메이션이 비활성 상태이므로 직접 그리기
    turtle.tracer(1) # 애니메이션 재활성
    turtle.stamp()
    isHandle = False # 거북이 조작 종료

turtle.title('파이썬 과제 1번 연습문제 8번')
turtle.shape('turtle')
turtle.pensize(pSize)
turtle.colormode(255) # 거북이의 색, 0부터 255 정수 단위로 설정
turtle.onscreenclick(screenClick, 3)

turtle.done()