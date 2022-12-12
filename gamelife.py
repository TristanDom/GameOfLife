"""EL JUEGO DE LA VIDA.
Este juego está basado en el popular."""

# Juego de la vida de Conway programado en Python con la librería de pygame, numpy y time por Tristán Domínguez.
# https://github.com/TristanDom

# Se importa las librerías necesarias para el correcto funcionamiento del juego.
# Como lo son la de pygame para la creación de la interfaz gráfica y la de numpy para la creación de la matriz.
import pygame
import numpy as np
import time

# Se imprime por pantalla mensaje de bienvenida y para conocer un poco el juego.
# Ajustes del juego para la cantidad de celdas en pantalla.
print("Hola, bienvenido al juego de la vida de Conway, vamos a ajustar algunos parámetros...")
print("Comencemos con las dimensiones de la pantalla...")

dim = input("Ingrese que tan grande quiere que se muestren los recuadros en pantalla 'ch', 'm' o 'g': ")

if dim == "ch":
    nxC, nyC = 10, 10
elif dim == "m":
    nxC, nyC = 50, 50
elif dim == "g":
    nxC, nyC = 100, 100
else:
    print("No se ingresó una opción válida, se seleccionará la opción por defecto.")
    nxC, nyC = 50, 50

# Se inicializa pygame.
pygame.init()

# Se crea la pantalla del juego con las dimensiones.
width, height = 1000, 1000

# se crea la pantalla del juego con las dimensionaes dadas con anterioridad con el método set_mode de pygame.
screen = pygame.display.set_mode((height, width))

# Se crea la variable bg que contendrá el color de fondo de la pantalla.
bg = 25, 25, 25

# Se crea la variable que contendrá el color de las celdas muertas.
screen.fill(bg)

# Se selecciona cuantas celdas se quieren en el eje x y en el eje y.
# nxC, nyC = 100, 100

# Se crea la variable dimCW que contendrá el ancho de cada celda.
dimCW = width / nxC

# Se crea la variable dimCH que contiene el largo de cada celda.
dimCH = height / nyC

# Se crea una matriz vacía con alluda de la función de zeros, la cual arroja un tablero vacío.
gameState = np.zeros((nxC, nyC))

# Variable para controlar la ejecución del juego.
pauseExec = False

# Implementación de célula vertical inicial.
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Bucle de ejecución del juego.
while True:


    newGameState = np.copy(gameState)

    # Límpia la pantalla con cada actualización. 
    screen.fill(bg)

    # Con la librería time se establede cuanto tiempo se desea esperar entre cada itereación para que haya una transición.
    time.sleep(0.1)

    # Con el método event.get() se obtiene la techa se acaba de presionar.
    ev = pygame.event.get()

    # Se crea un bucle for para detectar si la tecla "flecha abajo" se ha presionado y para conocer el clic del ratón.
    for event in ev:

        # Si se presiona la tecla indicada para pausa el juego se pausará, si se vuelve a presionar se quitará la pausa.
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Detecta el clic presionado con el mouse para activar una u otra función.
        # Si se presiona clic derecho se activa una célula.
        # Si se presiona clic izquierdo se muere la célula seleccionada.
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)
                             ), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

        # mouseClick = pygame.mouse.get_pressed()

    # For para el comportamiento de las coordenadas y la estratégia toroidal o estratégia del pacman.
    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExec:
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                    gameState[(x) % nxC, (y-1) % nyC] + \
                    gameState[(x+1) % nxC, (y-1) % nyC] + \
                    gameState[(x-1) % nxC, (y) % nyC] + \
                    gameState[(x+1) % nxC, (y) % nyC] + \
                    gameState[(x-1) % nxC, (y+1) % nyC] + \
                    gameState[(x) % nxC, (y+1) % nyC] + \
                    gameState[(x+1) % nxC, (y+1) % nyC]

                # Regla 1: Una célula muerta con exactamente 3 vecinas vivas "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas "muere".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]
            
            # Dibuja la el estado de la matriz además de el grosor de la líneas que lo dividen.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

# Imprime en pantalla la copia que se ha recolectado del sistema.
    gameState = np.copy(newGameState)

# Imprime en pantalla un recuadro para visualizar.
    pygame.display.flip()