def cntdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input())
for num in cntdown(n):
    print(num)