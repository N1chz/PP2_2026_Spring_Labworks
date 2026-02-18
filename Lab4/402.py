def even_numbers(limit):
    for i in range(0, limit + 1, 2):
        yield i

def main():
    n = int(input())
    gen = even_numbers(n)
    try:
        first = next(gen)
        print(first, end='')
        for num in gen:
            print(f',{num}', end='')
    except StopIteration:
        pass
    print() 

if __name__ == '__main__':
    main()