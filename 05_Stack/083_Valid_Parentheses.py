def valid_parentheses(s: str) -> bool:
    stack = []
    
    for ch in s:
        if ch in '({[':
            stack.append(ch)
        elif ch == ')':
            if len(stack) != 0 and stack[-1] == '(':
                stack.pop()
            else:
                return False
        elif ch == '}':
            if len(stack) != 0 and stack[-1] == '{':
                stack.pop()
            else:
                return False
        elif ch == ']':
            if len(stack) != 0 and stack[-1] == '[':
                stack.pop()
            else:
                return False
            
    return len(stack) == 0

r = input("Enter the string of parentheses: ")
if valid_parentheses(r):
    print("The parentheses are valid.")
else:
    print("The parentheses are not valid.")