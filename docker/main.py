import os, sys, inspect
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def event_payload():
    import json
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

    print(f"{payload}")
    return template.render(**payload)


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
    notify(render_template('push'))


def handle_pull_request():
    notify(render_template('pull_request'))


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
