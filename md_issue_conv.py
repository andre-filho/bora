import re


def remove_md_titles(line, file):
    line = re.sub(
        '((#\s)|(##\s)|(###\s)|(####\s)|(#####\s)|(######\s))', '', line)
    return line


def md_tables_to_array(line, output_file):
    line = re.sub('(\|\ {1,3}|\ {1,3}\||)', '', line)
    line = str(line.split(' '))
    line = line.replace("\\n", '')
    output_file.write(line + '\n')
    return line


def get_all_lines(file):
    line = file.readline()
    file2 = open('xxx.txt', 'w+')
    while line:
        md_tables_to_array(line, file2)
        # remove_md_titles(line, file2)
        line = file.readline()
    file2.close()


def create_issue(title, description, acceptance_criteria):
    pass


def make_api_call(parameter_list):
    pass


if __name__ == "__main__":
    try:
        file = open('teste.md')
        get_all_lines(file)

    finally:
        file.close()
