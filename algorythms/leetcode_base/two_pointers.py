"""Два указателя (Two Pointers)
Фреймворк, в котором два указателя перемещаются по одной или нескольким последовательностям по заданным правилам, позволяя решать задачи эффективнее, чем полный перебор.
"""


# С двух сторон
# Время: O(n)
# Память: O(1)
def two_sum(nums: list[int], target: int) -> list[int]:
    """Возвращает индексы элементов, которые в сумме дают target"""

    # Инициализация
    l = 0
    r = len(nums) - 1

    # Цикл
    while l < r:

        # Логика движения указателей

        current_sum = nums[l] + nums[r]

        if current_sum == target:
            return [l, r]
        elif current_sum > target:
            r -= 1
        else:
            l += 1

    return [-1, -1]


nums_1 = [-2, 1, 6, 9, 12, 21]
target = 18
print(two_sum(nums_1, target))


# Green flags:
# * Дан отсортированный массив
# * Задача на палиндром (Возможны усложнения)
# * Решение формируется за счет сужения области с двух сторон

# --


# Каждому по указателю
# Время: O(n + m)
# Память: O(min(n,m))
def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """Возвращает общие элементы из двух списков"""

    # Инициализация
    p1 = 0
    p2 = 0
    result = []

    # Цикл
    while p1 < len(nums1) and p2 < len(nums2):

        # Логика движения указателей

        if nums1[p1] == nums2[p2]:
            result.append(nums1[p1])
            p1 += 1
            p2 += 1
        elif nums1[p1] < nums2[p2]:
            p1 += 1
        else:
            p2 += 1

    return result


nums_first = [0, 2, 4, 8, 8]
nums_second = [1, 2, 2, 7, 8, 8, 8]

# Green flags:
# * Даны несколько массивов или строк (!)
# * Нужно искать объединения/пересечения

# -


# ** Доп Задача
# Сортировка 2х отсортированных массивов
def two_sorted_to_one(nums1: list[int], nums2: list[int]) -> list[int]:
    """Вернет общий отсортированный массив"""

    p1 = 0
    p2 = 0
    result = []

    while nums1[p1] < len(nums1) and nums2[p2] < len(nums2):

        if nums1[p1] < nums2[p2]:
            result.append(nums1[p1])
            p1 += 1
        elif nums1[p1] > nums2[p2]:
            result.append(nums2[p2])
            p2 += 1
        else:
            result.append(nums1[p1])
            result.append(nums2[p2])

    result += nums1[p1:] + nums2[p2:]

    return result


nums_2_first = [1, 3, 5, 7, 9]
nums_2_second = [2, 4, 6, 8]
print(two_sorted_to_one(nums_2_first, nums_2_second))

# --


# Быстрый и медленный
# Время: O(n)
# Память: O(1)
def move_zeros(nums: list[int]) -> list[int]:
    """Возвращает список с 0 в конце"""

    # Инициализация
    slow = 0  # Куда пишем (Всегда стоит на 0)
    fast = 0  # Откуда читаем (ищейка - двигается всегда)

    # Цикл
    while fast < len(nums):

        # Логика движения

        if nums[fast] != 0:
            if fast != slow:
                nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
        fast += 1

    return nums


nums_3 = [12, 13, 0, 1, 3, 0, 0, 0, 4]
nums_4 = [1, 2, 0, 0, 3, 4, 0, 0, 7]
nums_5 = [0, 1, 0, 3, 12]
print(move_zeros(nums_5))

# Green flags:
# * Нужна инплейс модификация исходного массива (!)
# * Нужно сохранить исходный порядок

# --


def isPalindrome(s: str) -> bool:
    new_s = "".join([c for c in s.lower() if c.isalpha() or c.isdigit()]).replace(
        " ", ""
    )
    l = 0
    r = len(new_s) - 1

    while l != r:
        if new_s[l] != new_s[r]:
            return False
        l += 1
        r -= 1

    return True


s = "race a car"
s2 = "0P"
new_s2 = new_s = "".join([c for c in s2.lower() if c.isalpha()]).replace(" ", "")
print(new_s2)
print(isPalindrome(s))
