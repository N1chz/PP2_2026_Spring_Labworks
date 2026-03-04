import re;
if re.compile(r'\d+$').match(input()):
    print("Match")
else:
    print("No match")