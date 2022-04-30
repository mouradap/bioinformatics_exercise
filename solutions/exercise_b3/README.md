# bioinformatics_exercise
This exercise has the objective to write software that translates transcript coordinates to genomic coordinates.
My solution is based solely on the input files, and its logic is wrapped around the CIGAR strings.

## Usage:
If necessary, install Python packages by running
> pip install -r requirements.txt

Necessary files:
- Input file: a 4-column text file containing transcript name, chromosome, starting position, and CIGAR string mapping.
- Target file: a 2-column text file containing the transcript name and the query transcript position.
Optional arguments:
- Output: Path to an output file.
- Separator: A separator string used in the input and target files. Default: "    "

Run main command with necessary and optional arguments.
> python main.py -i input/input.txt -t input/target.txt -o output/output.txt -sep "    "

## Assumptions:
This script assumes you provide only one entry per transcript name in the input file.
The target file can have multiple queries for the transcript position.
A valid CIGAR string is necessary, and the script tests their validity via regex.

## Setbacks:
This script repeats is CIGAR operations for each query of the target transcript, taking O(N*(T*P)) processing time, where N is the number of distinct transcripts in the target file, T is the number of which each transcript is queried, and P is the CIGAR processing time.
Space-wise, this script stores and writes O(N).

## Further improvement:
As the necessity grows, this logic can be implemented using a databases to store each transcript CIGAR chromosome mapping, reducing the processing time of the query to a select in the database.