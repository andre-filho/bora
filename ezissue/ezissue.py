import os
import re
import click
import getpass
import requests
import json as js
from os.path import join
from os.path import dirname

from ezissue.converter.manipulation import *
from ezissue.secops.secops_basic import get_token
from ezissue.secops.secops_basic import folder_path
from ezissue.secops.secops_basic import write_tokens
from ezissue.secops.secops_basic import create_secure_key


GITHUB_BASE_URL = "http://api.github.com"
GITLAB_BASE_URL = "https://gitlab.com/api/v4"


def create_issue_json(title, description, acceptance_criteria, repo_host):
    body = "%s\n%s" % (description, acceptance_criteria)

    if repo_host == 'gitlab':
        return js.dumps({"title": title, "description": body})

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
    
    my_token = get_token(host)
    if not host == 'github':
        a = requests.post(
            url,
            data=json_issue,
            headers={
                'PRIVATE-TOKEN': my_token,
                'Content-Type': 'application/json'
            }
        )
    else:
        auth = 'Bearer %s' % my_token
        a = requests.post(
            url,
            data=json_issue,
            headers={
                'Authorization': auth,
                'Content-Type': 'application/json'
            }
        )
    return a


@click.command()
@click.argument("filename", required=True)
@click.argument("repo_host", type=click.Choice(["github", "gitlab"], case_sensitive=False), required=True)
@click.option("--subid", required=False, default="", type=str)
@click.option("--numerate", required=False, default=True, type=bool)
@click.option("--prefix", required=False, default="", type=click.Choice(["US", "TS", "", "BUG"], case_sensitive=False))
def main(filename, repo_host, prefix, subid, numerate):
    if not os.path.isfile(folder_path + 'key.key'):
        config()

    try:
        file = open(filename)
        lines = get_all_lines(file)
        rows = []

        for line in lines:
            rows.append(md_table_row_to_array(line))

        for idx, row in enumerate(rows):
            row[0] = add_prefix_to_title(
                row[0], idx+1, prefix, subid, numerate)
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

        print(repr(url))
        responses = []

        for row in rows:
            responses.append(
                make_api_call(
                    create_issue_json(row[0], row[1], row[2], repo_host),
                    url,
                    repo_host
                )
            )

        for resp in responses:
            print('\n\nRespose:\n')
            print(resp.status_code)
    finally:
        file.close()


def config():
    print("Config file not found! Initializing configuration...")
    ghtk = getpass.getpass(prompt="Please insert your github token: ")
    gltk = getpass.getpass(prompt="Please insert your gitlab token: ")
    b = create_secure_key()
    a = write_tokens(ghtk, gltk)
    if a:
        print("Created config files successfully!\n(They're encrypted, don't worry)")
    else:
        print("Something went wrong, please try again.")


if __name__ == "__main__":
    main()
