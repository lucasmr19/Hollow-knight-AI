import os

# Lista de números de imágenes que quieres eliminar
numeros_a_eliminar1 = [i for i in range(273,282)] # 83-89
numeros_a_eliminar2 = [i for i in range(257,263)]
#numeros_a_eliminar3 = [176, 177, 118, 119 ]
#numeros_a_eliminar4 = [i for i in range(186,205)]

numeros_a_eliminar = numeros_a_eliminar1 + numeros_a_eliminar2 #+ numeros_a_eliminar3 + numeros_a_eliminar4

directory = "screenshots"

extension = ".png"

def eliminar_imagenes(directory, numeros_a_eliminar, extension):
    # Asegúrate de que el directorio exista
    if not os.path.exists(directory):
        print(f"El directorio {directory} no existe.")
        return

    # Recorrer los números a eliminar
    for numero in numeros_a_eliminar:
        # Construir el nombre del archivo
        filename = f"{numero}{extension}"
        file_path = os.path.join(directory, filename)

        # Verificar si el archivo existe y eliminarlo
        if os.path.exists(file_path):
            os.remove(file_path)
            #print(f"Eliminado: {filename}")
        else:
            print(f"No encontrado: {filename}")

# Llamar a la función para eliminar las imágenes
eliminar_imagenes(directory, numeros_a_eliminar, extension)
