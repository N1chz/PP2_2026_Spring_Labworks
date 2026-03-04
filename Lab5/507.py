import re

def main():
    S = input()
    P = input()
    R = input()
    result = re.sub(re.escape(P), R, S)
    print(result)

if __name__ == "__main__":
    main()