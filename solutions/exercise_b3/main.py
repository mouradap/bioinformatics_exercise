import argparse
from transformers.operator import Operator


parser = argparse.ArgumentParser()

## Arguments
parser.add_argument(
    "-i",
    "--input",
    type=str,
    help="Input one: a 4-column text file containing transcript name, chromosome, starting position, and CIGAR string mapping.",
    required=True
)
parser.add_argument(
    "-t",
    "--target",
    type=str,
    help="a 2-column text file containing the transcript name and the query transcript position.",
    required=True
)
parser.add_argument("-o", "--output", type=str, help="File path for output file.", default="output/output.txt")
parser.add_argument(
    "-sep", "--separator", type=str, help="The separator for the input files.", default="    "
)
args = parser.parse_args()

# Instantiating the main operator class.
op = Operator(
    input_file=args.input,
    target_file=args.target,
    output=args.output,
    separator=args.separator,
)
# Calling up the main resolution method.
op.get_coordinates()

# Finished running operation.
print("Output file generated.")
