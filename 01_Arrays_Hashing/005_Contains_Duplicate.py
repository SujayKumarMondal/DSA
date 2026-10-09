def duplicate(arr):
    
    seen = set()
    duplicates = set()
    
    for num in arr:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

arr = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = duplicate(arr)
if res:
    print(f"Duplicate elements in the array are: {res}")