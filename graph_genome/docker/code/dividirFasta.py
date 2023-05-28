import os
import sys
from Bio import SeqIO

def separate_sequences(fasta_file, output_dir):
    # Utiliza SeqIO para leer el archivo FASTA
    records = list(SeqIO.parse(fasta_file, "fasta"))

    # Guarda el nombre de la primera secuencia en un archivo
    first_sequence_name = records[0].id
    first_sequence_file = output_dir + "referencia.txt"
    with open(first_sequence_file, "w") as f:
        f.write(first_sequence_name)
    
    # Crea un archivo para cada secuencia en la ruta especificada
    for record in records:
        output_file = output_dir + f"{record.id}.fasta"
        # Escribe la secuencia en el archivo individual
        with open(output_file, "w") as f:
            SeqIO.write(record, f, "fasta")
        
        print(f"Secuencia {record.id} guardada en {output_file}")

if __name__ == "__main__":

    fasta_file = sys.argv[1]
    output_dir  = "/shared/inputs/"
    separate_sequences(fasta_file, output_dir)