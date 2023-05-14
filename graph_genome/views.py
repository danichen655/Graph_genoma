from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from .docker.utils import *
from .static.py.utils import *
import base64
import pandas as pd
import os
import json
import stat
import shutil
import zipfile

# Página inicial
def index(request):
    return render(request, 'index.html')

# Página que se muestra al subir archivos
def upload_file(request):
    limpiezaOuputsAnteriores()
    uploaded_file = "default"
    metadatos = False
    if request.method == 'POST':
        for key in list(request.FILES.keys()):
            if key =='dna': 
                limpiezaDocker()
                numFiles = upload_fasta(request)
            if key =='metadata':
                metadatos = True
                upload_metadata(request)
            if key == "graphGenome":
                limpiezaDocker()
                numFiles = upload_descargas(request)

    if (not metadatos):
        with open('graph_genome\\static\\outputs\\metadatos.csv', 'w') as file:
            file.write('gen,start,end,id,locus_tag,type\n')
    arrSwitch = [True]*numFiles
    context = cargar_grafo(arrSwitch)
    return render(request, 'index_graph.html', context)

# Página que se muestra al seleccionar sólo las secuencias que se desean visualizar
def join_csv(request):
    path = 'graph_genome\\docker\\outputs\\csv'
    arrSwitch = json.loads(request.POST.get('arrSwitch'))
    files_list = [f for f in os.listdir(path) if f != '.gitkeep']
    frames = list()
    # Si no hay ninguno a True, pongo el primero
    if all(i==False for i in arrSwitch): arrSwitch[0] = True
    # Recorro arrSwitch, los que están a True los uno en "fasta_union.csv", los que están ahí son los que se visualizan al cargar la página
    for i in range(len(arrSwitch)):
        if arrSwitch[i]:
            df = pd.read_csv(os.path.join(path,files_list[i]))
            frames.append(df)
    pd.concat(frames).to_csv("graph_genome\\static\\outputs\\fasta_union.csv", index=False)
    context = cargar_grafo(arrSwitch)
    return render(request, 'index_graph.html', context)

# Página para descargar múltiples archivos, al lanzarlo con ajax, se ejecuta en segundo plano
def download_files(request):
    ruta = 'graph_genome/static/outputs/'
    ruta_descarga = ruta + 'GraphGenome.zip'
    # Crear un zip que contiene los archivos y los guarda en una ruta específica, para después poder descargarlos de esa ruta
    with zipfile.ZipFile(ruta_descarga, 'w') as zip_file:
        zip_file.write(ruta+'fasta_res.csv', 'fasta_res.csv')
        zip_file.write(ruta+'fasta_res.csv', 'fasta_union.csv')
        zip_file.write(ruta+'multiqc_report.html', 'multiqc_report.html')
        zip_file.write(ruta+'grafo.csv', 'grafo.csv')
        zip_file.write(ruta+'grafo.gfa', 'grafo.gfa')
    
    # Descargar el zip
    with open(ruta_descarga, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=GraphGenome.zip'
        return response