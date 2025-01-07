# Takes in an mgf and mzIdentML from the same DDA run, and will return the abundance 
# of precursors that were identified (based on the threshold specified in mzIdentML)
# relative to the abundance of precursors that were unidentified.
# There are no package dependencies.
#
# Inputs:
#    input.mgf is the MGF file containing MS2 data.
#    input.mzid is the mzIdentML file containing identification results.
#    output.txt is the text file where the statistics will be written.
# Writes the final statistics to a text file, including:
#    Total MS2 scans
#    Number and percentage of identified MS2 scans
#    Total precursor intensity
#    Identified precursor intensity and percentage
# 
# Run from the command line as:
# python mgf_mzid_statistics.py input.mgf input.mzid output.txt
#
# This was made with the obvious help of chatGPT and tested with msconvert mgf and mzidentlML from Mascot
# B. Neely 7 Jan 2025

import sys
import xml.etree.ElementTree as ET
import csv

def parse_mgf(mgf_file):
    """
    Parse MGF file to extract MS2 scan data (scan number, m/z, intensity).
    Returns a list of tuples (scan_number, intensity).
    """
    mgf_data = []
    print("Parsing MGF file...")
    with open(mgf_file, 'r') as f:
        lines = f.readlines()

    scan_number = None
    intensity = None
    for line in lines:
        line = line.strip()
        if line.startswith('BEGIN IONS'):
            scan_number = None
            intensity = None
        elif line.startswith('TITLE='):
            # Extract scan number from TITLE line
            parts = line.split('scan=')
            if len(parts) > 1:
                scan_number = parts[1].split(' ')[0].strip().replace('"', '')
        elif line.startswith('PEPMASS='):
            # Extract intensity (second number in PEPMASS)
            parts = line.split(' ')
            if len(parts) > 1:
                intensity = float(parts[1])
        elif line == 'END IONS':
            if scan_number is not None and intensity is not None:
                mgf_data.append((scan_number, intensity))

    return mgf_data


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


def calculate_statistics(mgf_data, mzid_data):
    """
    Calculate statistics on identified MS2 scans and precursor intensities.
    """
    # Create dictionaries for easier lookup
    mzid_dict = {scan: pass_threshold for scan, pass_threshold in mzid_data}

    total_scans = len(mgf_data)
    identified_scans = 0
    total_intensity = 0
    identified_intensity = 0

    # Loop through MGF data and check against mzIdentML data
    for scan, intensity in mgf_data:
        total_intensity += intensity
        if scan in mzid_dict and mzid_dict[scan]:  # Check if scan is identified and passes threshold
            identified_scans += 1
            identified_intensity += intensity

    percent_identified = (identified_scans / total_scans) * 100 if total_scans > 0 else 0
    intensity_identified_percent = (identified_intensity / total_intensity) * 100 if total_intensity > 0 else 0

    return total_scans, identified_scans, percent_identified, total_intensity, identified_intensity, intensity_identified_percent


def main():
    if len(sys.argv) != 4:
        print("Usage: python mgf_mzid_statistics.py <input.mgf> <input.mzid> <output.txt>")
        sys.exit(1)

    mgf_file = sys.argv[1]
    mzid_file = sys.argv[2]
    output_file = sys.argv[3]

    # Parse the MGF and mzIdentML files
    mgf_data = parse_mgf(mgf_file)
    mzid_data = parse_mzid_with_scans(mzid_file)

    # Calculate statistics
    total_scans, identified_scans, percent_identified, total_intensity, identified_intensity, intensity_identified_percent = calculate_statistics(mgf_data, mzid_data)

    # Write results to the output text file
    with open(output_file, 'w') as f:
        f.write(f"Total MS2 scans: {total_scans}\n")
        f.write(f"Identified MS2 scans: {identified_scans} ({percent_identified:.2f}%)\n")
        f.write(f"Total precursor intensity: {total_intensity:.2f}\n")
        f.write(f"Identified precursor intensity: {identified_intensity:.2f} ({intensity_identified_percent:.2f}%)\n")

    print(f"Statistics written to {output_file}.")


if __name__ == "__main__":
    main()
