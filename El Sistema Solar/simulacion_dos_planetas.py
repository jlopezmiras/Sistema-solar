import numpy as np
import matplotlib.pyplot as plt

# Constantes físicas
c = 1.496e11 #distancia Tierra-Sol (m)


# --------------------------------------------
#Clase planeta:
#Crea un objeto planeta con al menos los atributos de masa (mass), posición inicial (pos0)
#y velocidad inicial (vel0). Otros atributos posibles son el periodo (period), la energía (energy),
#la excentricidad (excentricity), etc.

class Planeta:

    def __init__(self,mass,pos0,vel0,**kwargs):

        self.mass = mass
        self.pos0 = pos0
        self.vel0 = vel0
        for attr in kwargs.keys():
            self.__dict__[attr] = kwargs[attr]



# Lee los datos y devuelve una lista de objetos planeta con los atributos especificados

def leerDatos(nfile):
    
    with open(nfile, "r") as f:
        data = [line.split() for line in f.read().splitlines()]

    r0 = (line[1] for line in data)

    




# Calcula la aceleración utilizando la ley de la gravitacion de Newton
#   r --> vector de vectores posicion reescalados de cada planeta 
#   m --> vector de la masa reescalada de cada planeta 

def calculaAceleracion(m,r):

    # Miro si los vectores son del mismo tamaño
    if len(m)==len(r):  
        
        #Declaro el vector de aceleraciones a devolver
        aceleracion = []    
        for i in range(len(r)):

            # Inicializo a (0,0) el vector aceleración para hacer la sumatoria sobre todos los planetas (j)
            a = np.zeros(2)   
            for j in range(len(r)):
                if j!=i:   
                    a -= m[j]*(r[i]-r[j])/np.linalg.norm(r[i]-r[j])**3

            # Añado la aceleración del planeta i al vector de aceleraciones
            aceleracion.append(a)

        return np.array(aceleracion)
    
    else:
        return False



# Recibe como parámetros los vectores de posición, velocidad y aceleración de cada partícula y el paso h
def Verlet(t,m,r,v,h):
    
    # Calculo la aceleración a partir de las posiciones en t
    a = calculaAceleracion(m,r)

    # Calculo los nuevos parámetros
    rnew = r + h*v + h**2*a/2
    rnew[0] = np.zeros(2)
    w = v + h*a/2
    anew = calculaAceleracion(m,rnew)
    vnew = w + h*anew/2
    t+=h

    return t, rnew, vnew


# Programa principal 

if __name__=='__main__':

    m = np.array([1.,1.])
    r0 = np.array([[0.,0.],[10.,0.]])
    v0 = np.array([[0.,-0.08],[0.,0.08]])

    h = 1e-3
    t = 0
    r = r0
    v = v0

    r1Data = [r0[0]]
    r2Data = [r0[1]]

    while t<100:

        t,r,v = Verlet(t,m,r,v,h)

        r1Data.append(r[0])
        r2Data.append(r[1])

    plt.plot(*zip(*r1Data))
    plt.plot(*zip(*r2Data))
    plt.show()
