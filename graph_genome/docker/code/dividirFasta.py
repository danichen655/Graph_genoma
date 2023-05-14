import os
import sys

if len(sys.argv) < 3:
    exit()

archivo = sys.argv[1]
ruta_salida = sys.argv[2]

with open(archivo) as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    if ">" in lines[i]:
        if(i == 0):
            mi_referencia = lines[i].split(">")[1].split()[0]
        nombre_archivo = lines[i].split(">")[1].split()[0] + ".fasta"
        datos_archivo = lines[i].split()[0] + "\n"
        i += 1
        while i < len(lines) and ">" not in lines[i]:
            datos_archivo += lines[i]
            i += 1
        with open(os.path.join(ruta_salida, nombre_archivo), "w") as f:
            f.write(datos_archivo)
            f.close()
    else:
        i += 1

with open(os.path.join(ruta_salida, "referencia"), "w") as f:
    # Escribir la variable en el archivo
    f.write(mi_referencia)
    f.close()
