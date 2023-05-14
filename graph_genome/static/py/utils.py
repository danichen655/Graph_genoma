from ...docker.utils import *
from io import BytesIO
import pandas as pd
import os
import shutil
import zipfile

# Unir los fastas de la ruta
def juntarFastas():
    ruta = "graph_genome\\docker\\inputs"
    extension = ".fasta"
    destino = "graph_genome\\docker\\inputs\\fastaFinal.fasta"

    with open(destino, 'wb') as archivo_unido:
        for archivo in os.listdir(ruta):
            if archivo.endswith(extension) and os.path.basename(archivo) != os.path.basename("fastaFinal.fasta"):
                with open(os.path.join(ruta, archivo), 'rb') as archivo_actual:
                    archivo_unido.write(archivo_actual.read())
                archivo_unido.write(os.linesep.encode())

# Limpiar archivos anteriores
def limpiezaDocker():
    PATH = 'graph_genome\\docker\\inputs'
    for f in os.listdir(PATH):
        if f != '.gitkeep':
            os.remove(os.path.join(PATH, f))
    
    PATH = 'graph_genome\\docker\\outPGGB'
    for f in os.listdir(PATH):
        file_path = os.path.join(PATH, f)
    
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else: 
            if f != '.gitkeep':
                os.remove(file_path)

    PATH = 'graph_genome\\docker\\outputs'
    for f in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH, f)):
            if f != '.gitkeep':
                os.remove(os.path.join(PATH, f))

    dir = os.path.join(PATH, "csv")
    for f in os.listdir(dir):
        if f != '.gitkeep':
            os.remove(os.path.join(dir, f))

    dir = os.path.join(PATH, "metadatos")
    for f in os.listdir(dir):
        if f != '.gitkeep':
            os.remove(os.path.join(dir, f))

def limpiezaOuputsAnteriores():
    PATH = 'graph_genome\\static\\outputs'
    
    for f in os.listdir(PATH):
        if os.path.isfile(os.path.join(PATH, f)):
            if f != '.gitkeep':
                os.remove(os.path.join(PATH, f))

# Subir los archivos fasta
def upload_fasta(request):
    # Seleccionar múltiples fastas
    files = request.FILES.getlist('dna')
    lenFiles = len(files)
    # Si sólo se sube un archivo, se interpreta como que tiene más fastas dentro, y se divide en varios
    if len(files) == 1:
        with open('graph_genome\\static\\tmp_files\\' + os.path.basename(files[0].name), 'wb') as f:
            for chunk in files[0].chunks():
                f.write(chunk)
                f.close()
                moveToDocker(files[0].name)
        dividirFastas(files[0].name)

        dir_path = "graph_genome\\docker\\inputs"
        ficheros = os.listdir(dir_path)
        aux = 0
        for fichero in ficheros:
            if os.path.basename(files[0].name) != os.path.basename(fichero) and fichero.endswith(".fasta"):
                aux = aux+1
                fasta_to_csv(fichero)
        
        lenFiles = aux
        # Coger la referencia
        referencia = os.path.join(PATH,"inputs","referencia")
        with open(referencia, 'r') as f:
            contenido = f.read()

        join_csv_utils()
        pggb(files[0].name, contenido)
    else:
        for file in files:
            with open('graph_genome\\static\\tmp_files\\' + file.name, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                    f.close() # Para que no se queje cuando otro proceso está usando el mismo fichero
                    moveToDocker(file.name)
                    fasta_to_csv(file.name)
        join_csv_utils()
        juntarFastas()
        pggb("fastaFinal.fasta", os.path.splitext(files[0].name)[0])
    
    gfa_to_csv("grafo.gfa")
    return lenFiles

def upload_metadata(request):
    # Seleccionamos el archivo de metadatos (primero revisamos cuál entra, si gb o gff3)
    file_obj = request.FILES['metadata']
    filename, file_extension = os.path.splitext(file_obj.name)
    if file_extension == '.gff3': ruta = "gff3_files\\" + file_obj.name
    elif file_extension == '.gb': ruta = "gb_files\\" + file_obj.name

    with open('graph_genome\\static\\tmp_files\\' + ruta, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()

    # Según la extensión, aplicamos una transformación u otra
    if file_extension == ".gff3": gff3_to_csv(file_obj.name)
    elif file_extension == ".gb": gb_to_csv(file_obj.name)

# Descomprimir zip con el graph genome, e incluir cada archivo en su ruta correspondiente para que se pueda visualizar
def upload_descargas(request):
    files = request.FILES.getlist('graphGenome')
    for file in files:
        if file.name.endswith('.zip'):
            with zipfile.ZipFile(BytesIO(file.read()), 'r') as zip_ref:
                zip_ref.extractall("graph_genome\\static\\outputs\\")
    lenFiles = dividirCSVs("graph_genome\\static\\outputs\\fasta_res.csv")
    return lenFiles

# Cargar el grafo
def cargar_grafo(arrSwitch):
    ruta_outputs = 'graph_genome\\static\\outputs\\'
    df = pd.read_csv(ruta_outputs + 'metadatos.csv')
    opciones = {}
    for i, row in df.iterrows():
        opciones[row['gen']] = [row['start'], row['end']]

    dfaux = pd.read_csv(ruta_outputs + 'fasta_union.csv')
    # Coger la última posición, para pasárselo al xDomain como configuración inicial, y poder visualizar el grafo entero
    end = int(dfaux[-1:]["start"])
    secuencias_union = dfaux["row"].unique()

    df2 = pd.read_csv(ruta_outputs + "fasta_res.csv")
    secuencias = df2["row"].unique()
    secuencias_dicc = dict(zip(secuencias, arrSwitch))
    context = {
        'opciones': opciones,
        'end': end,
        'secuencias': secuencias_union,
        'secuencias_dicc': secuencias_dicc
    }
    return context