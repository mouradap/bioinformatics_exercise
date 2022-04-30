import re


class InvalidInput(Exception):
    pass


class TranscriptToGenome:
    """
    Main logic algorithm. Compares the transcript coordinates with genomic coordinates based on CIGAR string.
    """

    def __init__(self):
        # Regex to validate CIGAR strings.
        self.valid_cigar_regex = r"([0-9]+)([MIDNSHPX=])"

    def __validate_cigar(self, cigar: str):
        """
        Method to validate the CIGAR string using regex.
        Parameters:
            cigar: str. Description: A valid CIGAR string.
        """
        match = re.findall(self.valid_cigar_regex, cigar)
        if match:
            return match
        else:
            raise InvalidInput("Please provide a valid CIGAR string.")

    def __analyze_cigar(self, match: list):
        """
        Main coordinate method. A simple string comparison algorithm for CIGAR strings. Outputs the offset between the reference genome and target position.
        Parameters:
            match: list. Description: A list of tuples extracted from a valid CIGAR string.
        """
        query_gap = 1

        paired_coordinates = []
        current_pos = 0

        for t in match:
            if t[1] == "M":
                for i in range(int(t[0])):
                    paired_coordinates.append(current_pos)
                    current_pos += 1
            elif t[1] == "I":
                insert_gap = 1
                for i in range(int(t[0])):
                    paired_coordinates.append(f"{current_pos-1}+{insert_gap}")
                    insert_gap += 1
            else:
                for i in range(int(t[0])):
                    current_pos += query_gap

        return paired_coordinates

    def resolve(self, starting_position: int, cigar: str, query_position: int):
        """
        The class' main method. Returns the genomic position of the queried transcript position.
        Parameters:
            starting_position: int. The starting position matching the first nucleotide of the transcript to its current genomic coordinate.
            cigar: str. Description: A CIGAR string containing the matching information between transcript and the reference genome.
            query_position: int. Description: The query position of the transcript to return its genomic coordinate.
        """
        match = self.__validate_cigar(cigar)
        paired_coordinates = self.__analyze_cigar(match)

        for i, coord in enumerate(paired_coordinates):
            if isinstance(coord, int):
                paired_coordinates[i] += starting_position
            else:
                transcript_coord = paired_coordinates[i].split('+')
                genomic_coord = int(transcript_coord[0]) + starting_position
                paired_coordinates[i] = f"{genomic_coord}+{transcript_coord[1]}"

        if query_position < len(paired_coordinates):
            return paired_coordinates[query_position]
