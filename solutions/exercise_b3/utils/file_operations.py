class Reader:
    """
    A class to read files and operates on them.
    """
    def __init__(self):
        pass

    def read_txt(self, txt_file: str, sep: str):
        """
        TXT reading method. Reads each line of the txt file and splits it by the separator. Expects a table formatted txt file.
        Parameters:
            txt_file: str. Description: The path to a txt file.
            sep: str. Description: The separator string used to split the txt lines.
        Output:
            A list of values per column in each txt line (row).
        """
        try:
            reads = [x.replace("\n", "").split(sep) for x in open(txt_file).readlines()]
            print(reads)
            return reads
        except Exception as e:
            if e == FileNotFoundError:
                raise FileNotFoundError
            else:
                raise e


class Writer:
    """
    A class to write files and operates on them.
    """
    def __init__(self):
        pass

    def write_output(
        self, output_list: list, output_path: str, output_file: str, sep: str
    ):
        """
        Writes the output file, one line per output result.
        Parameters:
            output_list: list. Description: List of output entries.
        """
        with open(f"{output_path}/{output_file}", "w") as out:
            for output in output_list:
                print(output)
                out.write(sep.join([str(i) for i in output]))
                out.write("\n")
            out.close()
