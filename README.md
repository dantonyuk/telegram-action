# Telegram Notifier

[![Actions Status](https://github.com/dantonyuk/telegram-action/workflows/Notify/badge.svg)](https://github.com/dantonyuk/telegram-action/actions)

Github action to send notification to Telegram about Github events.

![](images/push-notifications.jpg)

## Usage

```yml
name: Telegram Notifications
on: [push]
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - uses: dantonyuk/telegram-action@v2
      with:
        destination: ${{ secrets.TELEGRAM_TO }}
        token: ${{ secrets.TELEGRAM_TOKEN }}
```

## Supported Event

* push
* pull_request
* pull_request_review
* issues
* issue_comment
