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

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        current_element = arr[i]
        j = i - 1
        while j >= 0 and current_element < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current_element
    return arr

def linsert(array, target):
    return linear_search(insertion_sort(array), target)

def binsert(array, target):
    return binary_search(insertion_sort(array), target)

def libble(array, target):
    return linear_search(bubble_sort(array), target)

def bibble(array, target):
    return binary_search(bubble_sort(array), target)

unsorted_list = [random.randint(1, 1000) for _ in range(10000)]
target = random.randint(0, 999999)
libble_time = timeit.timeit(lambda: libble(unsorted_list.copy(), target), number=1)
bibble_time = timeit.timeit(lambda: bibble(unsorted_list.copy(), target), number=1)
linsert_time = timeit.timeit(lambda: linsert(unsorted_list.copy(), target), number=1)
binsert_time = timeit.timeit(lambda: binsert(unsorted_list.copy(), target), number=1)
linear_time = timeit.timeit(lambda: linear_search(unsorted_list.copy(),target), number=1)
# print(f"Linear Insertion Sort Execution Time: {linsert_time:.6f} seconds")
# print(f"Linear Bubble Sort Execution Time: {libble_time:.6f} seconds")
print(f"Binary Insertion Sort Execution Time: {binsert_time:.6f} seconds")
print(f"Binary Bubble Sort Execution Time: {bibble_time:.6f} seconds")
print(f"Linear Search Execution Time: {linear_time:.6f} seconds")