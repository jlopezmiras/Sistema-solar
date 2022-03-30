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
        
    #Declaro el vector de aceleraciones a devolver
    aceleracion = []    
    for i in range(len(r)):

    # Inicializo la aceleración a aquella que le ejerce el sol 
    # y hago la sumatoria sobre todos los demás planetas (j)
        a = -r[i]/np.linalg.norm(r[i])**3
        for j in range(len(r)):
            if j!=i:   
                a -= m[j]*(r[i]-r[j])/np.linalg.norm(r[i]-r[j])**3

        # Añado la aceleración del planeta i al vector de aceleraciones
        aceleracion.append(a)

    return np.array(aceleracion)



# Recibe como parámetros los vectores de posición, velocidad y aceleración de cada partícula y el paso h
def Verlet(t,m,r,v,h):
    
    # Calculo la aceleración a partir de las posiciones en t
    a = calculaAceleracion(m,r)

    # Calculo los nuevos parámetros
    rnew = r + h*v + h**2*a/2
    w = v + h*a/2
    anew = calculaAceleracion(m,rnew)
    vnew = w + h*anew/2
    t+=h


    return t, rnew, vnew






# Programa principal 

if __name__=='__main__':

    filein = "datos_iniciales.txt"
    fileout = "planets_data.dat"

    m0,r0,v0 = leerDatos(filein)
    h, tmax = 1e-2, 1e3
    m,r,v = reescalamiento(np.array(m0),np.array(r0),np.array(v0))
    
    f = open(fileout, "w")

    t=0

    contador = 0
    start = timeit.default_timer()
    while t<tmax:

        t,r,v = Verlet(t,m,r,v,h)

        print(r)

        if contador%100==0:
        
            np.savetxt(f, r, delimiter=", ")
            f.write("\n")

        contador+=1

    f.close()
    
    # Muestra el tiempo que ha tardado 
    stop = timeit.default_timer()
    print('Time: ', stop - start)  

    