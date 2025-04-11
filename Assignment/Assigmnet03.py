# # 문제 7번 
# # 주사위 게임 
# import random

# dices = []

# for i in range(2):
#     dice = []
#     for j in range(2):
#         dice.append(random.randrange(1, 6))
#     dices.append(dice)

# print("A의 주사위 숫자는 %d %d입니다." % (dices[0][0], dices[0][1]))
# print("B의 주사위 숫자는 %d %d입니다." % (dices[1][0], dices[1][1]))

# if dices[0][0] + dices[0][1] > dices[1][0] + dices[1][1]:
#     print('A가 이겼네요')
# elif dices[0][0] + dices[0][1] == dices[1][0] + dices[1][1]:
#     print('둘이 비겼네요')
# else:
#     print('B가 이겼네요')

# 문제 8번
import turtle
import random
import math

# 기본 설정
swidth, sheight, pSize = 1300, 800, 3
exitCount = 0

turtle.title("거북이가 맘대로 다니고 충돌하면 색 바꾸기기")
turtle.setup(width=swidth + 30, height=sheight + 30)
turtle.screensize(swidth, sheight)
turtle.pensize(pSize)
turtle.tracer(0)  # 수동 화면 업데이트

# 동적으로 생성할 거북이 인스턴스 수 입력받기
num_turtles = 6

# 거북이 인스턴스 생성
turtle.hideturtle()

turtles = []
for _ in range(num_turtles):
    t = turtle.Turtle()
    t.shape('turtle')
    t.penup()
    t.shapesize(1)
    t.goto(random.randrange(-100, 100), random.randrange(-100, 100))
    turtles.append(t)

# 각 거북이의 '남은 이동 거리(pending move)'를 저장할 리스트
pending_moves = [None for _ in range(len(turtles))]
previous_collision = [False for _ in range(len(turtles))]
current_collision = [False for _ in range(len(turtles))]
collision_timer = [0 for _ in range(len(turtles))]

# shapesize(1)일 때 거북이의 대략적인 크기 (충돌 감지를 위한 반지름)
initial_turtle_radius = 10

def get_radius(t):
    stretch_wid, stretch_len, _ = t.shapesize()
    # 터틀 모양은 대략 원형이라 가정하고 충돌 범위를 원형으로 가정합니다
    # print(stretch_wid, stretch_len)
    # 확인 결과 stretch_wid와 stretch_len가 같은 값이므로 
    # 여기서는 stretch_wid를 사용합니다.
    return initial_turtle_radius * (stretch_wid)

def get_distance(t1, t2):
    x1, y1 = t1.xcor(), t1.ycor()
    x2, y2 = t2.xcor(), t2.ycor()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def changeFormRandom(t):
    t.color(random.random(), random.random(), random.random())
    t.shapesize(random.uniform(1, 9))

def collison(turtle_index):
    global turtles, previous_collision, collision_timer, current_collision
    current_collision[turtle_index] = True
    if previous_collision[turtle_index] is False or collision_timer[turtle_index] > 30:
        changeFormRandom(turtles[turtle_index])
        previous_collision[turtle_index] = True        
        collision_timer[turtle_index] = 0
    else:
        collision_timer[turtle_index] = collision_timer[turtle_index] + 1

def animate():
    global turtles, previous_collision, collision_timer, current_collision
    step_size = 5  # 거북이 한 번에 이동할 픽셀 수
    
    # 각 거북이에 대해
    for i, t in enumerate(turtles):
        # pending move가 없으면 새 랜덤 이동을 설정
        if pending_moves[i] is None:
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
            t.goto(0, 0)
            pending_moves[i] = None

    # 충돌 체크
    num_t = len(turtles)
    # 계속 충돌해서 색과 크기가 마구 바뀌는 것을 방지하기 위해 
    # 충돌 했다가 다시 비충돌 상태가 될 때까지 색 바뀜 방지
    for i in range(num_t):
        for j in range(i + 1, num_t):
            radius1 = get_radius(turtles[i])
            radius2 = get_radius(turtles[j])
            if get_distance(turtles[i], turtles[j]) < (radius1 + radius2):  
                # 두 거북이의 반지름 합보다 작으면 충돌
                # 충돌한 두 거북이의 색과 크기를 랜덤하게 변경
                collison(i)
                collison(j)
    for t in range(num_t):
        if current_collision[t] is False:
            previous_collision[t] = False
            collision_timer[t] = 0
    current_collision = [False for _ in range(len(turtles))]

    # 모든 이동을 한 번에 업데이트하여 부드러운 애니메이션 구현
    turtle.update()
    turtle.ontimer(animate, 50)

animate()
turtle.done()