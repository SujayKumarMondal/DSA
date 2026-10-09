from math import inf


def se_lar(arr):
    lar = float(-inf)
    slar = float(-inf)
    
    for i in arr:
        if i>lar:
            slar = lar
            lar = i
        elif lar>i>slar:
            slar = i
    return slar

c = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = se_lar(c)
if res:
    print(f"The second largest element in the array is: {res}")