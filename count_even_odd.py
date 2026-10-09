def ev_od(arrr):
    
    od = 0
    ev = 0
    
    for i in arrr:
        if i%2 == 0:
            ev = ev+1
        else:
            od = od+1
    return ev, od

j = list(map(int, input("Enter the array elements separated by spaces: ").split()))
res = ev_od(j)
if res:
    print(f"The number of even elements in the array is: {res[0]}")
    print(f"The number of odd elements in the array is: {res[1]}")