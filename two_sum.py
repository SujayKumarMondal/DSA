#Optimized Approach

def two_sum(arr, tar):

    xyz = {}
    
    for i, num in enumerate(arr):
        dif = tar - num
        if dif in xyz:
            return [xyz[dif], i]
        xyz[num] = i
    return []  

pqr = int(input("Enter the target value: "))
arr = list(map(int, input("Enter the array elements separated by spaces: ").split()))

res = two_sum(arr, pqr)
if res:
    print(f"Indices of the two numbers that add up to {pqr} are: {res}")
else:
    print(f"No two numbers add up to {pqr}.")
    
    
    
#---------------------------------------------------------------------------------------#


#Brute Force Approach

def two_sum(arr, tar):
    
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == tar:
                return [i, j] 
            
    return []

ab = int(input("Enter the target value: "))
arr = list(map(int, input("Enter the array elements separated by spaces: ").split()))

res = two_sum(arr, ab)
if res:
    print(f"Indices of the two numbers that add up to {ab} are: {res}")
else:
    print(f"No two numbers add up to {ab}.")