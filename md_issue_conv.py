import os
import re
import click
import requests
import json as js
from os.path import join
from os.path import dirname
from dotenv import load_dotenv

from converter.manipulation import *


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GITHUB_BASE_URL = "https://api.github.com"
GITLAB_BASE_URL = "https://gitlab.com/api/v4"
GITHUB_TOKEN = os.getenv('GHTOKEN')
GITLAB_TOKEN = os.getenv('GITLABTOKEN')


def create_issue_json(title, description, acceptance_criteria):
    body = "%s\n%s" % (description, acceptance_criteria)
    return js.dumps({"title": title, "body": body})


def create_github_url(repo_name, owner):
    github = "/repos/%s/%s/issues" % (owner, repo_name)
    endpoint = GITHUB_BASE_URL + github
    return endpoint


def create_gitlab_url(repo_id):
    gitlab = "/projects/%i/issues" % repo_id
    endpoint = GITLAB_BASE_URL + gitlab
    return endpoint


def make_api_call(json_issue, url, host):
    print(json_issue)
    if host is not 'github':
        a = requests.post(
            url,
            data=json_issue,
            headers={
                'PRIVATE-TOKEN': GITLAB_TOKEN,
                'Content-Type': 'application/json'
            }
        )
    else:
        auth = 'Bearer %s' % GITHUB_TOKEN
        a = requests.post(
            url,
            data=json_issue,
            headers={
                'Authorization': auth,
                'Content-Type': 'application/json'
            }
        )
    return a.json()


@click.command()
@click.argument('filename', required=True)
@click.argument("repo_host", type=click.Choice(['github', 'gitlab'], case_sensitive=False), required=True)
def main(filename, repo_host):
    try:
        file = open(filename)
        lines = get_all_lines(file)
        rows = []

        for line in lines:
            rows.append(md_table_row_to_array(line))

        for idx, row in enumerate(rows):
            row[0] = add_prefix_to_title(row[0], idx+1)
            row[1] = format_description(row[1])
            row[2] = add_md_checkbox(row[2])

        issues = []
        if repo_host == 'github':
            repo = input("Enter repo name: (Ex.: username/repo)\n")
            repo = repo.split('/')
            url = create_github_url(repo[1], repo[0])
        else:
            repo = int(input("Enter the repo id: (Ex.: 9120898)\n"))
            url = create_gitlab_url(repo)
            
        print(url)
        responses = []

        for row in rows:
            responses.append(make_api_call(create_issue_json(
                row[0], row[1], row[2]), url, 'github'))

        for resp in responses:
            print('\n')
            print(resp)
    finally:
        file.close()


if __name__ == "__main__":
    main()
