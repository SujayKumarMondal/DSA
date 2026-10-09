def find_all_numbers_disappeared_in_an_array(arr):
    u = len(arr)
    h = set(arr)
    m = []
    for i in range(1, u+1):
        if i not in h:
            m.append(i)
    return m    


xy = list(map(int, input("Enter the array elements separated by spaces: ").split()))
result = find_all_numbers_disappeared_in_an_array(xy)
if result:
    print(f"The numbers that disappeared in the array are: {result}")
        