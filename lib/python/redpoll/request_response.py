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

from __future__ import print_function, unicode_literals
from proton import Message, Condition
from proton.handlers import MessagingHandler
from proton.reactor import Container, EventInjector, ApplicationEvent

class Request(object):
    def __init__(self, event):
        self.message      = event.message
        self.in_delivery  = event.delivery
        self.out_delivery = None

    def __str__(self):
        return "Request"

    @property
    def properties(self):
        return self.message.properties if self.message.properties else {}

    @property
    def body(self):
        return self.message.body


class RequestServer(MessagingHandler):
    def __init__(self, reactor, connection, service_address):
        super(RequestServer, self).__init__(auto_accept=False, auto_settle=False)
        self.service_address = service_address
        self.reactor         = reactor
        self.events          = EventInjector()
        self.reactor.selectable(self.events)

        self.connection       = connection
        self.service_receiver = self.reactor.create_receiver(self.connection, self.service_address, handler=self)
        self.reply_sender     = self.reactor.create_sender(self.connection, None, handler=self)

    def stop(self):
        self.service_receiver.close()
        self.reply_sender.close()
        self.events.close()

    def fail(self, request, message):
        request.in_delivery.local.condition = Condition('redpoll:bad-request', message)
        self.reject(request.in_delivery)

    def reply(self, request, properties={}, data=None):
        reply_message = Message(properties=properties,
                                body=data,
                                address=request.message.reply_to,
                                correlation_id=request.message.correlation_id)
        request.out_delivery = self.reply_sender.send(reply_message)
        request.out_delivery._request = request

    def on_settled(self, event):
        try:
            request = event.delivery._request
            self.accept(request.in_delivery)
        except:
            pass

    def on_message(self, event):
        request               = Request(event)
        request_event         = ApplicationEvent("request")
        request_event.request = request
        request_event.server  = self
        self.events.trigger(request_event)


class RequestClient(MessagingHandler):
    def __init__(self, reactor, connection, service_address):
        super(RequestClient, self).__init__()
        self.service_address = service_address
        self.reactor         = reactor
        self.events          = EventInjector()
        self.reactor.selectable(self.events)

        self.connection     = connection
        self.service_sender = None
        self.reply_receiver = self.reactor.create_receiver(self.connection, dynamic=True, handler=self)
        self.reply_to       = None
        self.ready          = False
        self.cid            = 1
        self.contexts       = {}

    def stop(self):
        self.service_sender.close()
        self.reply_receiver.close()
        self.events.close()

    def request(self, properties={}, body=None, user_context=None):
        cid = self.cid
        self.cid += 1
        request_message = Message(properties     = properties,
                                  body           = body,
                                  reply_to       = self.reply_to,
                                  correlation_id = cid)
        self.contexts[cid] = user_context

        dlv      = self.service_sender.send(request_message)
        dlv._cid = cid

    def on_link_opened(self, event):
        if event.receiver == self.reply_receiver:
            self.reply_to = self.reply_receiver.remote_source.address
            self.service_sender = self.reactor.create_sender(self.connection, self.service_address, handler=self)

    def on_sendable(self, event):
        if not self.ready and event.sender == self.service_sender:
            self.ready = True
            self.events.trigger(ApplicationEvent("service_ready"))

    def on_rejected(self, event):
        dlv = event.delivery
        context = None
        if dlv._cid in self.contexts:
            context = self.contexts[dlv._cid]
        event = ApplicationEvent("request_failed")
        event.context = context
        event.error   = None

    def on_message(self, event):
        reply_message = event.message
        cid           = reply_message.correlation_id
        context       = None
        if cid in self.contexts:
            context = self.contexts[cid]
        new_event              = ApplicationEvent("response")
        new_event.properties   = reply_message.properties if reply_message.properties else {}
        new_event.body         = reply_message.body
        new_event.user_context = context
        new_event.client       = self
        self.events.trigger(new_event)

