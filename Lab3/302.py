def isUsual(num: int) -> bool:
    for divisor in (2, 3, 5):
        while num % divisor == 0:
            num //= divisor
    return num == 1

def main():
    n = int(input().strip())
    if isUsual(n):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()