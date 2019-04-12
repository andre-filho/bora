import re


def remove_md_titles(line, file):
    line = re.sub(
        '((#\s)|(##\s)|(###\s)|(####\s)|(#####\s)|(######\s))', '', line)
    return line


def md_table_row_to_array(line):
    line = re.sub('(\ \|\ )', '-', line)
    line = re.sub('(\|\ )|(\ \|)', '', line)
    line = line.replace("\\n", '')
    line = line.split('-')
    return line


def add_md_checkbox(items):
    items = items.split(';')
    a = ""
    for item in items:
        a += str('- [ ] ' + item + '\n')
    return a


def format_description(description):
    return str('**Issue description:**\n' + description + '\n')


def add_prefix_to_title(title, number, prefix='US', subid=''):
    return str(prefix + subid + str(number) + " " + title)


def get_all_lines(file):
    line = file.readline()
    lines = []
    while line:
        # md_table_row_to_array(line)
        lines.append(line)
        line = file.readline()
    return lines
