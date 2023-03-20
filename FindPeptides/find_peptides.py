import argparse
import csv

def parse_fasta(fasta_file):
    sequences = {}
    with open(fasta_file) as f:
        seq_id = None
        sequence = ''
        for line in f:
            if line.startswith('>'):
                if seq_id is not None:
                    sequences[seq_id] = sequence
                seq_id = line.strip()[1:]
                sequence = ''
            else:
                sequence += line.strip()
        if seq_id is not None:
            sequences[seq_id] = sequence
    return sequences

def check_peptides(peptides_file, fasta_file, output_file):
    sequences = parse_fasta(fasta_file)
    with open(peptides_file) as f, open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Peptide', 'Found', 'Entries'])
        for line in f:
            peptide = line.strip()
            found = False
            entries = ''
            for seq_id, sequence in sequences.items():
                if peptide in sequence:
                    found = True
                    if entries:
                        entries += ','
                    entries += seq_id
            writer.writerow([peptide, str(found), entries])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('peptides_file', help='path to the file containing the list of peptides')
    parser.add_argument('fasta_file', help='path to the fasta file')
    parser.add_argument('output_file', help='path to the output file')
    args = parser.parse_args()

    check_peptides(args.peptides_file, args.fasta_file, args.output_file)
