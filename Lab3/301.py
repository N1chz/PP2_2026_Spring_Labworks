def is_valid(number: int) -> bool:
    """Return True if all digits of number are even."""
    return all(int(digit) % 2 == 0 for digit in str(number))

def main():
    n = int(input().strip())
    if is_valid(n):
        print("Valid")
    else:
        print("Not valid")

if __name__ == "__main__":
    main()