def even_num(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input())
evens = list(even_numbers(n))
print(", ".join(map(str, evens)))