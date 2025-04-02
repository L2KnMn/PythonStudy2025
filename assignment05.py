a = int(input('정수 입력 : '))

if a >= 90:
    print('A', end='')
elif a >= 80:
    print('B', end='')
elif a>= 70:
    print('C', end='')
elif a >= 60:
    print('D', end='')
else:
    print('F', end='')

if a % 10 >= 5:
    print("+", end='')

print("학점 ^^")