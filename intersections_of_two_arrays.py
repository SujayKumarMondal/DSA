def sec(arr, arr2):
    
    inter = []
    
    for i in arr:
        for j in arr2:
            if i in arr2 and i not in inter:
                inter.append(i)
                
            elif j in arr and j not in inter:
                inter.append(j)
                
    return inter

lo = list(map(int, input("Enter the first array elements separated by spaces: ").split()))
lo2 = list(map(int, input("Enter the second array elements separated by spaces: ").split()))

res = sec(lo, lo2)
if res:
    print(f"The intersection of the two arrays is: {res}")