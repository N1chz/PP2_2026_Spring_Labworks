n = int(input())

numbers = list(map(int, input().split()))

most_frequent = numbers[0]
max_count = 0

for i in range(n):
    current = numbers[i]
    count = 0
    
    for j in range(n):
        if numbers[j] == current:
            count += 1
    
    if count > max_count:
        max_count = count
        most_frequent = current

    elif count == max_count and current < most_frequent:
        most_frequent = current

print(most_frequent)