z=[]
c=0
for i in range(400):
    for j in range(10):
        c+=int(input())
    z.append(c)
    c=0
for i in z:
    print(i)