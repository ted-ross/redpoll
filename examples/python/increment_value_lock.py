#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from proton.handlers import MessagingHandler
from proton.reactor import Container
from redpoll.request_response import RequestClient
from redpoll.lock import Lock

class IncrementValueLock(MessagingHandler):
    def __init__(self, bus_address, service_address, lock_name):
        super(IncrementValueLock, self).__init__()
        self.bus_address     = bus_address
        self.service_address = service_address
        self.lock_name       = lock_name

    def on_start(self, event):
        self.container = event.container
        self.conn      = self.container.connect(self.bus_address)
        self.client    = RequestClient(self.container, self.conn, self.service_address)
        self.lock      = Lock(self.container, self.conn, self.lock_name)
        self.started   = False
        self.lock_held = False

    def on_service_ready(self, event):
        if not self.started:
            self.started = True
            self.lock.acquire()

    def on_lock_acquired(self, event):
        self.lock_held = True
        self.client.request({'opcode':'GET'})

    def on_lock_failed(self, event):
        print("Lock Failed")
        self.client.stop()
        self.lock.destroy()
        self.conn.close()

    def on_lock_released(self, event):
        self.lock_held = False

    def on_request_failed(self, event):
        pass

    def on_response(self, event):
        done = False
        try:
            props = event.properties
            if props['opcode'] == 'GET':
                if self.lock_held:
                    self.client.request({'opcode':'PUT', 'value':(props['value'] + 1)})
                else:
                    print("Aborted sequence: lock was dropped")
                    done = True
            elif props['opcode'] == 'PUT':
                print("Value set to %d" % props['value'])
                self.lock.release()
                done = True

        except Exception, e:
            print("EXCEPTION: %r" % e)

        if done:
            self.lock.destroy()
            self.client.stop()
            self.conn.close()


Container(IncrementValueLock("127.0.0.1:5672", "counterValue", "mutex.counterValue")).run()

