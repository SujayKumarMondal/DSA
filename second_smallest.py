from math import inf


def sec_sm(arr):
    
    s = float(inf)
    ss = float(inf)
    
    for i in arr:
        if i<s:
            ss=s
            s=i
        elif s<i<ss:
            ss=i
            
    return ss

w = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = sec_sm(w)
if res:
    print(f"The second smallest element in the array is: {res}")