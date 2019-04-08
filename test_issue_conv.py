import md_issue_conv as conv


def test_md_table_row_to_array():
    md = '| get to the choppa | asdf | jkl |'
    array = conv.md_table_row_to_array(md)

    if not array == ['get to the choppa', 'asdf', 'jkl']:
        raise AssertionError()


def test_add_md_checkbox():
    arg = "asdf;asdf;adsf;asdf"
    resp = conv.add_md_checkbox(arg)
    if not (resp == '- [ ] asdf\n- [ ] asdf\n- [ ] adsf\n- [ ] asdf\n'):
        raise AssertionError()


def test_format_description():
    desc = "lorem ipsum dolor sit amet"
    a = conv.format_description(desc)
    print(repr(a))
    if not (a == '**Issue description:**\nlorem ipsum dolor sit amet\n'):
        raise AssertionError()


def test_add_prefix_to_title():
    titles = ["make america great again", "make stuff work"]
    formattedUS = []
    formattedTS = []
    
    for idx, title in enumerate(titles):
        formattedUS.append(conv.add_prefix_to_title(title, idx+1))
        formattedTS.append(conv.add_prefix_to_title(title, idx+1, prefix='TS'))

    if not (formattedUS[0] == 'US1 make america great again' and formattedTS[0] == 'TS1 make america great again'):
        raise AssertionError()
    if not (formattedUS[1] == 'US2 make stuff work' and formattedTS[1] == 'TS2 make stuff work'):
        raise AssertionError()


def test_create_issue():
    title = "US1 make america great again"
    description = "American economy is currently a trash."
    acceptance_criteria = "- [ ] asdfasdfasdf\n"
    issue = conv.create_issue(title, description, acceptance_criteria)
    
    exp_json = '{"title": "US1 make america great again", "body": "American economy is currently a trash.\n- [ ] asdfasdfasdf\n"}'

    if not issue == repr(exp_json):
        raise AssertionError()


def test_create_github_url():
    pass


def test_create_gitlab_url():
    pass
