def buy_sell(arr):
    
    max_profit = 0
    l = len(arr)
    for h in range(l):
        for a in range(h+1, l):
            profit = arr[a] - arr[h]
            if profit > max_profit:
                max_profit = profit
    return max_profit            
            
g = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = buy_sell(g)
if res:
    print(f"The maximum profit from buying and selling the stock is: {res}")
