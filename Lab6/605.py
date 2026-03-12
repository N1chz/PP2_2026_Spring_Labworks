import re

s = input()

if re.search(r"[aeiouAEIOU]", s):
    print("Yes")
else:
    print("No")