import re

s = input().strip()

if re.match(r'^Hello', s):
    print("Yes")
else:
    print("No")
