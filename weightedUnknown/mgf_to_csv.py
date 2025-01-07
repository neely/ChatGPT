# Takes in an mgf and will return the abundance of each precursor fragmented.
# There are no package dependencies.
#
# Inputs:
#    input_file.mgf is the MGF file containing MS2 data.
#    output.csv is the csv file that will be written
# Writes the csv with the following columns
#    scan_number
#    pepmass
#    intensity
# 
# Run from the command line as:
# python mgf_to_csv.py input_file.mgf output_file.csv
#
# This was made with the obvious help of chatGPT and tested with msconvert mgf and mzidentlML from Mascot
# B. Neely 7 Jan 2025



import csv
import sys

def parse_mgf(mgf_file):
    """Parse MGF file manually to extract precursor information."""
    precursor_data = []

    print("Parsing MGF file...")
    with open(mgf_file, 'r') as f:
        inside_ion_block = False
        scan_number = None
        precursor_mz = None
        intensity = None

        for line in f:
            line = line.strip()

            # Identify start of an ion block
            if line == "BEGIN IONS":
                inside_ion_block = True
                scan_number = None
                precursor_mz = None
                intensity = None

            # Parse lines within the ion block
            elif inside_ion_block:
                if line.startswith("TITLE="):
                    # Extract scan number from the TITLE line
                    if "scan=" in line:
                        scan_number = line.split("scan=")[-1].strip().split()[0].strip('"')
                elif line.startswith("PEPMASS="):
                    # Extract precursor m/z and intensity from PEPMASS line
                    pepmass_values = line.split("=")[-1].strip().split()
                    precursor_mz = float(pepmass_values[0])
                    intensity = float(pepmass_values[1]) if len(pepmass_values) > 1 else 0
                elif line == "END IONS":
                    # End of ion block, store data
                    inside_ion_block = False
                    if scan_number and precursor_mz is not None:
                        precursor_data.append({
                            'scan_number': scan_number,
                            'pepmass': precursor_mz,
                            'intensity': intensity
                        })

    return precursor_data

def export_to_csv(data, output_file):
    """Export precursor data to a CSV file."""
    print(f"Exporting data to {output_file}...")
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['scan_number', 'pepmass', 'intensity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Data successfully exported to {output_file}.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python mgf_to_csv.py <input.mgf> <output.csv>")
        sys.exit(1)

    mgf_file = sys.argv[1]
    output_csv = sys.argv[2]

    precursor_data = parse_mgf(mgf_file)
    export_to_csv(precursor_data, output_csv)

if __name__ == "__main__":
    main()
