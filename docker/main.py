import os, sys, inspect
from pathlib import Path

def event_payload():
    import json
    event_path = os.environ['GITHUB_EVENT_PATH']
    contents = Path(event_path).read_text()
    return json.loads(contents)


def notify(message):
    import requests
    import textwrap

    chat_id = os.environ['INPUT_DESTINATION']
    token = os.environ['INPUT_TOKEN']

    requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
        'chat_id': chat_id,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True,
        'text': textwrap.dedent(message)
    })


def handle_push():
    payload = event_payload()
    env = os.environ

    event_name = env['GITHUB_EVENT_NAME']
    repo = env['GITHUB_REPOSITORY']
    server = env['GITHUB_SERVER_URL']
    actor = env['GITHUB_ACTOR']

    commits = '\n'.join([f"""\
        <a href="{commit['url']}">{commit['id'][:8]}</a> {commit['message']}"""
        for commit in payload['commits'][::-1]])

    notify(f"""\
        {event_name} in <a href="{server}/{repo}">{repo}</a> by <a href="{server}/{actor}">{actor}</a>

        Commits (<a href="{payload['compare']}">Diff</a>):\n""" + commits)


def handle_pull_request():
    payload = event_payload()
    env = os.environ

    repo = env['GITHUB_REPOSITORY']
    server = env['GITHUB_SERVER_URL']
    actor = env['GITHUB_ACTOR']
    action = payload['action']
    pr = payload['pull_request']

    notify(f"""\
        PR #<a href="{pr['html_url']}">{pr['number']}</a> {pr['title']}
        {action} in <a href="{server}/{repo}">{repo}</a> by <a href="{server}/{actor}">{actor}</a>
        """)


if __name__ == "__main__":
    env = os.environ
    event_name = os.environ['GITHUB_EVENT_NAME']

    members = inspect.getmembers(sys.modules[__name__])
    func_name = f'handle_{event_name}'
    funcs = [obj for name, obj in members if name == func_name]
    if funcs:
        funcs[0]()
    else:
        repo = env['GITHUB_REPOSITORY']
        server = env['GITHUB_SERVER_URL']
        notify(f'{event_name} in <a href="{server}/{repo}">{repo}</a>')
