def r(arr):
    
    l = len(arr)
    
    for i in range(l-1, -1, -1):
        print(arr[i], end=" ")
        
    return arr

y = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = r(y)

if res:
    print("\nThe array has been reversed.")