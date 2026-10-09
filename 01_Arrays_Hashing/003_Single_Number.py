from collections import Counter
arr = [1, 2, 3, 4, 5, 1, 2, 3, 4]

def single_no(arr):
    
    count = Counter(arr)
    for num, freq in count.items():
        if freq == 1:
            return num
    return None

res = single_no(arr)
if res:
    print(f"The single number in the array is: {res}")
    
    
#-------------------------------------------------------------#

def single_number(arr):
    
    res = 0
    for i in arr:
        res = res ^ i
    return res

o = single_number(arr)
if o:
    print(f"The single number in the array is: {o}")