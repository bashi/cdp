import os
import sys
import time

from cdp import actions
from cdp.devtools import DevTools


_CONSUME_URL_SMALL = 'http://output.jsbin.com/dovute?count=10000'
_CONSUME_URL_MEDIUM = 'http://output.jsbin.com/dovute?count=50000'
_CONSUME_URL_LARGE = 'http://output.jsbin.com/dovute?count=150000'


def main():
  devtools = DevTools()
  urls = [
      _CONSUME_URL_SMALL,
      _CONSUME_URL_MEDIUM,
      _CONSUME_URL_LARGE,
  ]
  pages = []
  for url in urls:
    page = devtools.CreateNewPage()
    actions.Navigate(page, url)
    time.sleep(5)
    pages.append(page)


if __name__ == '__main__':
  main()
