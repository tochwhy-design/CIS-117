# This is my first Python programming assignment
# Author: Zhaochun Fu
# Date: 08/30/2026

name = input("What is your name? ")
print("Hello,", name)
my_id = 3489073
print(f"8 digits: {my_id:08d}")
print(f"With two decimals: {my_id:.2f}")
print(f"Binary number {my_id:b}")
print(f"Hzhexadecimal number: {my_id:#x}")
first_number = my_id // 1000000
last_number = my_id % 10
print("Result of adding first + last: ", first_number + last_number)
