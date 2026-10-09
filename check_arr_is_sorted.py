def check_sorted(arr):
    l = len(arr)
    for i in range(1, l):
        if(arr[i]<arr[i-1]):
            return False
    return True 

t = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = check_sorted(t)

if res:
    print("The array is sorted in ascending order.")

else:
    print("The array is not sorted in ascending order.")