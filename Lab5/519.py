import re
pat = re.compile(r'\b\w+\b')
match = pat.findall(input())
print(len(match))