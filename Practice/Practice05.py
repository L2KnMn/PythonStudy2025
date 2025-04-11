menu = input("입력한 수식 계산 : 1 | 두 수 사이의 합계 : 2  ")

if menu == '1':
    numstr = input(" 수식을 입력하세요 : ")
    print('결과는 %5.1f입니다' % eval(numstr))
elif menu == '2':
    num1 = int(input('첫번째 숫자를 입력 : '))
    num2 = int(input('두번째 숫자를 입력 : '))
    result = ((num2 - num1 + 1) * (num2 + num1) / 2)
    print('결과는 %d입니다.' % result)
else:
    print('잘못된 요청입니다.')
