 = [1,2,2,3,4,4,5,6,17]
b = [1,2,2,3,4,5,6,6,7]

import collections
print([item for item, count in collections.Counter(a).items()])
print([item for item, count in collections.Counter(b).items()])


seen = set()
uniq_a = [x for x in a if x not in seen and not seen.add(x)]
uniq_b = [x for x in b if x not in seen and not seen.add(x)]

print (uniq_a)
print (uniq_b)



seen = {}
dupes = []

for x in a:
    if x not in seen:
        seen[x] = 1
    else:
        if seen[x] == 1:
            dupes.append(x)
        seen[x] +=1
        
print(seen)
print(dupes)