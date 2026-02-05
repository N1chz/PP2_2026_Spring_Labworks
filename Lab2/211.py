n, l, r = map(int, input().split())
arr = list(map(int, input().split()))

l -= 1
r -= 1

left = l
right = r

while left < right:

    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1

print(' '.join(map(str, arr)))