import re
string = str(input())
string_1 = str(input())
a = re.findall(string_1, string)
print(len(a))