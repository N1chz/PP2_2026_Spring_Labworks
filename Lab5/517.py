import re
a = len(re.findall(r'\d{2}/\d{2}/\d{4}',input()))
if a >= 0:
    print(a)
else:
    print("No dates")