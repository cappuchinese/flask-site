"""module to read fasta file imported from site"""

__author__ = "Lisa Hu"
__version__ = "03.2021"

from io import BytesIO
import base64
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")


class FastaRead:
    """
    class reads fasta file and returns all the data
    """
    file_ = None
    all_results = None
    reading_frame = None

    def __init__(self, file_, reading_frame):
        self.file_ = file_
        self.all_results = {}
        self.headers = []
        self.reading_frame = reading_frame

    def get_headers(self):
        """
        function makes list of headers
        :return: list of headers in file
        """
        with open(self.file_) as opened_file:  # open file
            for line in opened_file:  # loop through file
                line = line.strip()
                if line.startswith(">"):
                    self.headers.append(line)  # add header to list

        return self.headers

    def get_results(self):
        """
        execute functions to make the results for each header
        :return: dict with header as key and results as value
        """
        fasta = self.file_reading()

        for header in fasta:  # loop through dict
            results = {}
            seq = fasta[header]  # get sequence of each header
            if self.nuc_check(seq):  # check if it's a DNA sequence
                codon_dict = self.codon_maker(seq)  # make codons
                protein_seq = self.protein_sequencer(codon_dict)  # make protein sequence

                results["percentage"] = self.percentage_calc(seq)  # get percentages, add to dict
                results["aa_count"] = self.aa_counter(protein_seq)  # get aa amounts, add to dict
                results["protein"] = self.format_protein(header, protein_seq)  # format, add to dict

                # add all the results to dict with respective header
                self.all_results[header] = results
            else:
                return None

        return self.all_results

    def file_reading(self):
        """
        reads file and splits header and sequence
        :return: dict with header as key and sequence as value
        """
        fasta = {}
        seq = ""

        with open(self.file_) as opened_file:
            for line in opened_file:
                line = line.strip()
                if line.startswith(">"):
                    if seq != "":
                        fasta[header] = seq
                        seq = ""
                    header = line
                else:
                    seq += line.upper()

            fasta[header] = seq

        return fasta

    def nuc_check(self, seq):
        """
        check if the file is a nucleotide sequence
        :param seq: sequence from file
        :return: boolean
        """
        for nuc in seq:
            if nuc not in "ACTGNRYKMSWBDHV":  # letters after G are ambiguous nucleotides
                return False
        return True

    def percentage_calc(self, seq):
        """
        makes dictionary of nucleotide percentages
        :param seq: sequence from file
        :return: dictionary with percentages of respective nucleotide
        """
        total = len(seq)
        # count the amount of each nucleotide and divide by total
        perc_dict = {"A": (seq.count("A") / total) * 100, "G": (seq.count("G") / total) * 100,
                     "C": (seq.count("C") / total) * 100, "T": (seq.count("T") / total) * 100}

        ambiguous_perc = 100 - sum(perc_dict.values())  # percentage of ambiguous nucleotides
        perc_dict["ambiguous"] = ambiguous_perc

        return perc_dict

    def codon_maker(self, seq):
        """
        framing the sequence in codons, adding to a list
        :param seq: sequence from file
        :return: list of codons
        """
        codon_list = []

        if self.reading_frame == "frame1":
            for startpos in range(0, len(seq), 3):  # step through it in steps of 3 (codonlength=3)
                codon = seq[startpos:startpos + 3]
                # slicing the sequence for codon
                if len(codon) == 3:  # only adds codon if the codonlength = 3 (due to framing)
                    codon_list.append(codon)

        # repetitive code from here, only difference is the start position
        elif self.reading_frame == "frame2":  # offset=1
            for startpos in range(1, len(seq), 3):
                codon = seq[startpos:startpos + 3]
                if len(codon) == 3:
                    codon_list.append(codon)

        elif self.reading_frame == "frame3":  # offset=2
            for startpos in range(2, len(seq), 3):
                codon = seq[startpos:startpos + 3]
                if len(codon) == 3:
                    codon_list.append(codon)

        elif self.reading_frame == "frame4":  # reverse offset=2
            for startpos in range(len(seq) - 3, 0, -3):
                codon = seq[startpos] + seq[startpos - 1] + seq[startpos - 2]
                if len(codon) == 3:
                    codon_list.append(codon)

        elif self.reading_frame == "frame5":  # reverse offset=1
            for startpos in range(len(seq) - 2, 0, -3):
                codon = seq[startpos] + seq[startpos - 1] + seq[startpos - 2]
                if len(codon) == 3:
                    codon_list.append(codon)

        elif self.reading_frame == "frame6":  # reverse offset=0
            for startpos in range(len(seq) - 1, 0, -3):
                codon = seq[startpos] + seq[startpos - 1] + seq[startpos - 2]
                if len(codon) == 3:
                    codon_list.append(codon)
        # end repetition code

        return codon_list

    def protein_sequencer(self, codon_list):
        """
        translate all the codons to amino acid
        :param codon_list: codons from sequence
        :return: string with protein letters
        """
        protein_seq = ""
        codon_to_amino = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
            'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W'}

        for codon in codon_list:
            if codon in codon_to_amino:
                protein = codon_to_amino[codon]  # translate to protein letter
                protein_seq += protein  # add to string
            else:  # codon contains ambiguous nucleotide, adds X as protein
                protein_seq += "X"

        return protein_seq

    def aa_counter(self, protein_seq):
        """
        counts the amount of each amino acid in the protein sequence
        :param protein_seq: protein sequence
        :return: dictionary of amount of respective amino acid
        """
        count_dict = {}
        for amino in protein_seq:
            if amino not in count_dict:
                count_dict[amino] = 1
            else:
                count_dict[amino] += 1

        return count_dict

    def format_protein(self, header, protein_seq):
        """
        format the protein sequence into lines of 70 and return the header of fasta file
        :param header: header of fasta
        :param protein_seq: protein sequence
        :return: string with newlines every 70 characters
        """
        formatted = header + "\n"
        # step through it in steps of 70 (linelength=70)
        for startpos in range(0, len(protein_seq), 70):
            formatted += protein_seq[startpos:startpos + 70] + "\n"  # add a newline every 70 chars

        return formatted


class DataModel:
    """
    class makes images to show data
    """
    pie_chart = None
    bar_chart = None

    def __init__(self, key, result):
        self.key = key
        self.result = result

    def create_web_plot(self, fig):
        """
        converts figure into base64 encoded png
        :param fig: figure created by plt
        :return: png image
        """
        figfile = BytesIO()
        fig.savefig(figfile, format="png")
        figfile.seek(0)
        website_png = base64.b64encode(figfile.getvalue()).decode('ascii')

        return website_png

    def pie_plot(self):
        """
        make pie chart with plt
        :return: image of pie chart
        """
        # set variables
        sizes = []
        labels = []

        for key, value in self.result.items():
            sizes.append(value)  # size of each slice
            labels.append(key)  # label of each slice

        fig, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct="%.1f%%")
        ax1.axis("equal")

        return self.create_web_plot(fig)

    def bar_plot(self):
        """
        make bar chart with plt
        :return: image of bar chart
        """
        labels = self.result.keys()  # labels of bar
        aa_values = self.result.values()  # size of bar

        label_loc = np.arange(len(labels))  # location for the labels

        fig, ax = plt.subplots()
        rects = ax.bar(label_loc, aa_values, 0.7)

        plt.figure(1)
        ax.set_ylabel("Amount")
        ax.set_xlabel("Amino acids")
        ax.set_xticks(label_loc)
        ax.set_xticklabels(labels)

        # adding the numbers to each bar
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height}", xy=((rect.get_x() + rect.get_width()), height), xytext=(0, 3),
                        textcoords="offset points", ha="right", va="bottom",
                        fontsize=9, rotation=90)

        return self.create_web_plot(fig)
