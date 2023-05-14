from Bio import SeqIO
import sys, os
import pandas as pd

# Script para transformar gb a csv
def gb_to_csv(filePath, fileName):
    df = pd.DataFrame(columns=['gen', 'start', 'end', 'id', 'locus_tag', 'type'])
    genbank_records = SeqIO.parse(open(filePath,"r"), "genbank")
    for record in genbank_records:
        for feature in record.features:
            if feature.type=="gene":
                # Seleccionamos los metadatos que nos interesan, para pasárselos al html, y que se pueda visualizar
                if "gene" in feature.qualifiers.keys():
                    for qualifier in feature.qualifiers:
                        aux_loc = str(feature.location).split("]")
                        aux_loc2 = aux_loc[0].split(":")
                        if "locus_tag" in feature.qualifiers.keys(): locus_tag = feature.qualifiers["locus_tag"][0]
                        else: locus_tag = "null"
                        if "db_xref" in feature.qualifiers.keys(): id_db_xref = feature.qualifiers["db_xref"][0].split(":")[1]
                        else: id_db_xref = "null"
                        
                        df = pd.concat([df, pd.DataFrame.from_records([{
                            'gen': feature.qualifiers["gene"][0],
                            'start': aux_loc2[0][1:],
                            'end': aux_loc2[1],
                            'id': id_db_xref,
                            'locus_tag': locus_tag,
                            'type': aux_loc[1][1],
                        }])],ignore_index=True)  
    df.drop_duplicates(inplace=True)
    src = os.path.join("/shared/outputs/metadatos/",fileName)
    df.to_csv(src, index=False)
    
if __name__ == "__main__":
    filePath = sys.argv[1]
    fileName = sys.argv[2]
    gb_to_csv(filePath,fileName)
