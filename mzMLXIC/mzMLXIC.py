import struct
import numpy as np
import re

def parse_spectrum(spectrum_xml):
    spectrum_dict = {}
    for line in spectrum_xml.splitlines():
        if line.startswith('<cvParam'):
            key_value = line.split('value="')[1].split('"')[0]
            if key_value.isnumeric():
                key_value = float(key_value)
            spectrum_dict[line.split('name="')[1].split('"')[0]] = key_value
    return spectrum_dict

import struct

def parse_mzml(filename):
    with open(filename, 'rb') as f:
        binary_data = f.read()

    # Find spectrum indexes
    index_list = [m.start() for m in re.finditer(b'</spectrum>', binary_data)]

    # Parse header to get binary offset to spectrum data
    binary_offset = struct.unpack('<i', binary_data[48:52])[0]

    # Initialize empty dictionary to store parsed spectrum data
    spectrum_dict = {}

    # Loop over spectrum indexes
    for idx, index in enumerate(index_list):
        start = index + 11 # skip over '</spectrum>'

        # Determine end of spectrum data
        if idx < len(index_list) - 1:
            end = index_list[idx+1] + 11 # skip over '</spectrum>'
        else:
            end = len(binary_data)

        # Extract spectrum header
        spectrum_header = binary_data[index:start]
        spectrum_id = re.search(b'id="([0-9]+)"', spectrum_header).group(1)

        # Calculate index and count of spectrum data
        spectrum_offset = struct.unpack('<i', spectrum_header[spectrum_header.index(b'binaryDataArray') + 19:spectrum_header.index(b'" />')])[0]
        spectrum_length = end - start

        # Add index and count to spectrum dictionary
        spectrum_dict[spectrum_id] = {'index': binary_offset + spectrum_offset, 'count': spectrum_length}

    return spectrum_dict


def read_spectrum_data(binary_data, offset, count):
    # Extract binary data
    spectrum_data = binary_data[offset:offset+count]

    # Unpack binary data into mz and intensity arrays
    n_data_points = count // 8 # 8 bytes per data point (4 bytes per float)
    data_format = '<' + 'f' * n_data_points * 2 # 'f' for float
    mz, intensity = struct.unpack(data_format, spectrum_data)

    return mz, intensity


def get_chromatogram(filename, mz, ppm_tolerance):
    spectrum_dict = parse_mzml(filename)
    chromatogram = []

    for spectrum_id, spectrum_data in spectrum_dict.items():
        mz_values, intensity_values = read_spectrum_data(binary_data, spectrum_data['index'], spectrum_data['count'])

        # Calculate the closest m/z value in the spectrum to the target m/z
        closest_mz_index = abs(mz_values - mz).argmin()
        closest_mz = mz_values[closest_mz_index]

        # Calculate the ppm difference between the target m/z and the closest m/z in the spectrum
        ppm_difference = abs((closest_mz - mz) / mz) * 1e6

        # If the ppm difference is within the tolerance, add the spectrum to the chromatogram
        if ppm_difference <= ppm_tolerance:
            chromatogram.append(intensity_values)

    return sum(chromatogram, []) # flatten list of arrays into a single array

# Define the mzML filenames and m/z values
mzml_files = ['2022-8-29_8321_30min.mzML']
mz_values = [648.5]

# Define the ppm tolerance
ppm_tolerance = 10

# Initialize the output array
output_array = np.zeros((len(mz_values), 0))

# Loop over the mzML files and extract the chromatogram for each mz value
for i, mzml_file in enumerate(mzml_files):
    chromatograms = []
    for mz in mz_values:
        chromatogram = get_chromatogram(mzml_file, mz, ppm_tolerance)
        chromatograms.append(chromatogram)
    output_array = np.concatenate((output_array, np.array(chromatograms).T), axis=1)
    
# Save the output array to a file
np.savetxt('output.txt', output_array, delimiter='\t')