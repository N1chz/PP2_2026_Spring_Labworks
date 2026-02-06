n = int(input())
arr = [input() for _ in range(n)]

first_occurrence = {}
for i in range(n):
    if arr[i] not in first_occurrence:
        first_occurrence[arr[i]] = i + 1

for key in sorted(first_occurrence.keys()):
    print(key, first_occurrence[key])