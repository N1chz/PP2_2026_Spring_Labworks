thisset = {"apple", "banana", "cherry"}
print(thisset) 
thisset = {"apple", "banana", "cherry", "apple"}

print(thisset)

thisset = {"apple", "banana", "cherry", True, 1, 2}

print(thisset)
thisset = {"apple", "banana", "cherry", False, True, 0}

print(thisset)
thisset = {"apple", "banana", "cherry"}

print(len(thisset)) 
set1 = {"apple", "banana", "cherry"}
set2 = {1, 5, 7, 9, 3}
set3 = {True, False, False} 
set1 = {"abc", 34, True, 40, "male"} 
myset = {"apple", "banana", "cherry"}
print(type(myset))
thisset = set(("apple", "banana", "cherry")) # note the double round-brackets
print(thisset) 
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x) 
  thisset = {"apple", "banana", "cherry"}

print("banana" in thisset) 
thisset = {"apple", "banana", "cherry"}

print("banana" not in thisset) 
thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset) 
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset) 
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]

thisset.update(mylist)

print(thisset)

thisset = {"apple", "banana", "cherry"}

thisset.remove("banana")

print(thisset) 
thisset = {"apple", "banana", "cherry"}

thisset.discard("banana")

print(thisset) 
thisset = {"apple", "banana", "cherry"}

x = thisset.pop()

print(x)

print(thisset) 
thisset = {"apple", "banana", "cherry"}

x = thisset.pop()

print(x)

print(thisset) thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x) 
   set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3) 
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1 | set2
print(set3)

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}

myset = set1.union(set2, set3, set4)
print(myset) 
