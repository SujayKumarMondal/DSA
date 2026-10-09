def largest(arr):
    
    lar = arr[0]
    for i in arr:
        if i > lar:
            lar = i
    return lar

g = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = largest(g)
if res:
    print(f"The largest element in the array is: {res}")