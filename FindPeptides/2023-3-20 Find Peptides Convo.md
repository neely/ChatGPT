*Note: This conversation was based on a need to take a list of peptides and determine if they were present in a specific fasta. There is a pdf certificate of analysis for [NIST RM 8321][https://shop.nist.gov/ccrz__ProductDetails?sku=8321&cclcl=en_US) that has a list of 439 peptides it contains. Since this material was created more than a few years ago, I wanted check to see that my human fasta had these sequences. For example purposes I have included the RM 8321 pdf, the input text file of 439 peptides, the UniProt human canonical "proteome" fasta, the script and the output csv.*


**Me**
I have a list of short (less than 50 amino acid long) peptide sequences and I want to determine if they are present in a fasta. Since a fasta has line breaks, this would need to be accounted for. Also, it would be nice if this was a command line operation in windows that could take in the list of peptides (text document where each row is a peptide) and the fasta and output whether each peptide was present. Can you help?

**ChatGPT**
Yes, I can help. Here's an example Python script that should do what you need:

python
```
import argparse

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

def check_peptides(peptides_file, fasta_file):
    sequences = parse_fasta(fasta_file)
    with open(peptides_file) as f:
        for line in f:
            peptide = line.strip()
            found = False
            for seq_id, sequence in sequences.items():
                if peptide in sequence:
                    found = True
                    print(f'{peptide} found in {seq_id}')
            if not found:
                print(f'{peptide} not found in any sequence')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('peptides_file', help='path to the file containing the list of peptides')
    parser.add_argument('fasta_file', help='path to the fasta file')
    args = parser.parse_args()

    check_peptides(args.peptides_file, args.fasta_file)
```

Save this code as a .py file (e.g., find_peptides.py), and then run it from the command line with the following arguments:

```
python find_peptides.py peptides.txt sequences.fasta
```

where peptides.txt is the file containing your list of peptides (one per line) and sequences.fasta is the fasta file you want to search. The script will output whether each peptide was found in any of the sequences in the fasta file.

**Me**
No problem that you didn't use command line. Can you make this script output the results into a text file?

**ChatGPT**
Yes, we can modify the check_peptides function to write the results to a text file instead of printing them to the console. Here's the modified code:

python
```
import argparse

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
    with open(peptides_file) as f, open(output_file, 'w') as out_file:
        for line in f:
            peptide = line.strip()
            found = False
            for seq_id, sequence in sequences.items():
                if peptide in sequence:
                    found = True
                    out_file.write(f'{peptide} found in {seq_id}\n')
            if not found:
                out_file.write(f'{peptide} not found in any sequence\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('peptides_file', help='path to the file containing the list of peptides')
    parser.add_argument('fasta_file', help='path to the fasta file')
    parser.add_argument('output_file', help='path to the output file')
    args = parser.parse_args()

    check_peptides(args.peptides_file, args.fasta_file, args.output_file)
```

Save this code as a .py file (e.g., find_peptides.py), and then run it from the command line with the following arguments:

```
python find_peptides.py peptides.txt sequences.fasta output.txt
```

where peptides.txt is the file containing your list of peptides (one per line), sequences.fasta is the fasta file you want to search, and output.txt is the name of the file you want to write the results to. The script will output whether each peptide was found in any of the sequences in the fasta file and write the results to output.txt.

**Me**
actually can you output a csv with the original peptide queries in one column, one per row, then a column of true or false if they are found, and if they are found, what entry or entries contained the peptide.

**ChatGPT**
Sure! Here's the modified code that will output a CSV file with the original peptide queries in one column, one per row, then a column of "True" or "False" if they are found, and if they are found, a comma-separated list of the entries that contained the peptide:

python
```
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
```

Save this code as a .py file (e.g., find_peptides.py), and then run it from the command line with the following arguments:

```
python find_peptides.py peptides.txt sequences.fasta output.csv
```

where peptides.txt is the file containing your list of peptides (one per line), sequences.fasta is the fasta file you want to search, and output.csv is the name of the CSV file you want to write the results to. The script will output a CSV file with three columns: "Peptide", "Found", and "Entries". The "Peptide" column will contain the original peptide queries, one per row. The "Found" column will contain either "True" or "False" depending on whether the peptide was found in any of the sequences in the fasta file. The "Entries" column will contain a comma-separated list of the entries that contained the peptide, if any.