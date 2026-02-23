def sqrt_generator(n):
    for i in range(1, n + 1):
        yield i * i

def main():
    n = int(input().strip())
    for sq in sqrt_generator(n):
        print(sq)

if __name__ == "__main__":
    main()