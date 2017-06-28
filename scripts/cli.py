# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

import pprint
import threading

from IPython import embed
from cdp import actions
from cdp.devtools import DevTools


def _ShowEvents(target):

  def _Runner():
    target.EnsureConnection()
    while target.connection.is_running:
      try:
        event = target.connection.GetEvent()
        pprint.pprint(event)
      except Exception:
        break

  t = threading.Thread(target=_Runner)
  t.daemon = True
  t.start()


def _GenerateHeader(pages):
  header = '''Variables:
  devtools
  browser
  pages[]
'''
  for i, page in enumerate(pages):
    header += '    %d: %s\n' % (i, page.metadata['title'])
  return header


def main():
  devtools = DevTools()
  browser = devtools.GetBrowserClient()
  _ShowEvents(browser)
  pages = devtools.GetPageClients()
  for page in pages:
    _ShowEvents(page)
  header = _GenerateHeader(pages)
  embed(header=header)


if __name__ == '__main__':
  main()
