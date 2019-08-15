#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Работа с функциями, аргументы и возвращаемое значение
#
# def my_print(message: str):
#     print("My print: " + message)
# my_print("some 1")
# my_print("some 2")
#
# def show_counter(step, max_step):
#     while step <= max_step:
#         print(step)
#         step += 1
#
#
#
# show_counter(5, 15)


def sum_of_two_numbers(a, b):
    print(a + b)
    return a + b

answer = sum_of_two_numbers(20, 20)
print(answer)