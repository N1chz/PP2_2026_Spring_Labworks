import re
match = re.search(r'Name:\s+(.*?),\s+Age:\s+(\d+)',input())
if match:
    name = match.group(1)
    age = match.group(2)
    print(f"{name} {age}")