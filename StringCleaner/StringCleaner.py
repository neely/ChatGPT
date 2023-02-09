# python clean_strings.py input.csv output.csv

import sys
import csv
import re

def clean_string(s):
    s = re.sub(r";.*$", "", s)
    s = re.sub(r" isoform.*$", "", s)
    s = re.sub(r"-like$", "", s)
    s = re.sub(r"LOW QUALITY PROTEIN: ", "", s)
    s = s.rstrip()
    return s

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)
    
    for row in reader:
        row[0] = clean_string(row[0])
        writer.writerow(row)
