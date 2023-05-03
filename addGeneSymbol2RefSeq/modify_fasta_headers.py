# To use run "python modify_fasta_headers.py input.fasta input.tsv output.fasta" from command line. Replace input.fasta, input.tsv, and output.fasta with the actual file paths for your input and output files. input.tsv is a feature table tab delimited .txt file. See https://github.com/neely/ChatGPT repo for details.

import sys

# Read in the input files
fasta_file = sys.argv[1]
tsv_file = sys.argv[2]

# Create a dictionary to map accession numbers to symbols
accession_to_symbol = {}
with open(tsv_file) as tsv:
    # Read the header row and get the index of the product_accession and symbol columns
    header = tsv.readline().rstrip().split('\t')
    product_accession_index = header.index('product_accession')
    symbol_index = header.index('symbol')
    # Iterate through the remaining rows and populate the dictionary
    for line in tsv:
        row = line.rstrip().split('\t')
        accession = row[product_accession_index]
        symbol = row[symbol_index]
        if symbol:
            accession_to_symbol[accession] = symbol

# Process the FASTA file and write the modified headers to a new file
with open(fasta_file) as fasta, open(sys.argv[3], 'w') as output:
    accession = None
    symbol = None
    for line in fasta:
        if line.startswith('>'):  # header line
            header = line.rstrip()
            accession = header.split()[0][1:]
            if accession in accession_to_symbol:
                symbol = accession_to_symbol[accession]
                header += f' GN={symbol}'
            output.write(header + '\n')
        else:  # sequence line
            output.write(line)
