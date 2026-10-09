def minimum(arr):
    
    min = arr[0]
    for i in arr:
        if i < min:
            min = i
    return min

o = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = minimum(o)   
if res:
    print(f"The minimum element in the array is: {res}")