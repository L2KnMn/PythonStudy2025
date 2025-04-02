import turtle



a = int(input('정수 입력 : '))

leap_year = False

if a % 4 == 0:
    if a % 100 != 0: 
        leap_year = True
    elif a % 400 == 0:
        leap_year = True

if leap_year:
    print('윤년')
else:
    print('평년')