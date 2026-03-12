import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    numbers = list(map(int, data[1:1 + n]))
    count = sum(map(bool, numbers))
    print(count)

if __name__ == "__main__":
    main()