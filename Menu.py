# Importar el módulo sys para acceder a los argumentos de la línea de comandos
import sys

# Crear una lista con los nombres de los archivos disponibles
archivos = ["HandsMouse.py", "VisionMouse.py"]

# Mostrar un mensaje al usuario con las opciones
print("Por favor, elige uno de los siguientes archivos para ejecutar:")
for i, archivo in enumerate(archivos):
    print(f"{i+1}. {archivo}")

# Leer la entrada del usuario y validarla
opcion = input("Ingresa el número de tu opción: ")
try:
    opcion = int(opcion)
    if opcion < 1 or opcion > len(archivos):
        raise ValueError
except ValueError:
    print("Opción inválida. Debe ser un número entre 1 y {len(archivos)}.")
    sys.exit()

# Obtener el nombre del archivo elegido
archivo_elegido = archivos[opcion-1]

# Ejecutar el archivo usando el módulo runpy
import runpy
runpy.run_path(archivo_elegido)
print("cargando")
