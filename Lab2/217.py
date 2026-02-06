n = int(input())

numbers = []
for _ in range(n):
    number = input()
    numbers.append(number)

processed = [False] * n
count_exactly_three = 0

for i in range(n):
    if processed[i]:
        continue
    
    current_number = numbers[i]
    count = 0
    
    for j in range(i, n):
        if numbers[j] == current_number:
            count += 1
            processed[j] = True
    
    if count == 3:
        count_exactly_three += 1

print(count_exactly_three)