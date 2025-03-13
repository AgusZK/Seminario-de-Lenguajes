#1
num = int (input('ingresa edad'))
#print(100-num)

#2
grados = int(input("Ingrese una temperatura en celcius: "))
#print((grados * 9/5 )+ 32)

#3
num = 0
for i in range(101):
    num = num + i
print (num)

#4
v = [1,2,3,4,5,6,7,8,9,10]
for i in range (10):
    if (v[i] % 2 == 0):
        print(v[i])

#5
v = [0]*10
for i in range(10):
    n = int(input())
    v[i] = n 
for i in range (10):
   if (v[i] > 0):
        print(v[i])
   else:
       break
       
#6
v = [1,2,3,4,5,6,7,8,9,10]
p = []
imp = []
for i in range (10):
    if (v[i] % 2 == 0):
        p.append(v[i])
    else:
        imp.append(v[i])


for i in range (len(p)):
   print (p[i])

for i in range(len(imp)):
    print(imp[i])

#7
l = []
cadena = ""
for i in range (10):
    num = int(input())
    l.append(num)
for i in range (10):
    if (l[i] % 3 != 0):
        cadena = cadena + "-" + str(l[i]) 
print(cadena) 