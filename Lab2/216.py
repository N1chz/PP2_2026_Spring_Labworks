n = int(input())
arr = list(map(int, input().split()))

seen = [0] * 1000001

for i in range(n):
    current = arr[i]
    
    if seen[current] == 0:
        print("YES")
        seen[current] = 1
    else:
        print("NO")