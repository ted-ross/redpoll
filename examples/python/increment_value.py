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

class IncrementValue(MessagingHandler):
    def __init__(self, bus_address, service_address):
        super(IncrementValue, self).__init__()
        self.bus_address     = bus_address
        self.service_address = service_address

    def on_start(self, event):
        self.container = event.container
        self.conn      = self.container.connect(self.bus_address)
        self.client    = RequestClient(self.container, self.conn, self.service_address)
        self.sent_get  = False

    def on_service_ready(self, event):
        if not self.sent_get:
            self.client.request({'opcode':'GET'})

    def on_request_failed(self, event):
        pass

    def on_response(self, event):
        try:
            props = event.properties
            if props['opcode'] == 'GET':
                self.client.request({'opcode':'PUT', 'value':(props['value'] + 1)})
            elif props['opcode'] == 'PUT':
                print("Value set to %d" % props['value'])
                self.client.stop()
                self.conn.close()
        except Exception, e:
            print("EXCEPTION: %r" % e)


Container(IncrementValue("127.0.0.1:5672", "counterValue")).run()

