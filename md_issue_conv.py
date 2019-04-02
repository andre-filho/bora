import re
import requests as req
import json


GITHUB_BASE_URL = "http://api.github.com"
GITLAB_BASE_URL = "http://gitlab.com/api/v4"


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


def add_md_checkbox(item):
    return str('- [ ] ' + item + '\n')


def format_description(description):
    return str('**Issue description:**\n' + description + '\n')


def add_prefix_to_title(title, number, prefix='US', subid=''):
    return str(prefix + subid + str(number) + title)


def get_all_lines(file):
    line = file.readline()
    file2 = open('xxx.txt', 'w+')
    while line:
        md_tables_to_array(line, file2)
        line = file.readline()
    file2.close()


def create_issue_github(title, description, acceptance_criteria, repo_name, owner):
    github = "/repos/%s/%s" % owner, repo_name
    endpoint = GITHUB_BASE_URL + github
    
    issue = {'title': title, 'body': description + '\n' + acceptance_criteria}
    issue = json.dumps(issue)

    return make_api_call(issue, endpoint)


def create_issue_gitlab(title, description, acceptance_criteria, repo_id):
    gitlab = "/projects/%i/issues" % repo_id
    endpoint = GITLAB_BASE_URL + gitlab
    
    issue = {'title': title, 'body': description + '\n' + acceptance_criteria}
    issue = json.dumps(issue)

    return make_api_call(issue, endpoint)
    


def make_api_call(json, url):
    a = req.post(url, json=json)
    return a.status_code


if __name__ == "__main__":
    try:
        file = open('teste.md')
        get_all_lines(file)

    finally:
        file.close()
