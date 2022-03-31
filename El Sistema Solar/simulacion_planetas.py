import numpy as np
import matplotlib.pyplot as plt
import math
import timeit


# Constantes físicas
c = 1.496e11 # distancia Tierra-Sol (m)
G = 6.67e-11 # constante de gravedad (Nm²/kg²)
Ms = 1.99e30  # masa del Sol (kg)


# Lee los datos y devuelve una lista de objetos planeta con los atributos especificados
# Los datos tienen que estar formateados por columnas de la forma nombre, masa, x, y, vx,
# vy y cada fila es un planeta distinto
def leerDatos(nfile):
    
    with open(nfile, "r") as f:
        data = [line.split() for line in f.read().splitlines()]

    data.pop(0)

    m0,r0,v0 = [],[],[]
    for linea in data:
        m0.append(float(linea[1]))
        r0.append([float(linea[2]),0])
        v0.append([0,float(linea[3])])

    return m0,r0,v0



# Función que reescala los valores a unidades de distancia tierra-sol
# Devuelve los valores rrescalados de todos los argumentos
def reescalamiento(m,r,v):

    m = m/Ms
    r = r/c
    v = math.sqrt(c/(G*Ms))*v

    return m,r,v


# Calcula la aceleración utilizando la ley de la gravitacion de Newton
#   r --> vector de vectores posicion reescalados de cada planeta 
#   m --> vector de la masa reescalada de cada planeta 
def calculaAceleracion(m,r):
    
    n = len(r)
    #Declaro el vector de aceleraciones a devolver  
    a = np.empty((n,2))
    for i in range(n):
        dist = math.sqrt(r[i,0]*r[i,0] + r[i,1]*r[i,1])
        a[i,0] = -r[i,0]/(dist*dist*dist)
        a[i,1] = -r[i,1]/(dist*dist*dist)
        for j in range(n):
            if j!=i:
                r_ij_x = r[i,0]-r[j,0]
                r_ij_y = r[i,1]-r[j,1]
                dist = math.sqrt( r_ij_x*r_ij_x + r_ij_y*r_ij_y )
                a[i,0] -= m[j]*r_ij_x/(dist*dist*dist)
                a[i,1] -= m[j]*r_ij_y/(dist*dist*dist)
    return a


# Recibe como parámetros los vectores de posición, velocidad y aceleración de cada partícula y el paso h
def Verlet(m,r,v,h,a):
    
    # Calculo los nuevos parámetros
    w = v + 0.5*h*a
    r += h*w
    a = calculaAceleracion(m,r)
    v = w + 0.5*h*a

    return r,v,a



# Programa principal 

if __name__=='__main__':

    filein = "datos_iniciales.txt"
    fileout = "planets_data.dat"

    m0,r0,v0 = leerDatos(filein)
    h, tmax = 1e-2, 2e3
    m,r,v = reescalamiento(np.array(m0),np.array(r0),np.array(v0))
    
    f = open(fileout, "w")

    t=0
    contador = 0

    start = timeit.default_timer()
    a = calculaAceleracion(m,r)
    while t<tmax:

        r,v,a = Verlet(m,r,v,h,a)

        if contador%100==0:
            
            np.savetxt(f, r, delimiter=", ")
            f.write("\n")

        t+=h
        contador+=1

    f.close()
    
    # Muestra el tiempo que ha tardado 
    stop = timeit.default_timer()
    print('Time: ', stop - start)


