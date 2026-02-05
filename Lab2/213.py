x = int(input())

if x < 2:
    print("No")
else:
    if x == 2:
        print("Yes")
    elif x % 2 == 0:
        print("No")
    else:
        is_prime = True
        divisor = 3
        
        while divisor * divisor <= x:
            if x % divisor == 0:
                is_prime = False
                break
            divisor += 2
        
        if is_prime:
            print("Yes")
        else:
            print("No")