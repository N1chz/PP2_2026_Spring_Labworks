import re
string = str(input())
match = re.search(r'\S+@\S+\.\S+', string)
if match:
    print(match.group())
else:
    print("No email")