n = input()
arr = list(map(int, input().split()))
print (' '.join(map(str, [x**2 for x in arr])))