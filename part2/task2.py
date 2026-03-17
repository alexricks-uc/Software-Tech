import random
import timeit

large_random_list = [random.randint(1, 1000) for _ in range(5000)]

def merge_sort(array):
    if len(array) <= 1:
        return array
    else:
        left_split = array[:len(array)//2]
        right_split = array[len(array)//2:]
        left = merge_sort(left_split)
        right = merge_sort(right_split)
        return merge(left, right)

def merge(left, right):
    merged = []
    left_pointer = 0
    right_pointer = 0
    merging = True
    while merging:
        left_element = left[left_pointer]
        right_element = right[right_pointer]
        if left_element < right_element:
            merged.append(left_element)
            left_pointer += 1
        elif right_element < left_element:
            merged.append(right_element)
            right_pointer += 1
        elif right_element == left_element:
            merged.append(right_element)
            merged.append(left_element)
            left_pointer += 1
            right_pointer += 1
        if left_pointer >= len(left):
            merged.extend(right[right_pointer:])
            merging = False
        elif right_pointer >= len(right):
            merged.extend(left[left_pointer:])
            merging = False
    return merged

def insertion_sort(arr):
    for i in range(1, len(arr)):
        current_element = arr[i]
        j = i - 1
        while j >= 0 and current_element < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current_element
    return arr

insertion_time = timeit.timeit(lambda: insertion_sort(large_random_list[:]), number=10)
merge_time = timeit.timeit(lambda: merge_sort(large_random_list[:]), number=10)
print("The list is of length",len(large_random_list))
print(f"Insertion Sort took: {insertion_time:.6f} seconds")
print(f"Merge Sort took: {merge_time:.6f} seconds")

'''
For larger sized lists, insertion sort takes substantially longer than merge
sort does. For example, when sorting a list of size 5000, insertion sort takes
around 2.3 seconds, whereas merge sort only takes around 0.04 seconds. When
considering merge sort, we can determine that the number of times the function
is called will be equal to 2^log2(N), which is equal to N (the mathematics here
is complicated, but the answer is essentially that N can be divided in two
log2(N) times, and the list is split 2^log2(N) times as we have double the
number of lists each time we divide, and we divide log2(N) times. Insertion
sort works by traversing the list once, but every element of the list triggers
another traversal. This is equal to N^2, which increases at a faster rate than
N the more that N increases. Therefore, as N grows larger, the complexity of
insertion sort grows much faster than merge sort, making merge sort a much more
efficient function.
'''