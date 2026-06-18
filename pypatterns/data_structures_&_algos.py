data = (1, 2, 3, 4)
_, second, third, _ = data
print(second, third)  # 2 3

first, *other = data
print(first)  # 1
print(other)  # [2, 3, 4] - список! даже если data был кортежем
