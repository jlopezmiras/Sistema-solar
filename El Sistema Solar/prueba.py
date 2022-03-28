from ast import Constant
import math
import numpy as np


# Constantes físicas
c = 1.496e11 # distancia Tierra-Sol (m)
G = 6.67e-11 # constante de gravedad (Nm²/kg²)
Ms = 1.99e30  # masa del Sol (kg)


def reescalamiento(m,t,r,v):

    m = m/Ms
    t = math.sqrt(G*Ms/c**3)*t
    r = r/c
    v = math.sqrt(c/(G*Ms))*v

    return m,t,r,v


with open("datos_iniciales.txt", "r") as f:
        data = [line.split() for line in f.read().splitlines()]

data.pop(0)

m0,r0,v0 = [],[],[]
for linea in data:
        m0.append(float(linea[1]))
        r0.append(float(linea[2]))
        v0.append(float(linea[3]))


print(m0,r0,v0)

print(reescalamiento(np.array(m0),10,np.array(r0),np.array(0)))




