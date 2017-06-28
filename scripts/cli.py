# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

from IPython import embed
from cdp import actions
from cdp.devtools import DevTools


def _GenerateHeader(pages):
  header = '''Variables:
  devtools
  browser
  pages
'''
  for i, page in enumerate(pages):
    header += '    %d: %s\n' % (i, page.metadata['title'])
  return header


def main():
  devtools = DevTools()
  browser = devtools.GetBrowserClient()  # pylint: disable=W0612
  pages = devtools.GetPageClients()
  header = _GenerateHeader(pages)
  embed(header=header)


if __name__ == '__main__':
  main()
