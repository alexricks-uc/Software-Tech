import random
import timeit

def iterative_sum(n):
    total = 0
    for i in range(n+1):
        total += i
    return total

def iterative_fib(n):
    if n == 0:
        return 0
    else:
        x = 0
        y = 1
        for i in range(1,n+1):
            z = (x + y)
            x = y
            y = z
        return y

def iterative_fact(n):
    final = 1
    for i in range(2,n+1):
        final *= i
    return final

def recursive_sum(n):
    if n == 1:
        return 1
    else:
        return n + recursive_sum(n - 1)

def recursive_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)

def recursive_factorial(n):
    if n == 0:
        return 1
    else:
        return n * recursive_factorial(n - 1)

it_sum_time = timeit.timeit(lambda: iterative_sum(30), number=10)
it_fib_time = timeit.timeit(lambda: iterative_fib(30), number=10)
it_fact_time = timeit.timeit(lambda: iterative_fact(30), number=10)
rec_sum_time = timeit.timeit(lambda: recursive_sum(30), number=10)
rec_fib_time = timeit.timeit(lambda: recursive_fibonacci(30), number=10)
rec_fact_time = timeit.timeit(lambda: recursive_factorial(30), number=10)

print(f'Iterative sum took: {it_sum_time:.6f} seconds, '
      f'while recursive sum took: {rec_sum_time:.6f}.')
print(f'Iterative fibonacci took: {it_fib_time:.6f} seconds, '
      f'while recursive fibonacci took: {rec_fib_time:.6f}.')
print(f'Iterative factorial took: {it_fact_time:.6f} seconds, '
      f'while recursive factorial took: {rec_fact_time:.6f}.')

'''
At large quantities, the recursive fibonacci is substantially slower than
the iterative fibonacci, meanwhile the other functions are of comparative
speed at all sizes. This is because the fibonacci recursive function refers to
itself twice; that is, for every time we call the recursive fibonacci
function, it calls itself twice more. Once we want to calculate larger
fibonacci numbers, we have called it once, then twice, then four times, then
16 times and so on. This means the function has complexity O(2^n), meanwhile
the iterative function has complexity O(N). Iterative functions are preferred
therefore for fibonacci calculations, or any function in which recursion would
require multiple recursive calls in the same function.
'''