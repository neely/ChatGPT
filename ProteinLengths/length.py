import numpy as np
import matplotlib.pyplot as plt

def read_fasta(file):
    """
    Read a FASTA file and return a dictionary where the keys are the names of the sequences and the values are the sequences themselves
    """
    sequences = {}
    name = None
    seq = ""
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    sequences[name] = seq
                name = line[1:]
                seq = ""
            else:
                seq += line
    if name:
        sequences[name] = seq
    return sequences

def plot_histogram(sequences, filename, bin_size=2):
    """
    Plot a histogram of the amino acid lengths of the sequences in the given dictionary and save it as png file
    """
    lengths = [len(seq) for seq in sequences.values()]
    #xmin, xmax = min(lengths), max(lengths)
    xmin, xmax = 0, 100
    bins = np.arange(xmin, xmax + bin_size, bin_size)
    plt.hist(lengths, bins=bins)
    plt.xlabel("Amino acid length")
    plt.ylabel("Frequency")
    plt.title("Histogram of amino acid lengths")
    plt.savefig(filename)

#Read your fasta file
sequences = read_fasta("UP000005640_9606.fasta")

# plot the histogram
plot_histogram(sequences, 'histogram.png', bin_size=2)