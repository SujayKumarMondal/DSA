"""
Problem: Binary Search Iterative
Topic: Searching

Approach:

Time Complexity: O(log n) // The search space is halved in each iteration. n/2^k = 1, n/2^k = 1 => k = log n    
Space Complexity: O(1) // Only a constant amount of extra space is used. No recursion or additional data structures are used.

Notes:
"""


def binary_search(arr, target):
    l = len(arr)
    
    if arr is not sorted:
        arr.sort()  # Sort the array if it's not sorted
    
    low = 0
    high = l-1
    
    while low <= high:
        mid = (low + high) //2 
        
        if arr[mid] == target:
            return mid
        
        elif arr[mid] < target:
            low = mid + 1
            
        else:
            high = mid -1
            
    return -1


u = list(map(int, input("Enter sorted array elements separated by spaces: ").split()))
v = int(input("Enter the target element to search: "))

res = binary_search(u, v)
if res != -1:
    print(f"Element found at index: {res}")
