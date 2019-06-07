import re


def remove_md_titles(line):
    line = re.sub(
        r'((#\s)|(##\s)|(###\s)|(####\s)|(#####\s)|(######\s))',
        '',
        line
    )
    return line


def md_table_row_to_array(line):
    # this will need to be fixed at some moment
    line = re.sub(r'(\ \|\ )', '-', line)
    line = re.sub(r'(\|\ )|(\ \|)', '', line)
    line = line.replace("\n", '')
    line = line.split('-')
    return line


def add_md_checkbox(items):
    items = items.split(';')
    a = ""
    for item in items:
        a += str('- [ ] ' + item + '\n')
    return a


def format_description(string):
    return str('**Issue description:**\n' + string + '\n')


def add_prefix_to_title(title, number, prefix, subid, numerate):
    subid = subid.upper()
    prefix = prefix.upper()
    title = title.capitalize()
    if numerate:
        return str(prefix + subid + str(number) + " " + title)
    return str(prefix + subid + " " + title)


def get_all_lines(file):
    line = file.readline()
    lines = []
    while line:
        lines.append(line)
        line = file.readline()
    return lines


def get_table_spec(line):
    thead = md_table_row_to_array(line)
    return len(thead), thead
    # (\|:*-*:*) regex to ignore the split line
    # (\ *\|\ *:*-*:*\ *)


def format_acc_criteria(string):
    checkboxes = add_md_checkbox(string)
    acc_criteria = "**Acceptance criteria:**\n"

    return "%s%s" % (acc_criteria, checkboxes)


def format_tasks(string):
    checkboxes = add_md_checkbox(string)
    tasks = "**Tasks:**\n"
    return "%s%s" % (tasks, checkboxes)


def make_md_formatting(conf, cont):
    func_dict = {
        "description": format_description,
        "body": format_description,
        "acceptance criteria": format_acc_criteria,
        "tasks": add_md_checkbox,
    }

    for idx in range(len(conf)):
        if len(conf) == 0 or idx == 0:
            pass
        else:
            cont[idx] = func_dict[conf[idx]](str(cont[idx][idx]))
    return cont
