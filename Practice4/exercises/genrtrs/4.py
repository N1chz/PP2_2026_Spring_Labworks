def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

a, b = 3, 7
for val in squares(a, b):
    print(val)