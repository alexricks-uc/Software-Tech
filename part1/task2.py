import random
import timeit


def linear_search(array, target):
    for i in range(len(array)):
        if array[i] == target:
            return i
    return -1

def binary_search(array, target):
    left = 0
    right = len(
        array) - 1
    mid = int((left + right) / 2)
    while left <= right:
        if array[mid] == target:
            return mid
        elif target > array[mid]:
            left = mid + 1
        elif target < array[mid]:
            right = mid - 1
        mid = int((left + right) / 2)
    return -1

sorted_list = list(range(1000000))
target = random.randint(0, 999999)
linear_time = timeit.timeit(lambda: linear_search(sorted_list, target), number=100)
binary_time = timeit.timeit(lambda: binary_search(sorted_list, target), number=100)
print(f"Linear search execution time: {linear_time:.6f} seconds")
print(f"Binary search execution time: {binary_time:.6f} seconds")