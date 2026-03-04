import re
string = str(input())
if re.match(r'^[a-zA-Z].*\d$',string):
    print("Yes")
else:
    print("No")
