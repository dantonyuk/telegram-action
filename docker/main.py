import os, sys, inspect
import requests
from pathlib import Path

def event_payload():
    event_path = os.environ['GITHUB_EVENT_PATH']
    return Path(event_path).read_text()


def notify(message):
    chat_id = os.environ['INPUT_DESTINATION']
    token = os.environ['INPUT_TOKEN']

    requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
        'chat_id': chat_id,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True,
        'text': message
    })

if __name__ == "__main__":
    env = os.environ
    print(env)
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
