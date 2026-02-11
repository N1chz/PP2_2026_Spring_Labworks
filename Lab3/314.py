def main():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    q = int(input().strip())

    for _ in range(q):
        operation = input().strip().split()
        if operation[0] == "add":
            x = int(operation[1])
            arr = list(map(lambda a: a + x, arr))
        elif operation[0] == "multiply":
            x = int(operation[1])
            arr = list(map(lambda a: a * x, arr))
        elif operation[0] == "power":
            x = int(operation[1])
            arr = list(map(lambda a: a ** x, arr))
        elif operation[0] == "abs":
            arr = list(map(lambda a: abs(a), arr))

    print(' '.join(map(str, arr)))

if __name__ == "__main__":
    main()