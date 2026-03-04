import re
string = str(input())
string_1 = str(input())
if re.search(string_1 , string):
    print("Yes")
else:
    print("No")