import random

m = open("Data.txt","w")

for x in range(0,1000):
    for y in range(0,1000):
        rand = random.randint(1,3)
        m.write(str(rand))
    m.write("\n")

m.close()
