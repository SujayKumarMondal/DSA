def subarrays(arr):
    n = len(arr)

    for st in range(n):
        for end in range(st, n):
            for i in range(st, end + 1):
                print(arr[i], end=" ")
            print("    ", end="")
        print()

a = list(map(int, input("Enter the elements separated by space: ").split()))

subarrays(a)




def max_subarray(arr):
    n = len(arr)
    max_sum = float('-inf')
    current_sum = 0
    st = 0
    end = 0

    for st in range(n):
        current_sum = 0
        for end in range(st, n):
            current_sum += arr[end]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum

a = list(map(int, input("Enter the elements of the array separated by space: ").split()))
print("Maximum subarray sum:", max_subarray(a))