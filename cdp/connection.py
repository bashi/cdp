# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

import json
from Queue import Empty
from Queue import Queue
from threading import Thread
import websocket


class _SenderThread(Thread):

  def __init__(self, conn):
    super(_SenderThread, self).__init__()
    self.daemon = True
    self._conn = conn

  def run(self):
    while self._conn.is_running:
      req = self._conn._requests.get()
      try:
        self._conn._websocket.send(json.dumps(req))
      except IOError as err:
        print('Connection error: %s' % err.message)
        self._conn.Close()


class _ReceiverThread(Thread):

  def __init__(self, conn):
    super(_ReceiverThread, self).__init__()
    self.daemon = True
    self._conn = conn

  def run(self):
    while self._conn.is_running:
      try:
        raw_res = self._conn._websocket.recv()
        res = json.loads(raw_res)
        if res.get('id'):
          self._conn._responses.put(res)
        else:
          self._conn._events.put(res)
      except IOError as err:
        print('Connection error: %s' % err.message)
        self._conn.Close()


class Connection(object):

  def __init__(self, url):
    self._url = url
    self._websocket = websocket.create_connection(self._url)
    self._current_request_id = 1
    self._requests = Queue()
    self._responses = Queue()
    self._events = Queue()

    self._sender = _SenderThread(self)
    self._receiver = _ReceiverThread(self)

    self._is_running = True
    self._sender.start()
    self._receiver.start()

  @property
  def is_running(self):
    return self._is_running

  def Close(self):
    if self._is_running:
      self._websocket.close()
      self._websocket = None
      self._is_running = False

  def CallMethod(self, method_name, params=None):
    request = {
        'id': self._current_request_id,
        'method': method_name,
        'params': params,
    }
    self._current_request_id += 1
    self._requests.put(request)

  def CallMethodSync(self, method_name, params=None):
    self.CallMethod(method_name, params)
    return self.GetResponse()

  def GetResponse(self):
    try:
      res = self._responses.get(timeout=10)
    except Empty:
      raise Exception('Response timed out')
    return res

  def GetEvent(self, timeout=None):
    return self._events.get(timeout=timeout)
