import re
s = input()
p = input()
c = re.escape(p)
match = re.findall(c,s)
print(len(match))