import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def main():
    numbers = list(map(int, input().split()))
    primes = list(filter(lambda x: is_prime(x), numbers))
    if primes:
        print(' '.join(map(str, primes)))
    else:
        print("No primes")

if __name__ == "__main__":
    main()