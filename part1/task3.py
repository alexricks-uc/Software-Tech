import random
import timeit


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

unsorted_list = [random.randint(1, 1000) for _ in range(10000)]
bubble_sort_time = timeit.timeit(lambda: bubble_sort(unsorted_list.copy()), number=1)
insertion_sort_time = timeit.timeit(lambda: insertion_sort(unsorted_list.copy()), number=1)
print(f"Bubble Sort Execution Time: {bubble_sort_time:.6f} seconds")
print(f"Insertion Sort Execution Time: {insertion_sort_time:.6f} seconds")