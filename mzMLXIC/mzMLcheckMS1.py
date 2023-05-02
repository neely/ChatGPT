from pyopenms import MSExperiment, MzMLFile, Precursor

def check_ms1_data(filename, output_file):
    # Load the mzML file
    exp = MSExperiment()
    MzMLFile().load(filename, exp)

    # Check if the file contains MS1 data
    has_ms1_data = False
    for spectrum in exp:
        if spectrum.getMSLevel() == 1:
            has_ms1_data = True
            break

    if has_ms1_data:
        message = f"{filename} contains MS1 data"
    else:
        message = f"{filename} does not contain MS1 data"
    
    # Write the message to the output file
    with open(output_file, 'w') as f:
        f.write(message)

    return message