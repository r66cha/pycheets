# Сортировка выбором — это алгоритм, который на каждой итерации ищет минимальный элемент в неотсортированной части массива и меняет его местами с первым элементом этой части, постепенно увеличивая отсортированную область слева.

# Пример: [5, 3, 6, 2, 10] → найти минимум 2 → [2, 3, 6, 5, 10] → найти минимум 3 → [2, 3, 6, 5, 10] → найти минимум 5 → [2, 3, 5, 6, 10]

# Время: O(n²)
# Память: O(1)


def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


numbers = [5, 3, 6, 2, 10]
sorted_numbers = selection_sort(numbers)
print(numbers)
