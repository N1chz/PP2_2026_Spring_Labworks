import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    words = data[1:1 + n]
    result = [f"{i}:{word}" for i, word in enumerate(words)]
    print(' '.join(result))

if __name__ == "__main__":
    main()