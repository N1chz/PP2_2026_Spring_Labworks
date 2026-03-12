import sys

def main():
    tokens = sys.stdin.read().strip().split()
    if not tokens:
        return
    n = int(tokens[0])
    keys = tokens[1:1 + n]
    values = tokens[1 + n:1 + 2 * n]
    query = tokens[1 + 2 * n] if len(tokens) > 1 + 2 * n else ''
    mapping = dict(zip(keys, values))
    print(mapping.get(query, "Not found"))

if __name__ == "__main__":
    main()