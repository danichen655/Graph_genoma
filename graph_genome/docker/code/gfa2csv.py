import gfapy
import pandas as pd
import sys, os

def dicc_seq(file):
    seq_dict = dict()
    gfa_file = gfapy.Gfa.from_file(file)
    # Inicializamos la primera posición del diccionario
    seq_dict[gfa_file.segments[0].name] = 1
    for i in range(1,len(gfa_file.segments)):
        seq_ant_key = gfa_file.segments[i-1].name
        seq_ant_len = len(gfa_file.segments[i-1].sequence)
        seq_dict[gfa_file.segments[i].name] = seq_dict[seq_ant_key]+seq_ant_len
    return seq_dict

# Script para transformar gfa a csv
def gfa_to_csv(gfa_file_input, output_file):
    cigar_dicc = {"M":"Match", "I":"Insertion",  "D":"Deletion" , "N":"Skipped region ", "S":"Soft clipping", "H":"Hard clipping ", "P":"Padding"}
    df = pd.DataFrame(columns=['start', 'end', 'orientation', 'overlap'])
    gfa_file = gfapy.Gfa.from_file(gfa_file_input)
    dicc = dicc_seq(gfa_file_input)
    for link in gfa_file.edges:
        source_id = link.from_segment
        sink_id = link.to_segment
        overlap = cigar_dicc[str(link.overlap[0])[1]]
        from_orient = link.from_orient
        to_orient = link.to_orient

        if from_orient == "+": orientation = "+" if to_orient == "+" else "-"
        else: orientation = "-" if to_orient == "+" else "+"

        df = pd.concat([df, pd.DataFrame.from_records([{
            'start':dicc[source_id.name],
            'end': dicc[sink_id.name],
            'orientation': orientation, 
            'overlap': overlap
            }])],ignore_index=True)

    src = os.path.join("/shared/outputs/csv/",output_file)
    df.to_csv(src, index=False)

if __name__ == "__main__":
    gfa_file_input = sys.argv[1]
    output_file = sys.argv[2]
    gfa_to_csv(gfa_file_input, output_file)
