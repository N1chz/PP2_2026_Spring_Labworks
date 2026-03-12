import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    B = list(map(int, data[1 + n:1 + 2 * n]))
    dot = sum(a * b for a, b in zip(A, B))
    print(dot)

if __name__ == "__main__":
    main()