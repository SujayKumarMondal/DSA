def dup(arr):
    f = set()
    dup = set()
    
    for i in arr:
        if i in f:
            dup.add(i)
        f.add(i)
    return dup

arr = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = dup(arr)
if res:
    print(f"The array contains duplicate elements, elements are: {res}")
