from menu import menu_principal
from juego import iniciar_juego

def principal():
    # Ejecutar el menú y seleccionar el nivel
    nivel_seleccionado = menu_principal()
    
    # Iniciar el juego con el nivel seleccionado
    iniciar_juego(nivel_seleccionado)

if __name__ == "__main__":
    principal()
