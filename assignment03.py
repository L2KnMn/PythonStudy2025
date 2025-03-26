# 동전 교환 프로그램

total = int(input("교환할 돈은 얼마인가?  "))

coins = [500, 100, 50, 10]
number_coins = [ 0, 0, 0, 0 ]
change = total

for i, coin in enumerate(coins):
    number_coins[i] = change // coin  
    change = change % coin
    print(coin, number_coins[i])

print("500원 짜리 %d개" % (number_coins[0]))
