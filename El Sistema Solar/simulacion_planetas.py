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
    rnew[0] = np.array([0.,0.])
    w = v + h*a/2
    anew = calculaAceleracion(m,rnew)
    vnew = w + h*anew/2
    t+=h

    return t, rnew, vnew


# Programa principal 

if __name__=='__main__':

    m = np.array([1e6,1.,1.,1.])
    r0 = np.array([[0.,0.], [10.,0.], [30.,0.], [-80,-120]])
    v0 = np.array([[0.,0], [0.,300], [0.,180], [200,200]])

    h = 1e-3
    t = 0
    r = r0
    v = v0

    x1Data = [r0[1][0]]
    y1Data = [r0[1][1]]
    x2Data = [r0[2][0]]
    y2Data = [r0[2][1]]
    x3Data = [r0[3][0]]
    y3Data = [r0[3][1]]

    while t<100:

        t,r,v = Verlet(t,m,r,v,h)

        x1Data.append(r[1][0])
        y1Data.append(r[1][1])
        x2Data.append(r[2][0])
        y2Data.append(r[2][1])
        x3Data.append(r[3][0])
        y3Data.append(r[3][1])

        
    plt.plot(x1Data,y1Data)
    plt.plot(x2Data,y2Data)
    plt.plot(x3Data,y3Data)

    plt.xlim([-40, 40])
    plt.ylim([-40, 40])

    plt.show()

