# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

import requests

from cdp import target_clients


class DevTools(object):

  def __init__(self, host='localhost', port='9222'):
    self._host = host
    self._port = port
    self._cached_protocol = None

  @property
  def _base_url(self):
    return 'http://%s:%s/json' % (self._host, self._port)

  def GetTargets(self):
    url = self._base_url + '/list'
    res = requests.get(url)
    return res.json()

  def GetProtocol(self):
    if not self._cached_protocol:
      url = self._base_url + '/protocol'
      res = requests.get(url)
      self._cached_protocol = res.json()
    return self._cached_protocol

  def GetVersion(self):
    url = self._base_url + '/version'
    res = requests.get(url)
    return res.json()

  def CreateNewPage(self):
    url = self._base_url + '/new'
    res = requests.get(url)
    metadata = res.json()
    page = target_clients.Page(metadata)
    page.InstallCommands(self.GetProtocol())
    return page

  def CloseTarget(self, target_id):
    url = self._base_url + '/close/' + target_id
    res = requests.get(url)
    return res.status_code == 200

  def ActivateTarget(self, target_id):
    url = self._base_url + '/activate/' + target_id
    res = requests.get(url)
    return res.status_code == 200

  def GetBrowserClient(self):
    browser = target_clients.Browser(self._host, self._port)
    browser.InstallCommands(self.GetProtocol())
    return browser

  def GetPageClients(self):
    def _CreatePageClient(target):
      page = target_clients.Page(target)
      page.InstallCommands(self.GetProtocol())
      return page

    targets = self.GetTargets()
    return [
        _CreatePageClient(target) for target in targets
        if target['type'] == 'page'
    ]
