def sum_arr(arr):
    sum = 0
    avg = 0
    for i in arr:
        sum = sum + i
        avg = sum / len(arr)
    return sum, avg


d = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = sum_arr(d)

if res:
    print(f"The sum of the array elements is: {res[0]}")
    print(f"The average of the array elements is: {res[1]}")