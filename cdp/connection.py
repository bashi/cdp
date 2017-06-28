# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# pylint: disable=C0111

import json
from Queue import Empty
from Queue import Queue
from threading import Thread
import websocket


class Connection(Thread):

  def __init__(self, url):
    super(Connection, self).__init__()
    self.daemon = True
    self._url = url
    self._websocket = websocket.create_connection(self._url)
    self._websocket.settimeout(2)
    self._current_request_id = 1
    self._requests = Queue()
    self._events = Queue()
    self._responses = Queue()
    self._is_running = False
    self.start()

  @property
  def is_running(self):
    return self._is_running

  def run(self):
    self._is_running = True
    while self._is_running:
      req = self._requests.get()
      try:
        self._websocket.send(json.dumps(req))
        raw_res = self._websocket.recv()
        res = json.loads(raw_res)
        if res.get('id'):
          self._responses.put(res)
        else:
          self._events.put(res)
      except IOError as err:
        self._websocket.close()
        self._websocket = None
        self._is_running = False
        print('Connection closed: %s' % err.message)
        break

  def Stop(self):
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
