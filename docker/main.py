import os
from pathlib import Path

if __name__ == "__main__":
    print(os.environ)
    event_path = os.environ['GITHUB_EVENT_PATH']
    contents = Path(event_path).read_text()
    print(contents)

