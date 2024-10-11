import pygame
from constantes import NEGRO, AZUL, GRIS, VERDE, BLANCO

pygame.init()

def menu_principal():
    ventana = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Seleccionar Nivel de Dificultad")

    # Fuente para el texto
    fuente = pygame.font.SysFont(None, 45)

    # Definir botones de nivel de dificultad
    boton_facil = pygame.Rect(100, 100, 400, 50)
    boton_medio = pygame.Rect(100, 180, 400, 50)
    boton_dificil = pygame.Rect(100, 260, 400, 50)
    boton_iniciar = pygame.Rect(200, 330, 200, 50)

    nivel_seleccionado = None

    # Función para mostrar texto
    def dibujar_texto(texto, fuente, color, superficie, x, y):
        texto_objeto = fuente.render(texto, True, color)
        texto_rect = texto_objeto.get_rect(center=(x, y))
        superficie.blit(texto_objeto, texto_rect)

    # Bucle del menú
    menu_activo = True
    while menu_activo:
        ventana.fill(NEGRO)  # Fondo negro

        # Dibujar botones de niveles
        pygame.draw.rect(ventana, AZUL if nivel_seleccionado == "fácil" else GRIS, boton_facil)
        pygame.draw.rect(ventana, AZUL if nivel_seleccionado == "medio" else GRIS, boton_medio)
        pygame.draw.rect(ventana, AZUL if nivel_seleccionado == "difícil" else GRIS, boton_dificil)

        # Dibujar botón de iniciar (solo activo si hay un nivel seleccionado)
        if nivel_seleccionado:
            pygame.draw.rect(ventana, VERDE, boton_iniciar)
        else:
            pygame.draw.rect(ventana, GRIS, boton_iniciar)

        # Agregar texto a los botones
        dibujar_texto("FÁCIL", fuente, BLANCO, ventana, boton_facil.centerx, boton_facil.centery)
        dibujar_texto("MEDIO", fuente, BLANCO, ventana, boton_medio.centerx, boton_medio.centery)
        dibujar_texto("DIFÍCIL", fuente, BLANCO, ventana, boton_dificil.centerx, boton_dificil.centery)
        dibujar_texto("INICIAR", fuente, BLANCO, ventana, boton_iniciar.centerx, boton_iniciar.centery)

        # Actualizar pantalla
        pygame.display.flip()

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_raton = pygame.mouse.get_pos()

                # Verificar si el usuario hizo clic en algún botón
                if boton_facil.collidepoint(pos_raton):
                    nivel_seleccionado = "fácil"
                elif boton_medio.collidepoint(pos_raton):
                    nivel_seleccionado = "medio"
                elif boton_dificil.collidepoint(pos_raton):
                    nivel_seleccionado = "difícil"

                # Si seleccionó un nivel, permitir hacer clic en "Iniciar"
                if nivel_seleccionado and boton_iniciar.collidepoint(pos_raton):
                    menu_activo = False
                    return nivel_seleccionado
