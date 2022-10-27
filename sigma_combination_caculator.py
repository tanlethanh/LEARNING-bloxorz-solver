import math


def combination(k, n):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def func(number_of_color, number_of_slots):
    facto = 1
    for idx in range(0, number_of_color):
        facto *= combination(4, number_of_slots - 4 * idx)
    return facto
