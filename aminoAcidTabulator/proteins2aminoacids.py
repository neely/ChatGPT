# This script will take in two input files and export a single csv. The "proteinList.txt" file
# is a text file with one column, no column header, which is a list of protein IDs. These can be
# whatever unique identifier from your protein list, but they should be unique in the companion
# fasta. Also, it can be the complete fasta header, there are no limitations, but it will not
# match if it isn't in the fasta, and if it isn't unique, it will return more than one match.
# The second file is the fasta, "input.fasta" is the fasta used when generating the protein list.
# the resulting table will be each row is a protein entry with 22 columns following with counts
# of each of the amino acids in the protein. Homocysteine is not included as it does not have a
# single letter amino acid code. If you have 442 protein IDs then your output_table.csv will have
# 442 rows in addition to the column headers. These will be in the same order as the proteinList.txt.
#
# You can change the name of the input files to whatever you have, but adjust the command 
# appropriately. If there are spaces in the file names you will need to surround them with "".
#
# To run this script from the command line, change directory to the directory containing both input files
# and then execute the script with the following command:
# python proteins2aminoacids.py proteinList.txt input.fasta output_table.csv
#
# Much help to ChatGPT 3.5 for helping B. Neely make this on 6 Nove 2023.
# This will be deposited to https://github.com/neely/ChatGPT/tree/main/aminoAcidTabulator
# but the conversation may be viewable here as well:
# https://chat.openai.com/share/ace6f28a-15d1-463c-846d-f6944d80d09e


import sys
import re
import csv

# Function to count amino acids in a sequence
def count_amino_acids(sequence):
    amino_acids = {
        "A": 0, "R": 0, "N": 0, "D": 0, "C": 0, "E": 0, "Q": 0, "G": 0,
        "H": 0, "I": 0, "L": 0, "K": 0, "M": 0, "F": 0, "P": 0, "S": 0,
        "T": 0, "W": 0, "Y": 0, "V": 0, "U": 0, "O": 0
    }

    for aa in sequence:
        if aa in amino_acids:
            amino_acids[aa] += 1

    return amino_acids

if len(sys.argv) != 4:
    print("Usage: python proteins2aminoacids.py proteinList.txt input.fasta output_table.csv")
    sys.exit(1)

protein_list_filename = sys.argv[1]
input_filename = sys.argv[2]
output_filename = sys.argv[3]

# Read the list of protein identifiers from proteinList.txt
with open(protein_list_filename, "r") as protein_list_file:
    protein_identifiers = [line.strip() for line in protein_list_file]

# Initialize a dictionary to store the protein identifiers and their corresponding amino acid counts
protein_data = {}

current_sequence = ""
current_id = ""

# Read the input FASTA file
with open(input_filename, "r") as input_file:
    for line in input_file:
        if line.startswith(">"):
            if current_id and any(identifier in current_id for identifier in protein_identifiers):
                # If the current identifier partially matches any in the list, process it
                amino_acid_counts = count_amino_acids(current_sequence)
                protein_data[current_id] = list(amino_acid_counts.values())
            current_id = line.strip()[1:]
            current_sequence = ""
        else:
            current_sequence += line.strip()

# Process the last entry
if current_id and any(identifier in current_id for identifier in protein_identifiers):
    amino_acid_counts = count_amino_acids(current_sequence)
    protein_data[current_id] = list(amino_acid_counts.values())

# Write the data to the output CSV file
with open(output_filename, "w", newline='') as output_file:
    writer = csv.writer(output_file)
    header = ["ID"] + list(protein_data[next(iter(protein_data))])
    writer.writerow(header)

    # Write the data in the order specified by the proteinList.txt
    for protein_id in protein_identifiers:
        for header, counts in protein_data.items():
            if protein_id in header:
                writer.writerow([header] + counts)

print(f"Processed {len(protein_data)} sequences. Output saved to {output_filename}")
