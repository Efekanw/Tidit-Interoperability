f = open("onto_new.txt",mode="r")
f1 = open("power.jsonld", mode="w+")
lines = f.readlines()
output = ""
[f1.write(line) for line in lines if not line.startswith("\n")]