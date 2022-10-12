import os

with open("data/cricket/rand_pol.txt",'r') as ogp:
    with open("new_rand_pol.txt", 'a') as newp:
        oglines = ogp.readlines()
        for line in oglines:
            newp.write(line.strip()[-1])
            newp.write("\n")

