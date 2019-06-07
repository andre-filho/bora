import os
import click
import getpass
import requests
import json as js

import ezissue.utils as u
from ezissue.converter.manipulation import *
from ezissue.secops.secops_basic import get_token
from ezissue.secops.secops_basic import folder_path
from ezissue.secops.secops_basic import write_tokens
from ezissue.secops.secops_basic import create_secure_key


GITHUB_BASE_URL = "https://api.github.com"
GITLAB_BASE_URL = "https://gitlab.com/api/v4"


def create_issue_json(tconf, values, repo_host):
    n_fields = len(tconf)
    d = dict()

    if n_fields != len(values):
        u.error(
            'Error: markdown table header and contents columns do not match!')
        raise

    for idx in range(n_fields):
        if tconf[idx] == 'title':
            d.update({'title': values[idx][idx]})
        elif tconf[idx] == 'description' and repo_host == 'github':
            d.update({'body': values[idx]})
        elif tconf[idx] == 'body' and repo_host == 'gitlab':
            d.update({'description': values[idx]})
        else:
            d.update({tconf[idx]: values[idx]})
    return d


def create_github_url(repo_name, owner):
    github = "/repos/%s/%s/issues" % (owner.lower(), repo_name.lower())
    endpoint = GITHUB_BASE_URL + github
    return endpoint


def create_gitlab_url(repo_id):
    gitlab = "/projects/%i/issues" % repo_id
    endpoint = GITLAB_BASE_URL + gitlab
    return endpoint


def make_api_call(json_issue, url, host, debug):
    u.debug(json_issue, debug)

    my_token = get_token(host)

    if not host == 'github':
        response = requests.post(
            url,
            data=js.dumps(json_issue),
            headers={
                'PRIVATE-TOKEN': my_token,
                'Content-Type': 'application/json'
            }
        )
    else:
        auth = 'Bearer %s' % my_token
        response = requests.post(
            url,
            data=js.dumps(json_issue),
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': auth,
                'Content-Type': 'application/json'
            }
        )
    return response, json_issue


@click.command()
@click.argument(
    "filename",
    required=True
)
@click.argument(
    "repo_host",
    type=click.Choice(["github", "gitlab"], case_sensitive=False),
    required=True
)
@click.option(
    "--subid",
    "-s",
    required=False,
    default="",
    type=str,
    help='Pass an sub-id into the issue\'s title'
)
@click.option(
    "--numerate",
    "-n",
    required=False,
    is_flag=True,
    help='Numerate the issues on the table\'s order'
)
@click.option(
    "--prefix",
    "-p",
    required=False,
    default="",
    type=click.Choice(["US", "TS", "", "BUG"], case_sensitive=False),
    help='Adds a prefix on the issue\'s title'
)
@click.option(
    "--debug",
    "-d",
    default=False,
    is_flag=True,
    help='Enables debug mode'
)
def main(filename, repo_host, prefix, subid, numerate, debug):
    if not os.path.isfile(folder_path + 'key.key'):
        config()

    try:
        file = open(filename)
        lines = get_all_lines(file)
        rows = []

        for idx, line in enumerate(lines):
            if idx == 0:
                col_count, columns = get_table_spec(line)
            elif idx == 1:
                pass
            else:
                rows.append(md_table_row_to_array(line))

        if repo_host == 'github':
            repo = u.get_from_user("Enter repo name: (Ex.: username/repo)")
            repo = repo.split('/')
            url = create_github_url(repo[1], repo[0])
        else:
            repo = int(u.get_from_user("Enter the repo id: (Ex.: 9120898)"))
            url = create_gitlab_url(repo)

        u.debug(repr(url), debug)
        u.debug(repr(repo_host), debug)

        for idx, row in enumerate(rows):
            row[0] = add_prefix_to_title(
                row[0], idx+1, prefix, subid, numerate)

        rows = make_md_formatting(columns, rows)

        for row in rows:
            response, issue = make_api_call(
                create_issue_json(columns, rows, repo_host),
                url,
                repo_host,
                debug
            )
            u.show_resp_req(issue, response)

    finally:
        file.close()


def config():
    u.notify("Config file not found! Initializing configuration...")
    ghtk = getpass.getpass(prompt="Please insert your github token: ")
    gltk = getpass.getpass(prompt="Please insert your gitlab token: ")
    create_secure_key()
    a = write_tokens(ghtk, gltk)
    if a:
        u.prompt("Created config files successfully!")
        u.prompt("(They're encrypted, don't worry)")
    else:
        u.prompt("Something went wrong, please try again.")


if __name__ == "__main__":
    main()
