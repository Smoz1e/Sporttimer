n=int(input())
if n<10:
    print(n)
else:
    a=str(n)
    s=[a[0],a[1]]
    q=1
    for i in range(len(a)):
        if a[i] not in s:
            q=0
    if q==1:
        print(n)
    while q==0:
        a=str(n+1)
        b=str(n-1)
        p=0
        l=0
        for i in range(len(a)):
            if p==0 and a[i] not in s:
                p=1
            if l==0 and i<len(b) and b[i] not in s:
                l=1
        if p==0:
            q=1
            print(a)
            break
        elif l==0:
            q=1
            print(b)
            break
