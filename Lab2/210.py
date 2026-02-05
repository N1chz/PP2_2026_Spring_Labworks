n = input()
arr = list(map(int, input().split()))
sorted_arr = sorted(arr)
reversed_arr = sorted_arr[::-1]
print(' '.join(map(str, reversed_arr)))