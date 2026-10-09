def ui(arr):
    
    
    seen = []
    duplicates = []
    
    for i in arr:
        if i in seen:
            duplicates.append(i)
        else:
            seen.append(i)
    return seen

op = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = ui(op)
if res:
    print(f"The unique elements in the array are: {res}")