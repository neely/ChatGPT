**Me**
For my input.csv I would like to perform some operations on the first column only to clean up the strings. Can you help me write a new script? For instance, I would like to remove anything after a semicolon, including the semicolon, I would like to remove any " isoform" and any following characters, I would like to remove anything that ends in "-like", and I would like to remove anything that says "LOW QUALITY PROTEIN: ", and I would like to remove anything after \[ including the \[.

**ChatGPT**
Sure, you can use the re library in Python to perform these string operations. Here's a script that takes in an input file, performs these operations, and outputs the result to a new file:

```
import csv
import re

def clean_string(s):
    s = re.sub(r";.*$", "", s)
    s = re.sub(r" isoform.*$", "", s)
    s = re.sub(r"-like$", "", s)
    s = re.sub(r"LOW QUALITY PROTEIN: ", "", s)
    s = re.sub(r"\[.*$", "", s)
    return s

with open('input.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    
    for row in reader:
        row[0] = clean_string(row[0])
        writer.writerow(row)
```
This script reads the input file line by line using the csv library and applies the clean_string function to the first column of each row. The cleaned string is then written to the output file along with the second column of the input.

**Me**
Can I run this from the command line with input and output file arguments? And will this only perform operations on the first column?

**ChatGPT**
Yes, you can run this script from the command line with input and output file arguments. Here's an updated version of the script that takes in the input and output file names as command line arguments:

```
import sys
import csv
import re

def clean_string(s):
    s = re.sub(r";.*$", "", s)
    s = re.sub(r" isoform.*$", "", s)
    s = re.sub(r"-like$", "", s)
    s = re.sub(r"LOW QUALITY PROTEIN: ", "", s)
    s = re.sub(r"\[.*$", "", s)
    return s

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)
    
    for row in reader:
        row[0] = clean_string(row[0])
        writer.writerow(row)
```
This script only performs operations on the first column of the input file and writes the cleaned string and second column to the output file. To run the script, you can call it from the command line like this:

```
python clean_strings.py input.csv output.csv
```

**Me**
Actually I realized removing things after the \[ will cause issues, so please remove this.

**ChatGPT**
Sure! Here's an updated version of the script that does not remove anything after a [:

```
import sys
import csv
import re

def clean_string(s):
    s = re.sub(r";.*$", "", s)
    s = re.sub(r" isoform.*$", "", s)
    s = re.sub(r"-like$", "", s)
    s = re.sub(r"LOW QUALITY PROTEIN: ", "", s)
    return s

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)
    
    for row in reader:
        row[0] = clean_string(row[0])
        writer.writerow(row)
```

This script will only perform operations on the first column of the input file and writes the cleaned string and second column to the output file. To run the script, you can call it from the command line like this:

```
python clean_strings.py input.csv output.csv
```

**Me**
Some of these lines end in spaces after characters, can you remove those?

**ChatGPT**
Of course! You can modify the clean_string function to remove the trailing spaces after characters as well. Here's the updated function:

```
def clean_string(s):
    s = re.sub(r";.*$", "", s)
    s = re.sub(r" isoform.*$", "", s)
    s = re.sub(r"-like$", "", s)
    s = re.sub(r"LOW QUALITY PROTEIN: ", "", s)
    s = s.rstrip()
    return s
```

And here's the entire script with the updated function:

```
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
```