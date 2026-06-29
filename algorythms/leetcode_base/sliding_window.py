"""Скользящее окно (Sliding Window)
Фреймворк для решения задач, которые требуют поиска подстрок или подмассивов в массиве или строке
"""


# Окно фиксированного размера
# Время: O(n)
# Память: O(1)
def k_elements_max_sum(nums: list[int], k: int) -> int:
    """Возвращает максимальную сумму k подряд идущих элементов в списке"""

    # Накопление
    window_sum = 0
    for i in range(k):
        window_sum += nums[i]

    max_sum = window_sum

    # Цикл
    for r in range(k, len(nums)):
        # Переход к следующему окну
        l = r - k
        window_sum = window_sum + nums[r] - nums[l]
        max_sum = max(max_sum, window_sum)

    return max_sum


nums_1 = [3, 2, 0, 9, 1, 2, 8, 5, 2]
k_1 = 5
print(k_elements_max_sum(nums_1, k_1))  # 25

# Green flags:
# * Дана переменная обозначающая размер окна
# * Требуется работать с подряд идущими элементами

# --


# Непересекающиеся окна
# Время: O(n)
# Память: O(n)
def compress_ranges(nums: list[int]) -> list[str]:
    """Возвращает список диапазонов последовательно идущих цифр"""

    # Инициализация
    l = 0
    r = 0
    result = []

    # Внешний цикл
    while l < len(nums):

        # Расширение
        while r + 1 < len(nums) and nums[r] + 1 == nums[r + 1]:
            r += 1

        # Обработка
        if l != r:
            result.append(f"{nums[l]}->{nums[r]}")
        else:
            result.append(f"{nums[l]}")

        # Переход к следующему
        l = r + 1
        r = r + 1

    return result


nums_2 = [1, 2, 3, 5, 8, 9, 14]
print(compress_ranges(nums_2))  # ['1->3', '5', '8->9', '14']

# Green flags:
# * Нужно работать с подряд идущими непересекающимися группами элементов

# --


# Пересекающиеся окна
# Время: O(n)
# Память: O(1)
def longest_ones_with_flips(nums: list[int], k: int) -> int:
    """Возвращает наибольшую последовательность единиц где k это количество раз смены 0 на 1"""

    # Инициализация
    l = 0
    r = -1
    result = 0

    # Cостояние окна
    zeros_count = 0

    # Внешний цикл
    while l < len(nums):

        # Расширение
        while r + 1 < len(nums) and (nums[r + 1] == 1 or zeros_count < k):
            if nums[r + 1] == 0:
                zeros_count += 1
            r += 1

        # Обработка
        result = max(result, r - l + 1)

        # Сужение
        if nums[l] == 0:
            zeros_count -= 1
        l += 1

    return result


nums_3 = [1, 0, 1, 0, 1, 0, 1, 1]
k_3 = 2
print(longest_ones_with_flips(nums_3, k_3))  # 6

# Green flags:
# * Нужно найти самую длинную последовательность с определенными свойствами

# ---


from collections import Counter

w = "aaabccccde"

c = Counter(w)
print(c)
max_c = max(c.keys(), key=lambda k: c[k])
print(max_c * c[max_c])
