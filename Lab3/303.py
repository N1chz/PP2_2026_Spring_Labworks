import re

def solve():
    to_digit = {
        "ZER": 0, "ONE": 1, "TWO": 2, "THR": 3, "FOU": 4,
        "FIV": 5, "SIX": 6, "SEV": 7, "EIG": 8, "NIN": 9
    }
    from_digit = {v: k for k, v in to_digit.items()}

    s = input().strip()
    tokens = re.split(r'([+\-*])', s)

    def number_value(token):
        value = 0
        for i in range(0, len(token), 3):
            triplet = token[i:i+3]
            value = value * 10 + to_digit[triplet]
        return value

    result = number_value(tokens[0])
    for i in range(1, len(tokens), 2):
        op = tokens[i]
        nxt = number_value(tokens[i+1])
        if op == '+':
            result += nxt
        elif op == '-':
            result -= nxt
        elif op == '*':
            result *= nxt

    result_str = str(result)
    output = []
    for ch in result_str:
        output.append(from_digit[int(ch)])
    print(''.join(output))

if __name__ == '__main__':
    solve()