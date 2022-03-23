
with open("datos.txt", "r") as f:
        data = [line.split() for line in f.read().splitlines()]

r0 = [line[1] for line in data]

print(r0)
