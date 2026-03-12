import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    numbers = list(map(int, data[1:1 + n]))
    distinct = sorted(set(numbers))
    print(' '.join(map(str, distinct)))

if __name__ == "__main__":
    main()