n = int(input())

dorama_dict = {}

for _ in range(n):
    line = input().split()
    name = line[0]  
    episodes = int(line[1]) 
    
    if name in dorama_dict:
        dorama_dict[name] += episodes
    else:
        dorama_dict[name] = episodes

sorted_doramas = sorted(dorama_dict.keys())

for name in sorted_doramas:
    print(name, dorama_dict[name])