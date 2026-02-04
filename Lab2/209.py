n = int(input())
arr = list(map(int, input().split()))
max = arr[0]
for i in range(n):
    if arr[i] > max:
        max = arr[i]
min = arr[0]
for i in range(n):
    if arr[i] < min:
        min = arr[i]
for i in range(n):
    max = min
    print(arr)