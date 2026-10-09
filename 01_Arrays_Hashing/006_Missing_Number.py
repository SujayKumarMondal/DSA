"""
Problem 6: Missing Number

Category: 01_Arrays_Hashing

LeetCode / Interview Problem
"""


# ============================================================
# Problem
# ============================================================
def mi(arr):
    
    sum = 0
    l = len(arr) + 1  # for the missing number, we add 1 to the length of the array
    
    ex_sum = (l*(l+1))/2
    
    for i in arr:
        sum = sum + i
    return int(ex_sum - sum)

    

f = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = mi(f)
if res:
    print(f"The missing number in the array is: {res}")
# Missing Number


# ============================================================
# Approach
# ============================================================

# TODO:
# Explain your approach here.


# ============================================================
# Solution
# ============================================================

def solution():
    pass


# ============================================================
# Complexity
# ============================================================

# Time Complexity:
# Space Complexity:


# ============================================================
# Test Cases
# ============================================================

if __name__ == "__main__":
    # Add your test cases here
    pass
