import sys, os
from Bio import SeqIO
import pandas as pd

# Script para transformar fastas a csv
def fasta_to_csv(filePath, fileName):
    df = pd.DataFrame()
    for registro in SeqIO.parse(filePath, "fasta"):
        identificador = registro.id
        secuencia = registro.seq

        for num, nucleotido in enumerate(secuencia, 1):
            if nucleotido!="-":
                nueva_fila = {'base': nucleotido, 'start': num, 'row': identificador, 'y_value': 1}
                df = pd.concat([df, pd.DataFrame.from_records([nueva_fila])], ignore_index=True)

    df['start'] = df['start'].astype(int)
    df['y_value'] = df['y_value'].astype(int)
    src = os.path.join("/shared/outputs/csv/",fileName)
    df.to_csv(src, index=False)

if __name__ == "__main__":
    filePath = sys.argv[1]
    fileName = sys.argv[2]
    fasta_to_csv(filePath, fileName)
