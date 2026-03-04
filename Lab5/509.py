import re
result = re.findall(r'\b\w{3}\b', input())
print(len(result))
