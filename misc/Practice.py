#Write a program to find the sum of digits of a number.
def sum_of_digits(number):
    total = 0
    while number > 0:
        digit = number % 10
        total += digit
        number //= 10
    return total
# Example usage
num = 12345
result = sum_of_digits(num)
print(f"The sum of digits of {num} is {result}")
