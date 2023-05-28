import os
import pandas as pd
import shutil

PATH = os.path.dirname(__file__)

def gb_to_csv(fileName):
    # Mover al docker
    src = os.path.join(PATH,"..","static","tmp_files","gb_files",f"{fileName}")
    dst = os.path.join(PATH,"inputs",f"{fileName}")
    os.replace(src, dst) # Si existe borra el anterior, se puede usar rename pero da error si existe ya el fichero

    if(".gb" in fileName):
        fileCsv = fileName.replace(".gb", ".csv")
    os.system(f"docker container run --rm -v {PATH}:/shared global_image python3 /shared/code/gb2csv.py /shared/inputs/{fileName} {fileCsv}")

    # Mover al static
    src = os.path.join(PATH,"outputs","metadatos",f"{fileCsv}")
    dst = os.path.join(PATH,"..","static","outputs","metadatos.csv")
    os.replace(src, dst)

def gff3_to_csv(fileName):
    # Mover al docker
    src = os.path.join(PATH,"..","static","tmp_files","gff3_files",f"{fileName}")
    dst = os.path.join(PATH,"inputs",f"{fileName}")
    os.replace(src, dst) # Si existe borra el anterior, se puede usar rename pero da error si existe ya el fichero

    if(".gff3" in fileName):
        fileCsv = fileName.replace(".gff3", ".csv")
    os.system(f"docker container run --rm -v {PATH}:/shared global_image python3 /shared/code/gff32csv.py /shared/inputs/{fileName} {fileCsv}")

    # Mover al static
    src = os.path.join(PATH,"outputs","metadatos",f"{fileCsv}")
    dst = os.path.join(PATH,"..","static","outputs","metadatos.csv")
    os.replace(src, dst)

# Transformar gfa a csv para poder visualizarlo
def gfa_to_csv(fileName):
    if(".gfa" in fileName):
        fileCsv = fileName.replace(".gfa", ".csv")

    archivo = os.path.join(PATH,"outputs",f"{fileName}")
    L = False
    with open(archivo, 'r') as file:
        for line in file:
            if line.startswith('L'):
                L = True
                break

    src = os.path.join(PATH,"outputs","csv",f"{fileCsv}")
    if L is True:
        os.system(f"docker container run --rm -v {PATH}:/shared gfapy_image python3 /shared/code/gfa2csv.py /shared/outputs/{fileName} {fileCsv}")
    else: 
        with open(src, 'w') as file:
            file.write('start,end,orientation,overlap\n')

    # Mover al static
    dst = os.path.join(PATH,"..","static","outputs",f"{fileCsv}")
    os.replace(src, dst)
    html = os.path.join(PATH,"outPGGB","multiqc_report.html")
    dst = os.path.join(PATH,"..","static","outputs","multiqc_report.html")
    os.replace(html, dst)

def fasta_to_csv(fileName):
    if(".fasta" in fileName):
        fileCsv = fileName.replace(".fasta", ".csv")
    elif(".fa" in fileName):
        fileCsv = fileName.replace(".fa", ".csv")
    os.system(f"docker container run --rm -v {PATH}:/shared global_image python3 /shared/code/fasta2csv.py /shared/inputs/{fileName} {fileCsv}")

def join_csv_utils():
    input_path = os.path.join(PATH,"outputs","csv")
    lista_archivos = os.listdir(input_path)
    num_archivos = len(lista_archivos) - 1 # uno menos por el .gitkeep (necesario para que estén las carpetas vacísa)
    # Inicialmente todo True, porque cuando se carga el grafo, todas las secuencias están habilitadas
    bool_list = [True]*num_archivos
    dst = os.path.join(PATH, "..", "static", "outputs", "fasta_res.csv")
    join_csv_aux(bool_list, input_path, dst)

    dst2 = os.path.join(PATH, "..", "static", "outputs", "fasta_union.csv")
    join_csv_aux(bool_list, input_path, dst2)

def join_csv_aux(bool_list, path, fasta_res):
    files_list = [f for f in os.listdir(path) if f != '.gitkeep']
    frames = list()
    for i in range(len(bool_list)):
        if bool_list[i]:
            df = pd.read_csv(os.path.join(path, files_list[i]))
            frames.append(df)
    return pd.concat(frames).to_csv(fasta_res, index=False)

def pggb(fileName, referencia):
    os.system(f'docker container run --rm -v {PATH}:/shared global_image bgzip /shared/inputs/{fileName}')
    if(".fasta" in fileName):
        src = fileName.replace(".fasta", ".fasta.gz")

    os.system(f'docker container run --rm -v {PATH}:/shared global_image samtools faidx /shared/inputs/{src}')
    os.system(f'docker container run --rm -v {PATH}:/shared global_image sh -c "pggb -i /shared/inputs/*fasta.gz -o output -n 9 -t 16 -p 90 -s 5k -V "{referencia}:#" -o /shared/outPGGB -M -m"')

    # Para mover el gfa en outPGGB, y ponerle el nombre que deseamos
    src = os.path.join(PATH,"outPGGB")
    dst = os.path.join(PATH,"outputs","grafo.gfa")

    for file_name in os.listdir(src):
        if file_name.endswith(".gfa"):
            # Obtiene la ruta completa del archivo en el directorio de origen
            src_file = os.path.join(src, file_name)
            # Copiar archivo al static
            dst_gfa = os.path.join(PATH,"..","static","outputs","grafo.gfa")
            shutil.copy2(src_file, dst_gfa)
            # Mueve el archivo al directorio de destino utilizando os.replace()
            os.replace(src_file, dst)
            break

# Transformar fasta a gfa
def fasta_to_gfa(extension):
    if(".fasta" in extension):
        os.system(f'docker container run --rm -v {PATH}:/shared global_image sh -c "minigraph -cxggs -t16 /shared/inputs/*fasta > /shared/outputs/grafo.gfa"')
    elif(".fa" in extension):
        os.system(f'docker container run --rm -v {PATH}:/shared global_image sh -c "minigraph -cxggs -t16 /shared/inputs/*fa > /shared/outputs/grafo.gfa"')

def moveToDocker(fileName):
    src = os.path.join(PATH,"..","static","tmp_files",f"{fileName}")
    dst = os.path.join(PATH,"inputs",f"{fileName}")
    # Si existe borra el anterior, se puede usar rename pero da error si ya existe el fichero
    os.replace(src, dst) 

# Si el usuario selecciona un fasta, se divide en varios, porque quiere decir que es uno que contiene varios
def dividirFastas(fileName):
    salida = os.path.join(PATH,"inputs")
    os.system(f"docker container run --rm -v {PATH}:/shared global_image python3 /shared/code/dividirFasta.py /shared/inputs/{fileName} {salida}")


# Función que divide un csv en varios, por "row"
def dividirCSVs(fileName):
    df = pd.read_csv(fileName)
    # Agrupar los datos por valor de "row"
    grupos = df.groupby('row')

    for row, grupo in grupos:
        datos = pd.concat([grupo])
        src = os.path.join(PATH,"outputs","csv",f"{row}.csv")
        datos.to_csv(src, index=False)
    return len(grupos)