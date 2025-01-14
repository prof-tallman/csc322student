
# Error: Incorrect range in the loop, leading to slow code (does not handle negative numbers)
def is_prime_v1(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Error: Incorrect square root calculation, leading to incorrect results
def is_prime_v2(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)):
        if n % i == 0:
            return False
    return True

# Sample Python function to check if a number is prime
def is_prime_v3(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_prime_v3_faster(n):
    if n <= 1 or n % 2 == 0 and n != 2:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Error: Incorrectly returning True for non-prime numbers
def is_prime_v4(n):
    if n <= 1:
        return True
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Error: Incorrect condition, leading to incorrect results for odd numbers
def is_prime_v5(n):
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Error: Incorrect range for even numbers, leading to incorrect results
def is_prime_v6(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True




common_tests = [ { 'type':'typical', 'input':13, 'output':True },
                 { 'type':'typical', 'input':17, 'output':True },
                 { 'type':'typical', 'input':9, 'output':False },
                 { 'type':'typical', 'input':15, 'output':False },
                 { 'type':'typical', 'input':25, 'output':False },
                 { 'type':'typical', 'input':40, 'output':False },
                 { 'type':'typical', 'input':-3, 'output':False },
                 { 'type':'edge', 'input':0, 'output':False },
                 { 'type':'edge', 'input':1, 'output':False },
                 { 'type':'edge', 'input':2, 'output':True },
                 { 'type':'invalid', 'input':"rrrrribit", 'output':False },
                 { 'type':'edge', 'input':2**31-1, 'output':True }, ]

for test in common_tests:
    if is_prime_v1(test['input']) != test['output']:
        print(f'ERROR: V1 input {test['input']} failed the test')






for test in common_tests:
    if is_prime_v2(test['input']) != test['output']:
        print(f'ERROR: V2 input {test['input']} failed the test')

for test in common_tests:
    if is_prime_v3(test['input']) != test['output']:
        print(f'ERROR: V3 input {test['input']} failed the test')

for test in common_tests:
    if is_prime_v4(test['input']) != test['output']:
        print(f'ERROR: V4 input {test['input']} failed the test')

for test in common_tests:
    if is_prime_v5(test['input']) != test['output']:
        print(f'ERROR: V5 input {test['input']} failed the test')

for test in common_tests:
    if is_prime_v6(test['input']) != test['output']:
        print(f'ERROR: V6 input {test['input']} failed the test')
