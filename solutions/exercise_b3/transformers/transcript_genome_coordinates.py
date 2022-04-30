import re

class InvalidInput(Exception):
    pass

class TranscriptToGenome:
    def __init__(self):
        self.valid_cigar_regex = r'([0-9]+)([MIDNSHPX=])'

    
    def __validate_cigar(self, cigar: str):
        match = re.findall(self.valid_cigar_regex, cigar)
        if match:
            return match
        else:
            raise InvalidInput("Please provide a valid CIGAR string.")


    def __analyze_cigar(self, cigar: str, match: list):
        query_gap = 1
        input_gap = -1

        paired_coordinates = []
        current_pos = 0

        for t in match:
            if t[1] == 'M':
                for i in range(int(t[0])):
                    paired_coordinates.append(current_pos)
                    current_pos += 1
            elif t[1] == 'I':
                for i in range(int(t[0])):
                    paired_coordinates.append(input_gap)
            else:
                for i in range(int(t[0])):
                    current_pos += query_gap
        
        return paired_coordinates



    def resolve(
                self,
                gene_name: str, chromosome: str, starting_position: int,
                cigar: str, query_position: int
                ):
        match = self.__validate_cigar(cigar)
        paired_coordinates = self.__analyze_cigar(cigar, match)

        for i, coord in enumerate(paired_coordinates):
            if coord != -1:
                paired_coordinates[i] += starting_position
        
        if query_position < len(paired_coordinates):
            return paired_coordinates[query_position]

