import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    numbers = list(map(int, data[1:1 + n]))
    if all(x >= 0 for x in numbers):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()