import re
import requests
import json


GITHUB_BASE_URL = "http://api.github.com"
GITLAB_BASE_URL = "http://gitlab.com/api/v4"


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
    file2 = open('xxx.txt', 'w+')

    while line:
        md_table_row_to_array(line)
        line = file.readline()

    file2.close()


def create_issue(title, description, acceptance_criteria):
    issue = {'title': title, 'body': description + '\n' + acceptance_criteria}
    issue = json.dumps(issue)
    return issue


def create_github_url(repo_name, owner):
    github = "/repos/%s/%s" % owner, repo_name
    endpoint = GITHUB_BASE_URL + github
    return github + endpoint


def create_gitlab_url(repo_id, private_token):
    gitlab = "/projects/%i/issues" % repo_id
    endpoint = GITLAB_BASE_URL + gitlab
    return gitlab + endpoint


def make_api_call(json, url, private_token=None):
    if private_token is not None:
        a = request.post(url, json=json, headers={'PRIVATE-TOKEN': private_token})
    else:
        a = request.post(url, json=json)
    return a.status_code


if __name__ == "__main__":
    try:
        file = open('teste.md')
        get_all_lines(file)

    finally:
        file.close()
