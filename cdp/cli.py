# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

from IPython import embed

from cdp.devtools import DevTools


def main():
  devtools = DevTools()  # pylint: disable=W0612
  embed()


if __name__ == '__main__':
  main()
