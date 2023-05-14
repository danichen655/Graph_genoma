from Bio import SeqIO
import sys, os
import pandas as pd
import gffutils

# Script para transformar gff3 a csv
def gff3_to_csv(filePath, filename):
    df = pd.DataFrame(columns=['gen', 'start', 'end', 'id', 'locus_tag', 'type'])
    db = gffutils.create_db(filePath, dbfn=':memory:', force=True, keep_order=True, merge_strategy='merge')
    for row in db.all_features():
        # Seleccionamos los metadatos que nos interesan, para pasárselos al html, y que se pueda visualizar
        if "gene" in row.attributes:
            if row.attributes["gbkey"]==['Gene']:
                if "locus_tag" in row.attributes.keys(): locus_tag = row.attributes["locus_tag"][0]
                else: locus_tag = "null"
                if "Dbxref" in row.attributes.keys(): id_db_xref = row.attributes["Dbxref"][0].split(":")[1]
                else: id_db_xref = "null"

                df = pd.concat([df, pd.DataFrame.from_records([{
                    'gen': row.attributes["gene"][0],
                    'start': row.start,
                    'end': row.end,
                    'id': id_db_xref,
                    'locus_tag': locus_tag,
                    'type': row.strand
                }])],ignore_index=True)

    df.drop_duplicates(inplace=True)
    src = os.path.join("/shared/outputs/metadatos/",fileName)
    df.to_csv(src, index=False)

if __name__ == "__main__":
    filePath = sys.argv[1]
    fileName = sys.argv[2]
    gff3_to_csv(filePath, fileName)
