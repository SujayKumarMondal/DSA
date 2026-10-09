from collections import Counter

def major_element(arr):
    l = len(arr)
    c = Counter(arr)
    
    for m, n in c.items():
        if n > l//2:
            return m
    return None

g = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = major_element(g)
if res is not None:
    print(f"The majority element in the array is: {res}")
else:
    print("No majority element found.")