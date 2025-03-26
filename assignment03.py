# 동전 교환 프로그램
# total = int(input("교환할 돈은 얼마인가?  "))
total = 777777

coins = [50000, 10000, 5000, 1000, 500, 100, 50, 10]
number_coins = []
change = total

for i, coin in enumerate(coins):
    number_coins.append(change // coin)  
    change = change % coin
    # print(coin, number_coins[i])

for i in range(coins.__len__()):
    print("%d원짜리 %d개" % (coins[i], number_coins[i]))
print("바꾸지 못한 잔돈 %d" % change)