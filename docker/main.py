import os, sys, inspect
import requests
from pathlib import Path

def event_payload():
    event_path = os.environ['GITHUB_EVENT_PATH']
    return Path(event_path).read_text()


def notify(message):
    chat_id = os.environ['destination']
    token = os.environ['token']

    requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
        'chat_id': chat_id,
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': True,
        'text': message
    })

if __name__ == "__main__":
    env = os.environ
    print(env)
    event_name = os.environ['GITHUB_EVENT_NAME']

    funcs = [obj for name, obj in inspect.getmembers(sys.modules[__name__]) if name == event_name]
    if funcs:
        funcs[0]()
    else:
        notify(f"{event_name} in [{env['GITHUB_REPOSITORY']}]({env['GITHUB_SERVER_URL']}/{env['GITHUB_REPOSITORY']})")

    print(contents)

