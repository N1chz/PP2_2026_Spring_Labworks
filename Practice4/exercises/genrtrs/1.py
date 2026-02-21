n = int(input())
sqrt_gen = (x**2 for x in range(n))
for num in sqrt_gen:
    print(num)