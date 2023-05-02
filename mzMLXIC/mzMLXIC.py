import pyopenms
import numpy as np
import matplotlib.pyplot as plt
import csv

# Define the mzML filenames and m/z values
# filenames = ["example1.mzML", "example2.mzML"]
filenames = ["2022-8-29_8321_30min.mzML"]
# mz_values = [100.0, 200.0, 300.0]
mz_values = [654.84]
ppm_tolerance = 10.0

# Load the spectra from all mzML files
experiments = []
for filename in filenames:
    exp = pyopenms.MSExperiment()
    pyopenms.MzMLFile().load(filename, exp)
    experiments.append(exp)

# Define a function to calculate the m/z value of a signal
def calculate_mz(spectrum):
    precursor_mz = 0
    if spectrum.getPrecursors():
        precursor_mz = spectrum.getPrecursors()[0].getMZ()
    return precursor_mz
    isolation_window = spectrum.getPrecursors()[0].getIsolationWindowLowerOffset()
    return precursor_mz + isolation_window

# Calculate the m/z ranges
mz_ranges = [(mz * (1.0 + ppm_tolerance * 1e-6), mz * (1.0 - ppm_tolerance * 1e-6)) for mz in mz_values]

# Filter the MS1 spectra to select only signals within the specified m/z ranges
ms1_spectra = []
for exp in experiments:
    ms1_spectra += [s for s in exp.getSpectra() if s.getMSLevel() == 1]
filtered_spectra = [s for s in ms1_spectra for mz_range in mz_ranges if mz_range[0] <= calculate_mz(s) <= mz_range[1]]

# Extract the retention times and intensity values for the selected signals
rt_values = {mz: [] for mz in mz_values}
intensity_values = {mz: [] for mz in mz_values}
for spectrum in filtered_spectra:
    mz = calculate_mz(spectrum)
    if mz in mz_values:
        rt_values[mz].append(spectrum.getRT())
        intensity_values[mz].append(spectrum.getNonZeroDataArrays()[0].getY())

# Plot the stacked chromatogram
fig, ax = plt.subplots()
for i, mz in enumerate(mz_values):
    ax.fill_between(rt_values[mz], np.zeros_like(intensity_values[mz]) + i, np.full_like(intensity_values[mz], i) + intensity_values[mz], label=f"{mz} m/z")
plt.xlabel("Retention time (s)")
plt.ylabel("Intensity")
plt.title(f"MS1 signals with m/z within {mz_values[0]-ppm_tolerance}-{mz_values[-1]+ppm_tolerance} ppm of {mz_values}")
plt.legend()

# Export the plot as a PNG file
plt.savefig("ms1_intensity_plot.png", dpi=300)

# Export the data as a CSV file
header = ["retention_time"] + [f"intensity_{mz}" for mz in mz_values]
data = []
for i, rt in enumerate(rt_values[mz_values[0]]):
    row = [rt] + [intensity_values[mz][i] if i < len(intensity_values[mz]) else "" for mz in mz_values]
    data.append(row)
with open("ms1_intensity_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)
