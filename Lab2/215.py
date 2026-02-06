n = int(input())
count_dict = {}
for _ in range(n):
    name = input()
    count_dict[name] = count_dict.get(name, 0) + 1
print(len(count_dict))