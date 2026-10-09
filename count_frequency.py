def freq(arr):
    
    fr = {}
    
    for i in arr:
        if i in fr:
            fr[i] = fr[i] + 1
        else:
            fr[i] = 1
    return fr

f = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = freq(f)
if res:
    print("The frequency of each element in the array is:")
    for value, key in res.items():
        print(f"{value}: {key}")