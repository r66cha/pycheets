# Быстрая сортировка — это алгоритм, который выбирает опорный элемент, делит массив на элементы меньше и больше него, затем рекурсивно сортирует обе части и объединяет результат в отсортированный массив.

# Пример: [7, 2, 1, 6] → pivot 7 → [2, 1, 6] и [] → pivot 2 → [1] и [6] → результат [1, 2, 6, 7]

# Время: O(n log n) в среднем, O(n²) в худшем
# Память: O(n)


def quick_sort_1(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort_1(left) + middle + quick_sort_1(right)


def quick_sort_2(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    a1 = arr[:mid]
    a2 = arr[mid:]

    if len(a1) > 1:
        a1 = quick_sort_2(a1)

    if len(a2) > 1:
        a2 = quick_sort_2(a2)

    return merge_sort(a1, a2)


def merge_sort(a1, a2):
    c = []

    N = len(a1)
    M = len(a2)

    i = 0
    j = 0

    while i < N and j < M:
        if a1[i] < a2[j]:
            c.append(a1[i])
            i += 1
        else:
            c.append(a2[j])
            j += 1

    c += a1[i:] + a2[j:]
    return c


numbers = [7, 2, 1, 6]
print(quick_sort_1(numbers))
print(quick_sort_2(numbers))
