import pygame
import random
import heapq
import time
from collections import deque
from utilidades import seleccionar_dificultad
from constantes import INICIO_PACMAN, ARRIBA, ABAJO, IZQUIERDA, DERECHA, NEGRO, AMARILLO, AZUL, VERDE, BLANCO
from constantes import MORADO, ROJO, CIAN, NARANJA
from menu import menu_principal

pygame.init()

def iniciar_juego(nivel_seleccionado):
    # Obtener las dimensiones de la ventana y otros valores antes de usar `pygame.display.set_mode`
    ancho_ventana, alto_ventana, tamaño_cuadrícula, ancho_cuadrícula, alto_cuadrícula, colores = seleccionar_dificultad(nivel_seleccionado)

    # Cargar las imágenes
    imagen_pacman = pygame.image.load('imagenes/pacman.gif')  # Ruta de la imagen del Pacman
    imagen_pacman = pygame.transform.scale(imagen_pacman, (tamaño_cuadrícula, tamaño_cuadrícula))  # Redimensiona la imagen

    imagen_meta = pygame.image.load('imagenes/meta.png')  # Ruta de la imagen de la meta
    imagen_meta = pygame.transform.scale(imagen_meta, (tamaño_cuadrícula, tamaño_cuadrícula))  # Redimensiona la imagen

    imagen_obstaculo = pygame.image.load('imagenes/obstaculo.png')  # Ruta de la imagen del obstáculo
    imagen_obstaculo = pygame.transform.scale(imagen_obstaculo, (tamaño_cuadrícula, tamaño_cuadrícula))  # Redimensiona la imagen

    # Inicializar la ventana con el tamaño correcto
    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption(f"Pacman Laberinto - Nivel: {nivel_seleccionado}")

    # Variables iniciales
    posicion_pacman = INICIO_PACMAN.copy()
    direccion_actual = None

    laberinto, zona_meta = generar_laberinto_valido(posicion_pacman, nivel_seleccionado, ancho_cuadrícula, alto_cuadrícula)
    meta = zona_meta[0]  # La meta es la esquina inferior derecha

    ruta_usuario = [tuple(posicion_pacman)]
    tiempo_inicio = time.time()

    juego_terminado = False

    # Bucle principal del juego
    while not juego_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    direccion_actual = ARRIBA
                elif evento.key == pygame.K_DOWN:
                    direccion_actual = ABAJO
                elif evento.key == pygame.K_LEFT:
                    direccion_actual = IZQUIERDA
                elif evento.key == pygame.K_RIGHT:
                    direccion_actual = DERECHA

        # Mover a Pacman
        posicion_pacman = mover_pacman(posicion_pacman, direccion_actual, laberinto, ancho_cuadrícula, alto_cuadrícula)
        ruta_usuario.append(tuple(posicion_pacman))

        if tuple(posicion_pacman) == meta:
            juego_terminado = True

        # Dibujar elementos del juego
        ventana.fill(NEGRO)
        dibujar_laberinto(ventana, laberinto, ancho_cuadrícula, alto_cuadrícula, tamaño_cuadrícula, imagen_obstaculo)
        dibujar_traza_pacman(ruta_usuario, ventana, tamaño_cuadrícula)
        dibujar_pacman(posicion_pacman, ventana, tamaño_cuadrícula, imagen_pacman)
        dibujar_meta(zona_meta, ventana, tamaño_cuadrícula, imagen_meta)

        pygame.display.flip()
        pygame.time.delay(200)

    # El juego ha terminado, Pacman ha llegado a la meta
    tiempo_fin = time.time()
    tiempo_usuario = tiempo_fin - tiempo_inicio

    # Encontrar rutas diversas (4 diferentes, si es posible)
    rutas, total_rutas = encontrar_rutas_diversas(laberinto, tuple(INICIO_PACMAN), zona_meta, ancho_cuadrícula, alto_cuadrícula)

    # Mostrar las rutas encontradas después de que el jugador llega a la meta
    if total_rutas > 0:
        mostrar_varias_rutas(ventana, laberinto, rutas, zona_meta, tamaño_cuadrícula, ancho_ventana, alto_ventana, ancho_cuadrícula, alto_cuadrícula, imagen_obstaculo, imagen_meta)

def camino_despejado(laberinto, inicio, area_meta, ancho_cuadrícula, alto_cuadrícula):
    # Inicializar una cola para la búsqueda en anchura (BFS) y un conjunto de visitados
    cola = deque([inicio])
    visitados = set()
    visitados.add(tuple(inicio))  # Convertir la posición inicial a tupla para agregarla al conjunto
    # Direcciones posibles de movimiento
    direcciones = [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
    while cola:
        x, y = cola.popleft()
        # Verificar si Pacman ha alcanzado la meta
        if (x, y) in area_meta:
            return True  # Camino encontrado
        # Explorar vecinos (celdas adyacentes)
        for direccion in direcciones:
            nuevo_x = x + direccion[0]
            nuevo_y = y + direccion[1]
            # Comprobar si la nueva posición está dentro de los límites del laberinto y es transitable
            if 0 <= nuevo_x < ancho_cuadrícula and 0 <= nuevo_y < alto_cuadrícula and laberinto[nuevo_y][nuevo_x] == 0:
                nueva_pos = (nuevo_x, nuevo_y)
                
                # Si no ha sido visitada, agregar a la cola y marcar como visitada
                if nueva_pos not in visitados:
                    visitados.add(nueva_pos)
                    cola.append(nueva_pos)
    # Si la cola se vacía sin encontrar la meta, no hay camino despejado
    return False

def generar_laberinto_valido(inicio_pacman, nivel, ancho_cuadrícula, alto_cuadrícula):
    while True:
        laberinto = generar_obstaculos_aleatorios(nivel, ancho_cuadrícula, alto_cuadrícula)  # Pasa las dimensiones dinámicas
        area_meta = generar_meta(ancho_cuadrícula, alto_cuadrícula)  # Pasa las dimensiones dinámicas
        
        # Si hay un camino despejado, devuelve el laberinto
        if camino_despejado(laberinto, inicio_pacman, area_meta, ancho_cuadrícula, alto_cuadrícula):
            return laberinto, area_meta

def generar_obstaculos_aleatorios(nivel, ancho_cuadrícula, alto_cuadrícula):
    # Inicializar laberinto con celdas vacías (0)
    laberinto = [[0 for _ in range(ancho_cuadrícula)] for _ in range(alto_cuadrícula)]
    
    # Ajustar el porcentaje de obstáculos según el nivel de dificultad
    if nivel == "fácil":
        nivel_num = 1
    elif nivel == "medio":
        nivel_num = 2
    elif nivel == "difícil":
        nivel_num = 3

    # Reducimos el porcentaje de obstáculos para permitir más rutas
    porcentaje_obstaculos = 0.30  # Reducido para más espacio
    num_obstaculos = int((ancho_cuadrícula * alto_cuadrícula) * porcentaje_obstaculos)

    # Colocar obstáculos aleatorios en el laberinto
    for _ in range(num_obstaculos):
        x = random.randint(0, ancho_cuadrícula - 1)
        y = random.randint(0, alto_cuadrícula - 1)

        # Asegurarse de que la posición de inicio de Pacman no esté bloqueada
        if (x, y) != (0, 0):
            laberinto[y][x] = 1  # Coloca un obstáculo en la celda
    
    return laberinto

def generar_meta(ancho_cuadrícula, alto_cuadrícula):
    area_meta = [(ancho_cuadrícula - 1, alto_cuadrícula - 1)]
    return area_meta

def dibujar_laberinto(ventana, laberinto, ancho_cuadrícula, alto_cuadrícula, tamaño_cuadrícula, imagen_obstaculo):
    for y in range(alto_cuadrícula):
        for x in range(ancho_cuadrícula):
            if laberinto[y][x] == 1:
                ventana.blit(imagen_obstaculo, (x * tamaño_cuadrícula, y * tamaño_cuadrícula))  # Dibuja la imagen del obstáculo

def dibujar_pacman(posicion, ventana, tamaño_cuadrícula, imagen_pacman):
    x, y = posicion
    ventana.blit(imagen_pacman, (x * tamaño_cuadrícula, y * tamaño_cuadrícula))  # Dibuja la imagen de Pacman

def dibujar_meta(area_meta, ventana, tamaño_cuadrícula, imagen_meta):
    for (x, y) in area_meta:
        ventana.blit(imagen_meta, (x * tamaño_cuadrícula, y * tamaño_cuadrícula))  # Dibuja la imagen de la meta

def mover_pacman(posicion, direccion, laberinto, ancho_cuadrícula, alto_cuadrícula):
    if direccion is None:
        return posicion
    nuevo_x = posicion[0] + direccion[0]
    nuevo_y = posicion[1] + direccion[1]
    if 0 <= nuevo_x < ancho_cuadrícula and 0 <= nuevo_y < alto_cuadrícula and laberinto[nuevo_y][nuevo_x] == 0:
        return [nuevo_x, nuevo_y]
    return posicion

def dibujar_traza_pacman(posiciones_visitadas, ventana, tamaño_cuadrícula):
    for pos in posiciones_visitadas:
        x, y = pos
        pygame.draw.circle(ventana, BLANCO, (x * tamaño_cuadrícula + tamaño_cuadrícula // 2, y * tamaño_cuadrícula + tamaño_cuadrícula // 2), 5)

def encontrar_rutas_diversas(laberinto_original, inicio, area_meta, ancho_cuadrícula, alto_cuadrícula):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def obtener_vecinos(pos, laberinto):
        x, y = pos
        vecinos = []
        direcciones = [ARRIBA, ABAJO, IZQUIERDA, DERECHA]
        random.shuffle(direcciones)  # Alterar el orden para hacer la ruta más diversa
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ancho_cuadrícula and 0 <= ny < alto_cuadrícula and laberinto[ny][nx] == 0:
                vecinos.append((nx, ny))
        return vecinos

    def encontrar_ruta(inicio, meta, celdas_prohibidas, laberinto):
        conjunto_abierto = []
        heapq.heappush(conjunto_abierto, (0, inicio, []))
        puntaje_g = {inicio: 0}
        puntaje_f = {inicio: heuristica(inicio, meta)}
        
        while conjunto_abierto:
            actual_f, actual, camino = heapq.heappop(conjunto_abierto)
            
            if actual == meta:
                return camino + [actual]
            
            for vecino in obtener_vecinos(actual, laberinto):
                if vecino in celdas_prohibidas:
                    continue
                
                puntaje_g_tentativo = puntaje_g[actual] + 1
                if vecino not in puntaje_g or puntaje_g_tentativo < puntaje_g[vecino]:
                    puntaje_g[vecino] = puntaje_g_tentativo
                    puntaje_f_vecino = puntaje_g_tentativo + heuristica(vecino, meta)
                    heapq.heappush(conjunto_abierto, (puntaje_f_vecino, vecino, camino + [actual]))
        
        return None

    rutas = []
    celdas_prohibidas = set()
    total_rutas_posibles = 0  # Inicializa el contador de rutas posibles
    laberinto = [fila[:] for fila in laberinto_original]  # Copia del laberinto original

    # Intentar encontrar exactamente 4 rutas
    while len(rutas) < 4:
        ruta = encontrar_ruta(inicio, area_meta[0], celdas_prohibidas, laberinto)
        if ruta:
            rutas.append(ruta)
            total_rutas_posibles += 1
            
            # Bloquear toda la ruta encontrada en el laberinto
            for celda in ruta[1:-1]:
                celdas_prohibidas.add(celda)

        else:
            break

    return rutas, total_rutas_posibles

def mostrar_varias_rutas(ventana, laberinto, rutas, area_meta, tamaño_cuadrícula, ancho_ventana, alto_ventana, ancho_cuadrícula, alto_cuadrícula, imagen_obstaculo, imagen_meta):
    colores = [MORADO, ROJO, CIAN, NARANJA]

    for i, ruta in enumerate(rutas):
        ventana.fill(NEGRO)
        dibujar_laberinto(ventana, laberinto, ancho_cuadrícula, alto_cuadrícula, tamaño_cuadrícula, imagen_obstaculo)
        dibujar_meta(area_meta, ventana, tamaño_cuadrícula, imagen_meta)  
        
        for j, (x, y) in enumerate(ruta):
            if j > 0:
                pygame.draw.rect(ventana, colores[i % len(colores)], pygame.Rect(
                    x * tamaño_cuadrícula + tamaño_cuadrícula // 4, 
                    y * tamaño_cuadrícula + tamaño_cuadrícula // 4, 
                    tamaño_cuadrícula // 2, 
                    tamaño_cuadrícula // 2
                ))
        pygame.display.flip()
        time.sleep(2)  # Mostrar cada ruta durante 2 segundos

def principal():
    # Inicializar pygame
    pygame.init()

    # Ejecutar el menú y obtener el nivel seleccionado
    nivel_seleccionado = menu_principal()

    # Obtener los valores según el nivel seleccionado
    ancho_ventana, alto_ventana, tamaño_cuadrícula, ancho_cuadrícula, alto_cuadrícula, colores = seleccionar_dificultad(nivel_seleccionado)

    # Crear la ventana con las dimensiones dinámicas según el nivel seleccionado
    ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption("Pacman Laberinto")

    # Iniciar el juego con el nivel seleccionado
    iniciar_juego(nivel_seleccionado, ventana, ancho_cuadrícula, alto_cuadrícula, tamaño_cuadrícula)

    # Variables iniciales
    posicion_pacman = INICIO_PACMAN.copy()
    direccion_actual = None

    while True:
        laberinto, zona_meta = generar_laberinto_valido(posicion_pacman, nivel_seleccionado, ancho_cuadrícula, alto_cuadrícula)
        meta = zona_meta[0]  # La meta ahora es la esquina inferior derecha
        juego_terminado = False
        ruta_usuario = [tuple(posicion_pacman)]
        tiempo_inicio = time.time()

        while not juego_terminado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        direccion_actual = ARRIBA
                    elif evento.key == pygame.K_DOWN:
                        direccion_actual = ABAJO
                    elif evento.key == pygame.K_LEFT:
                        direccion_actual = IZQUIERDA
                    elif evento.key == pygame.K_RIGHT:
                        direccion_actual = DERECHA

            # Mover Pacman
            posicion_pacman = mover_pacman(posicion_pacman, direccion_actual, laberinto, ancho_cuadrícula, alto_cuadrícula)
            ruta_usuario.append(tuple(posicion_pacman))

            if tuple(posicion_pacman) == meta:
                juego_terminado = True

            # Dibujar elementos en la ventana
            ventana.fill(NEGRO)
            dibujar_laberinto(ventana, laberinto, ancho_cuadrícula, alto_cuadrícula, tamaño_cuadrícula)
            dibujar_traza_pacman(ruta_usuario, ventana, tamaño_cuadrícula)
            dibujar_pacman(posicion_pacman, ventana, tamaño_cuadrícula)
            dibujar_meta(zona_meta, ventana, tamaño_cuadrícula)

            pygame.display.flip()
            pygame.time.delay(200)

        tiempo_fin = time.time()
        tiempo_usuario = tiempo_fin - tiempo_inicio

        # Encontrar y mostrar las rutas
        rutas = encontrar_rutas_diversas(laberinto, tuple(INICIO_PACMAN), zona_meta, ancho_cuadrícula, alto_cuadrícula)
        mostrar_varias_rutas(laberinto, rutas, zona_meta, ruta_usuario, tiempo_usuario, ventana, tamaño_cuadrícula, ancho_ventana, alto_ventana)

        # Reiniciar posición Pacman
        posicion_pacman = INICIO_PACMAN.copy()