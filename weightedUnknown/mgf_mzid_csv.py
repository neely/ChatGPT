# Takes in an mgf and mzIdentML from the same DDA run, and will generate a table
# where each row is an MSMS, including intensity of the precursor, and whether
# the spectra was identied(based on the threshold specified in mzIdentML).
# There are no package dependencies.
#
# It parses the MGF and mzID files separately.
# It matches the scan numbers between both files.
# It combines the scan number, pepmass, intensity, and pass threshold into one CSV file.

# Inputs:
#    input.mgf is the MGF file containing MS2 data.
#    input.mzid is the mzIdentML file containing identification results.
#    output.csv is the csv file that will be written
# Writes the csv with the following columns
#    scan_number
#    pepmass
#    intensity
#    pass threshold
# 
# Run from the command line as:
# python mgf_mzid_csv.py input.mgf input.mzid output.csv
#
# This was made with the obvious help of chatGPT and tested with msconvert mgf and mzidentlML from Mascot
# B. Neely 7 Jan 2025

import csv
import sys
import xml.etree.ElementTree as ET


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


def parse_mzid_with_scans(mzid_file):
    """
    Parse mzIdentML file to extract scan numbers and their passThreshold status.
    Returns a list of tuples (scan_number, pass_threshold).
    """
    data = []
    namespace = {'ns': 'http://psidev.info/psi/pi/mzIdentML/1.1'}

    print("Parsing mzIdentML file...")
    tree = ET.parse(mzid_file)
    root = tree.getroot()

    for sir in root.findall('.//ns:SpectrumIdentificationResult', namespace):
        # Extract scan number from "spectrum title"
        scan_number = None
        spectrum_title = sir.find('./ns:cvParam[@name="spectrum title"]', namespace)
        if spectrum_title is not None:
            value = spectrum_title.attrib.get('value', '')
            if 'scan=' in value:
                try:
                    # Extract scan number and remove any quotes or unwanted characters
                    scan_number = value.split('scan=')[1].split('&quot;')[0].strip().replace('"', '')
                except IndexError:
                    scan_number = "Unknown"

        # Determine passThreshold status
        pass_threshold = False
        sii = sir.find('./ns:SpectrumIdentificationItem[@passThreshold="true"]', namespace)
        if sii is not None:
            pass_threshold = True

        if scan_number is not None:
            data.append((scan_number, pass_threshold))

    return data


def merge_data(mgf_data, mzid_data):
    """
    Merges MGF and mzID data on the scan number.
    Assumes both data lists are sorted by scan_number.
    """
    merged_data = []

    # Create dictionaries for faster lookup
    mzid_dict = {scan_number: pass_threshold for scan_number, pass_threshold in mzid_data}

    for mgf_entry in mgf_data:
        scan_number = mgf_entry['scan_number']
        pass_threshold = mzid_dict.get(scan_number, False)
        merged_data.append({
            'scan_number': scan_number,
            'pepmass': mgf_entry['pepmass'],
            'intensity': mgf_entry['intensity'],
            'pass_threshold': pass_threshold
        })

    return merged_data


def export_to_csv(data, output_file):
    """Export merged data to a CSV file."""
    print(f"Exporting data to {output_file}...")
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['scan_number', 'pepmass', 'intensity', 'pass_threshold']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Data successfully exported to {output_file}.")


def main():
    if len(sys.argv) != 4:
        print("Usage: python mgf_mzid_csv.py <input.mgf> <input.mzid> <output.csv>")
        sys.exit(1)

    mgf_file = sys.argv[1]
    mzid_file = sys.argv[2]
    output_csv = sys.argv[3]

    # Parse MGF and mzID files
    mgf_data = parse_mgf(mgf_file)
    mzid_data = parse_mzid_with_scans(mzid_file)

    # Merge data from MGF and mzID
    merged_data = merge_data(mgf_data, mzid_data)

    # Export merged data to CSV
    export_to_csv(merged_data, output_csv)


if __name__ == "__main__":
    main()
