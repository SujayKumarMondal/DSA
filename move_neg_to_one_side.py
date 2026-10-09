def on(arr):
    
    pos = []
    neg = []
    
    for i in arr:
        if i < 0:
            neg.append(i)
        else:
            pos.append(i)
    return pos + neg


k = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = on(k) 
if res:
    print(f"The array after moving all negative numbers to the end is: {res}")