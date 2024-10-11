def seleccionar_dificultad(nivel):
    tamaño_cuadrícula = 20  # Esto es constante para todos los niveles
    colores = {
        "fondo": (0, 0, 0)  # Negro
    }

    if nivel == "fácil":
        ancho_ventana, alto_ventana = 600, 400
        colores.update({
            "jugador": (255, 255, 0),  # Amarillo
            "meta": (0, 255, 0),  # Verde claro
            "obstáculos": (0, 0, 255)  # Azul
        })
    elif nivel == "medio":
        ancho_ventana, alto_ventana = 900, 600
        colores.update({
            "jugador": (255, 165, 0),  # Naranja
            "meta": (0, 255, 255),  # Cian
            "obstáculos": (255, 0, 0)  # Rojo
        })
    elif nivel == "difícil":
        ancho_ventana, alto_ventana = 1200, 800
        colores.update({
            "jugador": (255, 255, 255),  # Blanco
            "meta": (255, 0, 255),  # Púrpura
            "obstáculos": (255, 0, 0)  # Rojo
        })
    else:
        raise ValueError("Nivel de dificultad no válido. Opciones válidas: fácil, medio, difícil.")

    # Actualizar el número de celdas en la cuadrícula para que cubra la nueva pantalla
    ancho_cuadrícula = ancho_ventana // tamaño_cuadrícula
    alto_cuadrícula = alto_ventana // tamaño_cuadrícula

    return ancho_ventana, alto_ventana, tamaño_cuadrícula, ancho_cuadrícula, alto_cuadrícula, colores