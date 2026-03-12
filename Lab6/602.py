n = int(input())
arr = list(map(int, input().split()))
cnt = 0
for i in range(n):
    if arr[i] % 2 == 0:
        cnt += 1
print(cnt, end=" ")