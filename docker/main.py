import os, sys, inspect
import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import re

def event_payload():
    event_path = os.environ['GITHUB_EVENT_PATH']
    contents = Path(event_path).read_text()
    return json.loads(contents)


def render_template(name):
    env = Environment(loader=FileSystemLoader('/templates'), trim_blocks=True)
    env.filters['lines'] = lambda value: [line for line in value.splitlines() if line]

    payload = event_payload()
    action = payload.get('action')
    try:
        template = env.get_template(f'{name}_{action}.html')
    except:
        template = env.get_template(f'{name}.html')

    print(json.dumps(payload, indent=2))
    return template.render(**payload)


def notify(message):
    import requests
    import textwrap

    chat_ids = re.split(',\s*', os.environ['INPUT_DESTINATION'])
    token = os.environ['INPUT_TOKEN']

    for chat_id in chat_ids:
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
            'chat_id': chat_id,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True,
            'text': textwrap.dedent(message)
        })


def handle_push():
    notify(render_template('push'))


def handle_pull_request():
    notify(render_template('pull_request'))


def handle_pull_request_review():
    notify(render_template('pull_request_review'))


def handle_issues():
    notify(render_template('issues'))


def handle_issue_comment():
    notify(render_template('issue_comment'))


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
