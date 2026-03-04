import re
string = str(input())
digits = re.findall(r'\d',string)
print(" ".join(digits))
