def sqrt_gene(N):
    for i in range(N + 1):
        yield i ** 2

N = 10
for num in sqrt_gene(N):
    print(num)