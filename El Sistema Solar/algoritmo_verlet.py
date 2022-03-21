import numpy as np
import matplotlib.pyplot as plt

# ------------------- Constantes físicas -----------------

g = 9.806


# ------------------- Funciones --------------------------

# Calcula la aceleración (angular) de un péndulo utilizando la segunda ley de Newton 
def calculaAceleracionPendulo(l,ang):
    return -g/l*np.sin(ang)
    


# Recibe como parámetros los vectores de posición, velocidad y aceleración de cada partícula y el paso h
def Verlet(l,t,ang,v,h):
    
    a = calculaAceleracionPendulo(l,ang)
    angNew = ang + h*v + h**2*a/2
    w = v + h*a/2
    aNew = calculaAceleracionPendulo(l,angNew)
    vNew = w + h*aNew/2
    t+=h

    return t, angNew, vNew


# Función principal

ang0 = 20
v0 = 0
h = 1e-4
l = 1

angData = [ang0]
vData = [v0]
tData = [0]

t = 0
ang = ang0*np.pi/180
v = v0

while t<4:
    t,ang,v = Verlet(l,t,ang,v,h)
    tData.append(t)
    angData.append(ang*180/np.pi)
    vData.append(v)
    print(t,ang)


fig, ax = plt.subplots()

plt.plot(tData,angData)
plt.show()
    



