def rem_dup(arr):
    
    arr2 = sorted((arr))
    
    seen = set()
    dup = set()
    
    
    #don't use till line 12 for unsorted array
    if arr != arr2:
        arr = arr2
        print("The array was not sorted in ascending order, so it has been sorted.")
        
    for i in arr:
        if i in seen:
            dup.add(i)
        else:
            seen.add(i)
    
    return list(seen)

h = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = rem_dup(h)
if res:
    print(f"The array after removing duplicates is: {res}")