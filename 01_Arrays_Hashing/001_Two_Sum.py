def two_sum(arr, t):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == t:
                return [i, j]   
            


l= list(map(int, input("enter arr elements separated by space: ").split()))
t = int(input("enter target sum: "))
res = two_sum(l, t)
if res:
    print(f"Indices of elements that sum to {t}: {res}")