n = int(input())

document = {}

for _ in range(n):
    command_line = input().strip().split()
    command_type = command_line[0]
    
    if command_type == "set":
        key = command_line[1]
        value = command_line[2]
        document[key] = value 
        
    elif command_type == "get":
        key = command_line[1]
        if key in document:
            print(document[key])
        else:
            print(f"KE: no key {key} found in the document")