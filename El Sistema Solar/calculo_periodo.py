import numpy as np
import math
import matplotlib.pyplot as plt


# Constantes

G = 6.67e-11
Ms = 1.99e30
c = 1.496e11

# Lectura del fichero de datos
# ========================================
def leerDatos(file_in):
    # Lee el fichero a una cadena de texto
    with open(file_in, "r") as f:
        data_str = f.read()

    # Inicializa la lista con los datos de cada fotograma.
    # frames_data[j] contiene los datos del fotograma j-ésimo
    frames_data = list()


    # Itera sobre los bloques de texto separados por líneas vacías
    # (cada bloque corresponde a un instante de tiempo)
    for frame_data_str in data_str.split("\n\n"):
        # Inicializa la lista con la posición de cada planeta
        frame_data = list()

        # Itera sobre las líneas del bloque
        # (cada línea da la posición de un planta)
        for planet_pos_str in frame_data_str.split("\n"):
            # Lee la componente x e y de la línea
            planet_pos = np.fromstring(planet_pos_str, sep=",")
            # Si la línea no está vacía, añade planet_pos a la lista de 
            # posiciones del fotograma
            if planet_pos.size > 0:
                frame_data.append(np.fromstring(planet_pos_str, sep=","))

        # Añade los datos de este fotograma a la lista
        frames_data.append(frame_data)

    # El número de planetas es el número de líneas en cada bloque
    # Lo calculamos del primer bloque
    nplanets = len(frames_data[0])

    return frames_data[:-1], nplanets



def calculaPeriodos(frames_data, nplanets, h):

    pos_iniciales = frames_data[0]

    # Resto a todas las posiciones la posición inicial
    # Así, cada planeta tiene su propio eje de coordenadas y se encuentra en el origen en t=0
    for row in range(len(frames_data)):
        for planet in range(nplanets):
            frames_data[row][planet] -= pos_iniciales[planet]

    contador = np.zeros(nplanets, dtype=int)
    for i in range(nplanets):
        y, steps = 0, 0
        while (y>=0):
            y = frames_data[steps][i][1]
            steps+=1

        while(y<=0):
            y = frames_data[steps][i][1]
            steps+=1

        contador[i] = steps

    return contador*h



def calculaEnergia(frames_data, nplanets):

    steps = len(frames_data)
    energia = np.empty((steps, nplanets))

    for i in range(steps):
        energia[i]




frames_data, nplanets = leerDatos("planets_data_extended.dat")

# Calculamos y eescalamos el periodo
periodos = math.sqrt(c**3/(G*Ms))/3600/24*calculaPeriodos(frames_data, nplanets,1e-2)

planetas = ["Mercurio", "Venus", "Tierra", "Marte ", "Jupiter", "Saturno", "Urano", "Neptuno"]
planetas = [name.ljust(8," ") for name in planetas]

periodos = np.round(periodos, 4)

periodos_reales = np.array([88, 225, 365, 687, 4333, 10759, 30687, 60190])

dif_periodos = np.round(periodos_reales-periodos, 4)

dif_rel_periodos = np.round(np.abs(dif_periodos)/periodos_reales*100, 4)


with open("Periodos.txt", "w") as f:
    f.write("Planeta \tPeriodo calculado\tPeriodo real\tDiferencia\tDiferencia relativa (%)\n\n")
    for i in range(nplanets):
        f.write(planetas[i] + "\t")
        f.write(str(periodos[i]).ljust(17," ") +"\t")
        f.write(str(periodos_reales[i]).ljust(12," ") + "\t")
        f.write(str(dif_periodos[i]).ljust(10," ") + "\t")
        f.write(str(dif_rel_periodos[i])+"\n")



