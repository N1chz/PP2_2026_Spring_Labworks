def gene_3_4(n):
    for i in range (n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
num = gene_3_4(n)
first = True 
for num in gene_3_4(n):
    if first:
        print(num, end='')
        first = False
    else:
        print('', num, end='')
print()