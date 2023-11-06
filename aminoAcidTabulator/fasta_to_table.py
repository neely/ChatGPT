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

if len(sys.argv) != 3:
    print("Usage: python fasta_to_table.py input.fasta output_table.csv")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

data = []
current_sequence = ""
current_id = ""

# Read the input FASTA file
with open(input_filename, "r") as input_file:
    for line in input_file:
        if line.startswith(">"):
            # A new entry starts
            if current_id:
                # Process the previous entry
                amino_acid_counts = count_amino_acids(current_sequence)
                data.append([current_id] + list(amino_acid_counts.values()))
            current_id = line.strip()[1:]
            current_sequence = ""
        else:
            current_sequence += line.strip()

# Process the last entry
if current_id and current_sequence:
    amino_acid_counts = count_amino_acids(current_sequence)
    data.append([current_id] + list(amino_acid_counts.values()))

# Write the data to the output CSV file
with open(output_filename, "w", newline='') as output_file:
    writer = csv.writer(output_file)
    header = ["ID"] + list(amino_acid_counts.keys())  # Use the keys from the last entry
    writer.writerow(header)
    writer.writerows(data)

print(f"Processed {len(data)} sequences. Output saved to {output_filename}")
