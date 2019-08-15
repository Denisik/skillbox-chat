#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Условные и циклические конструкции языка
#
age = int(input("Type your age: "))

if age < 18:
    print("Bye!")
elif age == 18:
    print()
else:
    print("Hello!")

print(age)

step = 1
max_step = 200

while step <= max_step:
    print(step)
    step += 1

