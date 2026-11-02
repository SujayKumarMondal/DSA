def long_consec_seq(arr):
    
    s = set(arr)
    
    longest = 0
    
    for i in arr:
        j = 1
        
        if i-1 not in s:
            while i+j in s:
                j += 1
            longest = max(longest, j)
    return longest