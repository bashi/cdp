# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

from cdp.connection import Connection


class _DomainAttr(object):
  def __init__(self, target, domain):
    for command in domain['commands']:
      name = command['name']
      command_name = domain['domain'] + '.' + name
      command_attr = _CommandAttr(target, command_name)
      setattr(self, name, command_attr)


class _CommandAttr(object):
  def __init__(self, target, command_name):
    self._target = target
    self._command_name = command_name
  
  def __call__(self, **kargs):
    return self._target.Call(self._command_name, kargs)


class TargetBase(object):

  def __init__(self):
    self._conn = None

  @property
  def websocket_url(self):
    raise NotImplementedError()

  def EnsureConnection(self):
    if not self._conn or not self._conn.is_running:
      self._conn = Connection(self.websocket_url)

  def InstallCommands(self, protocol):
    for domain in protocol['domains']:
      domain_attr = _DomainAttr(self, domain)
      setattr(self, domain['domain'], domain_attr)

  def Call(self, method_name, params=None):
    self.EnsureConnection()
    return self._conn.CallMethodSync(method_name, params)


class Browser(TargetBase):

  def __init__(self, host, port):
    super(Browser, self).__init__()
    self._host = host
    self._port = port

  @property
  def websocket_url(self):
    return 'ws://%s:%s/devtools/browser' % (self._host, self._port)


class Page(TargetBase):

  def __init__(self, metadata):
    super(Page, self).__init__()
    self._metadata = metadata

  @property
  def websocket_url(self):
    return self._metadata['webSocketDebuggerUrl']

  @property
  def target_id(self):
    return self._metadata['id']

  @property
  def metadata(self):
    return self._metadata
