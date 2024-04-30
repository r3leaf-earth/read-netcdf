import sys

infile_original_try = sys.argv[1]


def is_part_of_header(line):
    return line[0].isalpha() or line[0].isspace() or line[0] == "*"


data = []

# parse file for temperatures only
with open(infile_original_try, 'r') as try_file:
    for line in try_file:

        # if line starts wiht letter or whitespace --> skip, because header
        if line and is_part_of_header(line):
            pass
        else:
            row = line.split()
            data.append(row)

print(data[0:5])
            

