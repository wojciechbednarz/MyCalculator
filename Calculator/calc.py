from functools import reduce
import re

# def evaluate_data(expression):
#     first_number = 0
#     second_number = 0
#     numbers_list = []
#     operators_list = []
#     number_or_symbol = re.compile(r'(\d+|[^ 0-9])')
#     list_of_values = re.findall(number_or_symbol, expression)
#     for value in list_of_values:
#         if value.isdigit():
#             numbers_list.append(value)
#         else:
#             operators_list.append(value)
#     if operators_list[0] == '+':
#         pass

class Calculations:
    def __init__(self):
        self.sum = 0
        self.list_of_num = []

    def append_values_to_list(self, *args):
        [self.list_of_num.append(value) for value in args]

    def add(self, *args):
        for value in args:
            self.sum += value
        return self.sum

    def subtract(self, values):
        first_val = int(values[0])
        second_val = int(values[1])
        subtraction = first_val - second_val
        return subtraction

    def multiplication(self, *args):
        self.append_values_to_list(*args)
        return reduce(lambda x, y: x * y, self.list_of_num)

    def division(self, *args):
        self.append_values_to_list(*args)
        return reduce(lambda x, y: x / y if (y != 0) else "None", self.list_of_num)

    def power(self, number, exp):
        value = 1
        for _ in range(exp):
            value *= number
        return number
