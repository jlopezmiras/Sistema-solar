from operator import le
import numpy as np
import matplotlib.pyplot as plt

# Constantes físicas
c = 1.496e11 #distancia Tierra-Sol (m)

# Calcula la aceleración utilizando la ley de la gravitacion de Newton
#   r --> vector de vectores posicion reescalados de cada planeta (9x2)
#   m --> vector de la masa reescalada de cada planeta (9)
def calculaAceleracion(m,r):

    # Miro si los vectores son del mismo tamaño
    if len(m)==len(r):  
        
        #Declaro el vector de aceleraciones a devolver
        aceleracion = []    
        for i in range(len(r)):

            # Inicializo a (0,0) el vector aceleración para hacer la sumatoria sobre todos los planetas (j)
            a = np.array([0.,0.])     
            for j in range(len(r)):
                if j!=i:   
                    a -= m[j]*(r[i]-r[j])/np.linalg.norm(r[i]-r[j]) 

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
    rnew[0] = np.array([0.,0.])
    w = v + h*a/2
    anew = calculaAceleracion(m,rnew)
    vnew = w + h*anew/2
    t+=h

    return t, rnew, vnew


# Programa principal 

m = np.array([1.,1.])
r0 = np.array([[0.,0.],[10.,0.]])
v0 = np.array([[0.,0.],[0.,1.]])

h = 1e-3
t = 0
r = r0
v = v0

x2Data = [r0[1][0]]
y2Data = [r0[1][1]]

while t<200:

    t,r,v = Verlet(t,m,r,v,h)

    x2Data.append(r[1][0])
    y2Data.append(r[1][1])


plt.plot(x2Data,y2Data)
plt.show()

