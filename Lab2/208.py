n = int(input())
b = 1
if n == 1:
        print("1", end=" ")
else:
        print(b, end=" ")
        for i in range(n):
            b *= 2
            print(b, end=" ")
            if b * 2 > n:
                break
            else:
                continue
