import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    words = data[1:1 + n]
    longest = max(words, key=len)
    print(longest)

if __name__ == "__main__":
    main()