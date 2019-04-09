import re
import requests
import json


GITHUB_BASE_URL = "https://api.github.com"
GITLAB_BASE_URL = "https://gitlab.com/api/v4"


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


def create_issue_json(title, description, acceptance_criteria):
    issue = {'title': title, 'body': description + '\n' + acceptance_criteria}
    issue = json.dumps(issue)
    return issue


def create_github_url(repo_name, owner):
    github = "/repos/%s/%s/issues" % (owner, repo_name)
    endpoint = GITHUB_BASE_URL + github
    return endpoint


def create_gitlab_url(repo_id):
    gitlab = "/projects/%i/issues" % repo_id
    endpoint = GITLAB_BASE_URL + gitlab
    return endpoint


def make_api_call(json, url, private_token=None):
    if private_token is not None:
        a = requests.post(url, json=json, headers={'PRIVATE-TOKEN': private_token})
    else:
        a = requests.post(url, json=json, headers={'User-Agent': 'andre-filho'})
    return a.json()


if __name__ == "__main__":
    try:
        file = open('teste.md')
        lines = get_all_lines(file)
        rows = []
        for line in lines:
            rows.append(md_table_row_to_array(line))
        print(rows)
        print('-------------------')
        for idx, row in enumerate(rows):
            row[0] = add_prefix_to_title(row[0], idx+1)
            row[1] = format_description(row[1])
            row[2] = add_md_checkbox(row[2])
        print(rows)
        issues = []
        print('-------------------')
        for row in rows:
            issues.append(create_issue_json(row[0], row[1], row[2]))
        print(issues)
        print(type(issues[0]))
        print('-------------------')
        url = create_github_url('commit-helper', 'andre-filho')
        print(url)
        responses = []
        for issue in issues:
            responses.append(make_api_call(issue, url))
            print(responses)
        print(requests.get(url).json())
    finally:
        file.close()
