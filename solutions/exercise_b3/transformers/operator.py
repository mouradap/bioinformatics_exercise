from utils.file_operations import Reader, Writer
from transformers.transcript_genome_coordinates import TranscriptToGenome


class InputError(Exception):
    pass


class Operator:
    """
    Main operator for the solution. Uses all of the submodules to generate the output file.
    Parameters:
        input_file: str. Description: File path for the input file.
        target_file: str. Description: File path for the target file.
        output: str. Description: File path for the output file.
        separator: str. Description: The separator used for input files.
    """

    def __init__(self, input_file: str, target_file: str, output: str, separator: str):
        self.reader = Reader()
        self.writer = Writer()
        self.resolver = TranscriptToGenome()
        self.separator = separator
        self.input = self.reader.read_txt(input_file, sep=separator)
        self.target = self.reader.read_txt(target_file, sep=separator)
        self.__validate_input_target()
        self.output_path = "/".join(output.split("/")[:-1])
        self.output_file = output.split("/")[-1]
        
    def __validate_input_target(self):
        """
        Validates the input. Throws InputError exceptions in the case when the input is missing any of the required columns.
        Parameters: None.
        """
        for i in self.input:
            if len(i) < 4:
                raise InputError("Please provide a valid input file!")

        for i in self.target:
            if len(i) < 2:
                raise InputError("Please provide a valid target file!")

    def __construct_output(
        self,
        transcript_name: str,
        chromosome: str,
        starting_position: int,
        cigar: str,
        query_position: int,
    ):
        """
        Constructs the output for each query target in the target input file.
        Parameters:
            transcript_name: str. Description: The name of the transcript for reference between both input files.
            chromosome: str. Description: Chromosome name.
            starting_position: int. The starting position matching the first nucleotide of the transcript to its current genomic coordinate.
            cigar: str. Description: A CIGAR string containing the matching information between transcript and the reference genome.
            query_position: int. Description: The query position of the transcript to return its genomic coordinate.
        """
        mapped_chromosome_position = self.resolver.resolve(
            starting_position=starting_position,
            cigar=cigar,
            query_position=query_position,
        )
        resolve = [
            transcript_name,
            query_position,
            chromosome,
            mapped_chromosome_position,
        ]

        return resolve

    def get_coordinates(self):
        """
        This is the main function of the operator. It calculates the genomic coordinates for all of the query targets, and writes the output to file.
        Parameters: None.
        """
        output_list = []

        for row in self.target:
            target_gene, query_position = row

            if target_gene not in [inpt[0] for inpt in self.input]:
                return -1

            else:
                target_input_lines = [
                    inpt for inpt in self.input if inpt[0] == target_gene
                ]

                if len(target_input_lines) > 1:
                    raise InputError(
                        "Please provide only one entry per transcript in the input file."
                    )
                else:
                    target_input = target_input_lines[0]

                output = self.__construct_output(
                    transcript_name=target_gene,
                    chromosome=target_input[1],
                    starting_position=int(target_input[2]),
                    cigar=target_input[3],
                    query_position=int(query_position),
                )
                output_list.append(output)

        self.writer.write_output(
            output_list, self.output_path, self.output_file, self.separator
        )
