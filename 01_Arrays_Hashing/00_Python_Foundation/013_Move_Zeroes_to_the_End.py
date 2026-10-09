def mo(arr):
    
    for i in arr:
        if i == 0:
            arr.remove(i)
            arr.append(i)
    return arr

y = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = mo(y)
if res:
    print(f"The array after moving all 0's to the end is: {res}")