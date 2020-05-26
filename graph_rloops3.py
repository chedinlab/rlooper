import argparse
import re

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class RLoopGraph:
    @classmethod
    def __create_file(cls, file_type, file_name, probability, energy, start_loci, end_loci):
        plt.title(file_name)
        plt.subplot(2, 1, 1)
        plt.ylim(0, 1)
        plt.xlabel('Position (bp)')
        plt.ylabel('P(x)')
        plt.plot(range(int(start_loci), int(end_loci) + 1), probability)
        plt.subplot(2, 1, 2)
        plt.plot(range(int(start_loci), int(end_loci) + 1), energy)
        plt.xlabel('Position (bp)')
        plt.ylabel('Local Avg G(x)')
        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.25, wspace=1.8)

        if file_type == 'pdf':
            with PdfPages(file_name + '.pdf') as pdf:
                pdf.savefig()
        else:
            plt.savefig(file_name + '.png', dpi=300)

        plt.close()

    @classmethod
    def get_args(cls):
        parser = argparse.ArgumentParser(description='Plot graphs from RLoop output')
        parser.add_argument('-i1', '--input-file-probability', metavar='PROBABILITY_WIG', type=str, required=True,
                            help='Probability WIG file', default=None)
        parser.add_argument('-i2', '--input-file-energy', metavar='ENERGY_WIG', type=str, required=True,
                            help='Energy WIG file', default=None)
        parser.add_argument('-o', '--output-file-prefix', metavar='OUTPUT_PREFIX', type=str, required=False,
                            help='Output file name prefix', default='')
        parser.add_argument('-p', '--png', required=False, action='store_const',
                            help='Output file as PNG image', const='png', default='pdf')
        return parser.parse_args()

    @classmethod
    def plot(cls, probability_file, energy_file, out_filetype='pdf', out_filename_prefix=''):
        loci_pattern = re.compile(r'\d+-\d+$')
        header1_pattern = re.compile(r'^browser position')
        header2_pattern = re.compile(r'^#')
        probability = list()
        energy = list()
        seq_name = ''

        with open(probability_file, 'r') as p_file, open(energy_file, 'r') as e_file:
            # Skip first line
            p_file.readline()
            p_line = p_file.readline()
            while p_line != '':
                p_line = p_line.strip()

                if header1_pattern.match(p_line):
                    if len(probability) > 0:
                        if len(energy) < 1:
                            raise AssertionError('Energy info for ' + seq_name + ' not found')
                        cls.__create_file(out_filetype, out_filename_prefix + seq_name, probability, energy,
                                          start_loci, end_loci)

                    probability.clear()
                    energy.clear()
                    energy_found = False

                    if len(loci_pattern.findall(p_line)) != 1:
                        raise AssertionError('Cannot find loci info')

                    start_loci, end_loci = loci_pattern.findall(p_line)[0].split('-')
                    p_line = p_file.readline().strip()

                    if not header2_pattern.match(p_line):
                        raise AssertionError('Cannot find sequence name')

                    seq_name = p_line.lstrip('#')
                    # Skip one line
                    p_file.readline()
                    p_line = p_file.readline().strip()
                    e_line = e_file.readline()

                    while e_line != '':
                        e_line = e_line.strip()

                        if energy_found:
                            try:
                                energy.append(float(e_line))
                            except ValueError:
                                energy_found = False
                                break
                        elif e_line.lstrip('#') == seq_name:
                            energy_found = True
                            # Skip one line
                            e_file.readline()

                        e_line = e_file.readline()

                probability.append(float(p_line))
                p_line = p_file.readline()

        if len(probability) > 0:
            if len(energy) < 1:
                raise AssertionError('Energy info for ' + seq_name + ' not found')
            cls.__create_file(out_filetype, out_filename_prefix + seq_name, probability, energy, start_loci,
                              end_loci)


if __name__ == '__main__':
    args = vars(RLoopGraph.get_args())
    RLoopGraph.plot(args.get('input_file_probability'), args.get('input_file_energy'),
                    args.get('png', 'pdf'), args.get('output_file_prefix', ''))
