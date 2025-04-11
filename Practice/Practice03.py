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

# 기본 설정
swidth, sheight, pSize = 1300, 800, 3
exitCount = 0
projectile_speed = 10  # 구슬 이동 속도

turtle.title("거북이가 맘대로 다니고 구슬 발사하기")
turtle.setup(width=swidth + 30, height=sheight + 30)
turtle.screensize(swidth, sheight)
turtle.pensize(pSize)
turtle.tracer(0)  # 수동 화면 업데이트

# 동적으로 생성할 거북이 인스턴스 수 입력받기
num_turtles = 10

# 거북이(발사자) 인스턴스 생성
turtles = []
for _ in range(num_turtles):
    t = turtle.Turtle()
    t.shape('turtle')
    t.pensize(pSize)
    turtles.append(t)

# 각 거북이의 '남은 이동 거리(pending move)'를 저장할 리스트
pending_moves = [None for _ in range(len(turtles))]

# 발사된 구슬(프로젝트일)을 저장할 리스트
projectiles = []

def fire_projectile(shooter):
    """
    shooter: 발사체를 발사하는 거북이 인스턴스
    반환: 새로 생성된 구슬(프로젝트일) Turtle 인스턴스
    """
    proj = turtle.Turtle()
    proj.shape("circle")         # 구슬 모양: circle
    proj.shapesize(0.5)            # 구슬 크기를 작게 조정
    proj.pendown()
    proj.speed(0)                # 애니메이션 속도 최고(수동 제어)
    # 발사자의 현재 위치에서 시작
    proj.goto(shooter.xcor(), shooter.ycor())
    proj.color(shooter.pencolor())  # 발사자의 색상을 따라갈 수도 있음
    # 발사 각도: 발사자의 현재 진행 방향에서 -45도 ~ +45도 내 임의의 각도로 발사
    proj.setheading(shooter.heading() + random.uniform(-45, 45))
    return proj

def animate():
    global exitCount
    step_size = 5  # 거북이 한 번에 이동할 픽셀 수
    
    # 각 발사자(거북이)에 대해
    for i, t in enumerate(turtles):
        # pending move가 없으면 새 랜덤 이동을 설정
        if pending_moves[i] is None:
            t.pencolor(random.random(), random.random(), random.random())
            angle = random.randrange(0, 360)
            distance = random.randrange(20, 100)
            t.setheading(angle)
            pending_moves[i] = distance
        
        # pending move가 있으면 step_size씩 이동
        if pending_moves[i] is not None:
            move = step_size if pending_moves[i] >= step_size else pending_moves[i]
            t.forward(move)
            pending_moves[i] -= move
            if pending_moves[i] <= 0:
                pending_moves[i] = None

        # 화면 범위 체크(거북이 벗어나면 중앙으로)
        curX, curY = t.xcor(), t.ycor()
        if not (-swidth/2 <= curX <= swidth/2 and -sheight/2 <= curY <= sheight/2):
            t.penup()
            t.goto(0, 0)
            t.pendown()
            exitCount += 1
            pending_moves[i] = None

        # **구슬 발사**: 매 업데이트마다 일정 확률(여기서는 5%)로 구슬을 발사
        if random.random() < 0.05:
            proj = fire_projectile(t)
            projectiles.append(proj)

    # 모든 구슬(프로젝트일)에 대해 이동 처리
    for proj in projectiles[:]:
        proj.forward(projectile_speed)
        # 구슬이 화면 범위를 벗어나면 숨기고 리스트에서 제거
        px, py = proj.xcor(), proj.ycor()
        if not (-swidth/2 <= px <= swidth/2 and -sheight/2 <= py <= sheight/2):
            proj.hideturtle()
            proj.clear()
            projectiles.remove(proj)
    
    # 모든 이동을 한 번에 업데이트하여 부드러운 애니메이션 구현
    turtle.update()

    # exitCount가 일정 횟수에 도달하지 않았다면 50ms 후에 다시 animate() 호출
    if exitCount < 5:
        turtle.ontimer(animate, 50)
    else:
        turtle.done()

animate()
turtle.done()