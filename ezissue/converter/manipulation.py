import re


def remove_md_titles(line):
    line = re.sub(
        r'((#\s)|(##\s)|(###\s)|(####\s)|(#####\s)|(######\s))',
        '',
        line
    )
    return line


def md_table_row_to_array(line):
    """
    Recieves a table line and parses it's content as a array of strings, with
    each element representing a column.
    """
    # replaces the | characters between the text with a totally random string
    line = re.sub(r'(\ \|\ )', '3Vb7adZJNY', line)
    line = re.sub(r'(\|\ )|(\ \|)', '', line)
    line = line.replace("\n", '')
    line = line.split('3Vb7adZJNY')
    return line


def add_md_checkbox(itemized_string):
    """
    Converts a itemized string in a formatted markdown checkbox list.
    """
    items = itemized_string.split(';')
    a = ""
    for item in items:
        a += str('- [ ] ' + item + '\n')
    return a


def format_description(string):
    """
    Adds the header and a final new line to the issue description string.
    """
    return str('**Issue description:**\n' + string + '\n')


def add_prefix_to_title(title, number, prefix, subid, numerate):
    """
    Formats the issue title to match the required for the project.
    """
    subid = subid.upper()
    prefix = prefix.upper()
    title = title.capitalize()
    if numerate:
        return str(prefix + subid + str(number) + " " + title)
    return str(prefix + subid + " " + title)


def get_all_lines(file):
    """
    Reads a file returning all it's lines in a array of lines format.
    """
    line = file.readline()
    lines = []
    while line:
        lines.append(line)
        line = file.readline()
    return lines


def get_table_spec(line):
    """
    Gets the table header and returns both it's length and it's formatted self.
    """
    thead = md_table_row_to_array(line)
    return len(thead), thead
    # (\|:*-*:*) regex to ignore the split line
    # (\ *\|\ *:*-*:*\ *)


def format_acc_criteria(string):
    """
    Formats the string adding the acceptance criteria header and adds a final
    new line.
    """
    checkboxes = add_md_checkbox(string)
    acc_criteria = "**Acceptance criteria:**\n"

    return "%s%s" % (acc_criteria, checkboxes)


def format_tasks(string):
    """
    Formats the string adding the tasks header and adds a final new line.
    """
    checkboxes = add_md_checkbox(string)
    tasks = "**Tasks:**\n"
    return "%s%s" % (tasks, checkboxes)


def make_md_formatting(configuration_header, content):
    """
    Dinamically formats the markdown content according to it's column header.
    """
    func_dict = {
        "description": format_description,
        "body": format_description,
        "acceptance criteria": format_acc_criteria,
        "tasks": add_md_checkbox,
    }

    print(configuration_header)
    print(content)

    for idx in range(len(configuration_header)):
        if len(configuration_header) == 0 or idx == 0:
            pass
        else:
            content[idx] = func_dict[configuration_header[idx]](
                str(content[idx][idx]))
    return content
